import Foundation

@MainActor
final class AppStore: ObservableObject {
    private enum StorageKey {
        static let profile = "codequest_profile_ios"
        static let results = "codequest_results_ios"
        static let teams = "codequest_teams_ios"
    }

    @Published var profile: UserProfile?
    @Published private(set) var results: [ChallengeResult] = []
    @Published private(set) var teams: [Team] = []

    /// Server-computed stats (points, streak, accuracy).  Updated after API calls.
    @Published private(set) var serverStats: APIService.UserStats?

    /// Non-nil when a network error occurred — views can display it.
    @Published var lastError: String?

    private let api = APIService.shared
    private let defaults = UserDefaults.standard
    private let encoder = JSONEncoder()
    private let decoder = JSONDecoder()

    init() {
        loadLocalState()
        if teams.isEmpty {
            teams = Self.defaultTeams
            save(teams, key: StorageKey.teams)
        }
    }

    // MARK: - Computed properties (local fallbacks)

    var todayChallenge: Challenge {
        ChallengeData.dailyChallenge(for: Date())
    }

    var todayResult: ChallengeResult? {
        let today = Calendar.current.startOfDay(for: Date())
        return results.first {
            Calendar.current.isDate(Calendar.current.startOfDay(for: $0.date), inSameDayAs: today)
        }
    }

    var totalPoints: Int {
        serverStats?.totalPoints ?? results.reduce(0) { $0 + ($1.correct ? $1.points : 0) }
    }

    var streak: Int {
        if let s = serverStats { return s.streak }
        guard !results.isEmpty else { return 0 }

        let completedDays = Set(results.filter(\.completed).map { Calendar.current.startOfDay(for: $0.date) })
        var currentStreak = 0

        for dayOffset in 0..<365 {
            guard let date = Calendar.current.date(byAdding: .day, value: -dayOffset, to: Date()) else { continue }
            let day = Calendar.current.startOfDay(for: date)
            let hasResult = completedDays.contains(day)

            if hasResult {
                currentStreak += 1
            } else if dayOffset > 0 {
                break
            }
        }

        return currentStreak
    }

    var accuracy: Int {
        serverStats?.accuracy ?? {
            let completed = results.filter(\.completed)
            guard !completed.isEmpty else { return 0 }
            let correct = completed.filter(\.correct).count
            return Int(round(Double(correct) / Double(completed.count) * 100))
        }()
    }

    var userTeam: Team? {
        guard let teamId = profile?.teamId else { return nil }
        return teams.first(where: { $0.id == teamId })
    }

    var sortedTeams: [Team] {
        teams.sorted { $0.totalPoints > $1.totalPoints }
    }

    var allRankedMembers: [RankedMember] {
        teams
            .flatMap { team in
                team.members.map { member in
                    RankedMember(
                        id: "\(team.id)-\(member.id)",
                        name: member.name,
                        avatar: member.avatar,
                        points: member.points,
                        teamName: team.name,
                        teamId: team.id
                    )
                }
            }
            .sorted { $0.points > $1.points }
    }

    func teamRank(for teamId: String) -> Int {
        (sortedTeams.firstIndex(where: { $0.id == teamId }) ?? -1) + 1
    }

    func challenges(for filter: DifficultyFilter) -> [Challenge] {
        let base = filter.asDifficulty.map { difficulty in
            ChallengeData.all.filter { $0.difficulty == difficulty }
        } ?? ChallengeData.all

        guard let age = profile?.age else { return base }
        return ChallengeData.forAge(age, from: base)
    }

    func isChallengeCompleted(_ challengeId: String) -> Bool {
        results.contains { $0.challengeId == challengeId && $0.completed }
    }

    // MARK: - Onboarding / Profile (local + API)

    func saveOnboarding(name: String, age: Int) {
        let avatars = ["👦", "👧", "🧒", "👨", "👩", "🧑"]
        let profile = UserProfile(
            memberId: UUID().uuidString,
            name: name,
            age: age,
            teamId: "team-1",
            avatar: avatars.randomElement() ?? "🧑"
        )

        self.profile = profile
        ensureUserMember(profile)
        save(profile, key: StorageKey.profile)

        // Sync to server in the background
        Task { await syncProfileToServer(profile) }
    }

    func updateProfile(name: String, age: Int) {
        guard var profile else { return }
        profile.name = name
        profile.age = age

        self.profile = profile
        replaceUserMember(profile)
        save(profile, key: StorageKey.profile)

        Task { await syncProfileToServer(profile) }
    }

    // MARK: - Challenge completion (local + API)

    func completeChallenge(_ challenge: Challenge, correct: Bool) {
        let result = ChallengeResult(
            challengeId: challenge.id,
            completed: true,
            correct: correct,
            date: Date(),
            points: correct ? challenge.points : 0
        )
        results.append(result)
        save(results, key: StorageKey.results)

        if correct {
            addPointsToCurrentMember(challenge.points)
        }

        // Send to server
        Task {
            guard let memberId = profile?.memberId else { return }
            do {
                lastError = nil
                let _ = try await api.completeChallenge(
                    challengeId: challenge.id,
                    memberId: memberId,
                    correct: correct)

                // Refresh server stats and teams after completion
                await refreshFromServer()

                // Track the event
                try? await api.trackEvent(
                    userType: "student", userId: memberId,
                    eventType: "challenge_completed",
                    eventData: [
                        "challenge_id": challenge.id,
                        "correct": String(correct),
                        "points": String(correct ? challenge.points : 0)
                    ])
            } catch {
                lastError = error.localizedDescription
            }
        }
    }

    // MARK: - Server sync

    /// Pull latest teams and stats from the backend.
    func refreshFromServer() async {
        do {
            lastError = nil
            let serverTeams = try await api.fetchTeams()
            teams = serverTeams
            save(teams, key: StorageKey.teams)

            if let memberId = profile?.memberId {
                serverStats = try await api.fetchStats(memberId)
            }
        } catch {
            // Non-fatal: we still have local data
            lastError = error.localizedDescription
        }
    }

    /// Called once at app launch to pull the latest cloud data.
    func loadFromServerIfAvailable() async {
        // Try to get profile from server if we have a local memberId
        if let memberId = profile?.memberId {
            do {
                let serverProfile = try await api.fetchProfile(memberId)
                self.profile = serverProfile
                save(serverProfile, key: StorageKey.profile)
            } catch {
                // Server unreachable — keep local profile
            }
        }

        await refreshFromServer()
    }

    // MARK: - Private: API sync helpers

    private func syncProfileToServer(_ profile: UserProfile) async {
        do {
            lastError = nil
            try await api.createProfile(profile)
        } catch {
            lastError = error.localizedDescription
        }
    }

    // MARK: - Private: local persistence

    private func loadLocalState() {
        profile = load(UserProfile.self, key: StorageKey.profile)
        results = load([ChallengeResult].self, key: StorageKey.results) ?? []
        teams = load([Team].self, key: StorageKey.teams) ?? []

        if let profile {
            ensureUserMember(profile)
        }
    }

    private func ensureUserMember(_ profile: UserProfile) {
        guard let teamIndex = teams.firstIndex(where: { $0.id == profile.teamId }) else { return }
        let exists = teams[teamIndex].members.contains(where: { $0.id == profile.memberId })

        if !exists {
            teams[teamIndex].members.append(
                TeamMember(id: profile.memberId, name: profile.name, avatar: profile.avatar, points: 0)
            )
            recalculateTeamTotal(at: teamIndex)
            save(teams, key: StorageKey.teams)
        }
    }

    private func replaceUserMember(_ profile: UserProfile) {
        guard let teamIndex = teams.firstIndex(where: { $0.id == profile.teamId }) else { return }
        guard let memberIndex = teams[teamIndex].members.firstIndex(where: { $0.id == profile.memberId }) else {
            ensureUserMember(profile)
            return
        }

        teams[teamIndex].members[memberIndex].name = profile.name
        teams[teamIndex].members[memberIndex].avatar = profile.avatar
        save(teams, key: StorageKey.teams)
    }

    private func addPointsToCurrentMember(_ points: Int) {
        guard let profile else { return }
        guard let teamIndex = teams.firstIndex(where: { $0.id == profile.teamId }) else { return }
        guard let memberIndex = teams[teamIndex].members.firstIndex(where: { $0.id == profile.memberId }) else { return }

        teams[teamIndex].members[memberIndex].points += points
        recalculateTeamTotal(at: teamIndex)
        save(teams, key: StorageKey.teams)
    }

    private func recalculateTeamTotal(at index: Int) {
        teams[index].totalPoints = teams[index].members.reduce(0) { $0 + $1.points }
    }

    private func load<T: Decodable>(_ type: T.Type, key: String) -> T? {
        guard let data = defaults.data(forKey: key) else { return nil }
        return try? decoder.decode(type, from: data)
    }

    private func save<T: Encodable>(_ value: T, key: String) {
        guard let data = try? encoder.encode(value) else { return }
        defaults.set(data, forKey: key)
    }

    private static let defaultTeams: [Team] = [
        Team(id: "team-1", name: "Code Warriors", members: [
            TeamMember(id: "1", name: "Alex", avatar: "👦", points: 450),
            TeamMember(id: "2", name: "Sam", avatar: "👧", points: 380),
            TeamMember(id: "3", name: "Jordan", avatar: "🧒", points: 420)
        ], totalPoints: 1250),
        Team(id: "team-2", name: "Algorithm Wizards", members: [
            TeamMember(id: "4", name: "Taylor", avatar: "👦", points: 410),
            TeamMember(id: "5", name: "Morgan", avatar: "👧", points: 390),
            TeamMember(id: "6", name: "Casey", avatar: "🧒", points: 380)
        ], totalPoints: 1180),
        Team(id: "team-3", name: "Binary Builders", members: [
            TeamMember(id: "7", name: "Riley", avatar: "👦", points: 360),
            TeamMember(id: "8", name: "Quinn", avatar: "👧", points: 350),
            TeamMember(id: "9", name: "Avery", avatar: "🧒", points: 340)
        ], totalPoints: 1050),
        Team(id: "team-4", name: "Logic Masters", members: [
            TeamMember(id: "10", name: "Jamie", avatar: "👦", points: 320),
            TeamMember(id: "11", name: "Drew", avatar: "👧", points: 310),
            TeamMember(id: "12", name: "Skyler", avatar: "🧒", points: 290)
        ], totalPoints: 920)
    ]
}
