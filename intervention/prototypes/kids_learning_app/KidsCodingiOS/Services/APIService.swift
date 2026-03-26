import Foundation

/// Lightweight HTTP client that talks to the DreamSpace Flask backend.
/// All methods are async and decode JSON responses into the app's existing model types.
actor APIService {
    static let shared = APIService()

    /// Base URL for the backend.  Change this to your deployed URL when hosting.
    /// For local Xcode Simulator → Mac the default ``http://127.0.0.1:5000`` works.
    /// For a real device on the same Wi-Fi, use your Mac's local IP (e.g. ``http://192.168.1.42:5000``).
    private let baseURL: URL

    private let encoder: JSONEncoder = {
        let e = JSONEncoder()
        e.keyEncodingStrategy = .convertToSnakeCase
        return e
    }()

    private let decoder: JSONDecoder = {
        let d = JSONDecoder()
        d.keyDecodingStrategy = .convertFromSnakeCase
        return d
    }()

    init(baseURL: URL = URL(string: "http://127.0.0.1:5000")!) {
        self.baseURL = baseURL
    }

    // MARK: - Profile

    func createProfile(_ profile: UserProfile) async throws {
        struct Body: Encodable {
            let memberId: String
            let name: String
            let age: Int
            let teamId: String
            let avatar: String
        }
        let body = Body(memberId: profile.memberId, name: profile.name,
                        age: profile.age, teamId: profile.teamId,
                        avatar: profile.avatar)
        let _: SuccessResponse = try await post("/api/kids/profile", body: body)
    }

    func fetchProfile(_ memberId: String) async throws -> UserProfile {
        try await get("/api/kids/profile/\(memberId)")
    }

    func updateProfile(_ profile: UserProfile) async throws {
        struct Body: Encodable {
            let name: String
            let age: Int
        }
        let body = Body(name: profile.name, age: profile.age)
        let _: SuccessResponse = try await put(
            "/api/kids/profile/\(profile.memberId)", body: body)
    }

    // MARK: - Stats

    struct UserStats: Decodable {
        let totalPoints: Int
        let completed: Int
        let correct: Int
        let accuracy: Int
        let streak: Int
    }

    func fetchStats(_ memberId: String) async throws -> UserStats {
        try await get("/api/kids/profile/\(memberId)/stats")
    }

    // MARK: - Challenges

    func fetchChallenges(difficulty: String? = nil, age: Int? = nil) async throws -> [Challenge] {
        var params: [String] = []
        if let d = difficulty { params.append("difficulty=\(d)") }
        if let a = age { params.append("age=\(a)") }
        let qs = params.isEmpty ? "" : "?\(params.joined(separator: "&"))"
        return try await get("/api/kids/challenges\(qs)")
    }

    func fetchDailyChallenge(date: String? = nil) async throws -> Challenge {
        let qs = date.map { "?date=\($0)" } ?? ""
        return try await get("/api/kids/challenges/daily\(qs)")
    }

    struct CompletionResponse: Decodable {
        let success: Bool
        let resultId: String
        let correct: Bool
        let pointsAwarded: Int
    }

    func completeChallenge(challengeId: String, memberId: String,
                           correct: Bool) async throws -> CompletionResponse {
        struct Body: Encodable {
            let memberId: String
            let correct: Bool
        }
        return try await post(
            "/api/kids/challenges/\(challengeId)/complete",
            body: Body(memberId: memberId, correct: correct))
    }

    // MARK: - Results

    struct APIResult: Decodable {
        let id: String
        let challengeId: String
        let completed: Bool
        let correct: Bool
        let points: Int
        let date: String
    }

    func fetchResults(_ memberId: String) async throws -> [APIResult] {
        try await get("/api/kids/results/\(memberId)")
    }

    // MARK: - Teams

    func fetchTeams() async throws -> [Team] {
        try await get("/api/kids/teams")
    }

    func fetchTeam(_ teamId: String) async throws -> Team {
        try await get("/api/kids/teams/\(teamId)")
    }

    struct TeamRank: Decodable {
        let id: String
        let name: String
        let totalPoints: Int
    }

    func fetchTeamRankings() async throws -> [TeamRank] {
        try await get("/api/kids/teams/rankings")
    }

    func fetchMemberRankings() async throws -> [RankedMember] {
        try await get("/api/kids/members/rankings")
    }

    // MARK: - Tracking

    func trackEvent(userType: String, userId: String,
                    eventType: String, eventData: [String: String] = [:],
                    sessionId: String? = nil) async throws {
        struct Body: Encodable {
            let userType: String
            let userId: String
            let eventType: String
            let eventData: [String: String]
            let sessionId: String?
        }
        let _: SuccessResponse = try await post(
            "/api/tracking/event",
            body: Body(userType: userType, userId: userId,
                       eventType: eventType, eventData: eventData,
                       sessionId: sessionId))
    }

    // MARK: - HTTP helpers

    private struct SuccessResponse: Decodable {
        let success: Bool
    }

    private func get<T: Decodable>(_ path: String) async throws -> T {
        let url = baseURL.appendingPathComponent(path)
        let (data, response) = try await URLSession.shared.data(from: url)
        try validateResponse(response)
        return try decoder.decode(T.self, from: data)
    }

    private func post<T: Decodable, B: Encodable>(_ path: String,
                                                     body: B) async throws -> T {
        try await request(path, method: "POST", body: body)
    }

    private func put<T: Decodable, B: Encodable>(_ path: String,
                                                    body: B) async throws -> T {
        try await request(path, method: "PUT", body: body)
    }

    private func request<T: Decodable, B: Encodable>(
        _ path: String, method: String, body: B
    ) async throws -> T {
        let url = baseURL.appendingPathComponent(path)
        var req = URLRequest(url: url)
        req.httpMethod = method
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try encoder.encode(body)
        let (data, response) = try await URLSession.shared.data(for: req)
        try validateResponse(response)
        return try decoder.decode(T.self, from: data)
    }

    private func validateResponse(_ response: URLResponse) throws {
        guard let http = response as? HTTPURLResponse,
              (200...299).contains(http.statusCode) else {
            let code = (response as? HTTPURLResponse)?.statusCode ?? -1
            throw APIError.httpError(statusCode: code)
        }
    }
}

enum APIError: LocalizedError {
    case httpError(statusCode: Int)

    var errorDescription: String? {
        switch self {
        case .httpError(let code):
            return "Server returned status \(code)"
        }
    }
}
