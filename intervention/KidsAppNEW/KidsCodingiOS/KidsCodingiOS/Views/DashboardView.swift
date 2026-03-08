import SwiftUI

struct DashboardView: View {
    @EnvironmentObject private var store: AppStore
    @Binding var selectedTab: AppTab

    @State private var activeChallenge: Challenge?

    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                welcomeCard
                dailyChallengeCard
                teamCard
                quickActionsCard
            }
            .padding()
        }
        .navigationTitle("CodeQuest")
        .sheet(item: $activeChallenge) { challenge in
            ChallengeSheetView(challenge: challenge) { correct in
                store.completeChallenge(challenge, correct: correct)
            }
        }
    }

    private var welcomeCard: some View {
        let profile = store.profile
        let rank = store.profile.map { store.teamRank(for: $0.teamId) } ?? 0

        return VStack(alignment: .leading, spacing: 14) {
            Text("Welcome back, \(profile?.name ?? "Coder")! \(profile?.avatar ?? "🧑")")
                .font(.title3.bold())
            Text("Ready to tackle today's coding challenge?")
                .foregroundStyle(.white.opacity(0.9))

            HStack(spacing: 12) {
                statChip(title: "Streak", value: "\(store.streak) days", icon: "flame.fill")
                statChip(title: "Points", value: "\(store.totalPoints)", icon: "trophy.fill")
                statChip(title: "Team Rank", value: "#\(rank)", icon: "person.3.fill")
            }
        }
        .foregroundStyle(.white)
        .padding()
        .background(
            LinearGradient(colors: [.purple, .pink, .orange], startPoint: .topLeading, endPoint: .bottomTrailing),
            in: RoundedRectangle(cornerRadius: 16)
        )
    }

    private func statChip(title: String, value: String, icon: String) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Label(title, systemImage: icon)
                .font(.caption)
            Text(value)
                .font(.headline)
        }
        .padding(10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.white.opacity(0.18), in: RoundedRectangle(cornerRadius: 12))
    }

    private var dailyChallengeCard: some View {
        let challenge = store.todayChallenge
        let completed = store.todayResult?.completed == true

        return GroupBox {
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Text("🎯")
                        .font(.largeTitle)
                    VStack(alignment: .leading) {
                        Text(challenge.title).font(.headline)
                        Text(challenge.description).font(.subheadline).foregroundStyle(.secondary)
                    }
                    Spacer()
                    Text(challenge.difficulty.title)
                        .font(.caption.weight(.semibold))
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(.purple.opacity(0.14), in: Capsule())
                }

                HStack {
                    Text("\(challenge.category)")
                    Spacer()
                    Text("⭐ \(challenge.points) pts")
                }
                .font(.caption)
                .foregroundStyle(.secondary)

                if completed {
                    Label("Challenge complete! Come back tomorrow.", systemImage: "checkmark.circle.fill")
                        .font(.subheadline)
                        .foregroundStyle(.green)
                } else {
                    Button("Start Challenge") {
                        activeChallenge = challenge
                    }
                    .buttonStyle(.borderedProminent)
                    .frame(maxWidth: .infinity)
                }
            }
        } label: {
            Label("Today's Challenge", systemImage: "calendar")
                .font(.headline)
        }
    }

    private var teamCard: some View {
        GroupBox {
            if let userTeam = store.userTeam {
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Text("Your Team: \(userTeam.name)")
                            .font(.headline)
                        Spacer()
                        Text("\(userTeam.totalPoints) pts")
                            .font(.subheadline.weight(.semibold))
                    }

                    SwiftUI.ProgressView(value: Double(userTeam.totalPoints), total: 2000)

                    ForEach(userTeam.members.prefix(4)) { member in
                        HStack {
                            Text(member.avatar)
                            Text(member.name)
                            Spacer()
                            Text("\(member.points) pts")
                                .foregroundStyle(.purple)
                        }
                        .font(.subheadline)
                    }
                }
            } else {
                Text("Join a team during onboarding to see team stats.")
                    .foregroundStyle(.secondary)
            }
        }
    }

    private var quickActionsCard: some View {
        GroupBox("Quick Actions") {
            VStack(spacing: 10) {
                Button("Browse All Challenges") { selectedTab = .challenges }
                    .buttonStyle(.bordered)
                    .frame(maxWidth: .infinity)
                Button("View Your Progress") { selectedTab = .progress }
                    .buttonStyle(.bordered)
                    .frame(maxWidth: .infinity)
                Button("Team Competition") { selectedTab = .teams }
                    .buttonStyle(.bordered)
                    .frame(maxWidth: .infinity)
            }
        }
    }
}
