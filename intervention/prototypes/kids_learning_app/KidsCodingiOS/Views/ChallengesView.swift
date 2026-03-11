import SwiftUI

struct ChallengesView: View {
    @EnvironmentObject private var store: AppStore

    @State private var filter: DifficultyFilter = .all
    @State private var selectedChallenge: Challenge?

    private var challenges: [Challenge] {
        store.challenges(for: filter)
    }

    var body: some View {
        List {
            Section {
                statsRow
            }
            .listRowBackground(Color.clear)

            Section("Difficulty") {
                Picker("Filter", selection: $filter) {
                    ForEach(DifficultyFilter.allCases) { value in
                        Text(value.title).tag(value)
                    }
                }
                .pickerStyle(.segmented)
            }

            Section("Challenges") {
                if challenges.isEmpty {
                    ContentUnavailableView("No challenges found", systemImage: "target", description: Text("Try another difficulty level."))
                }

                ForEach(challenges) { challenge in
                    challengeRow(challenge)
                }
            }
        }
        .navigationTitle("Challenge Library")
        .sheet(item: $selectedChallenge) { challenge in
            ChallengeSheetView(challenge: challenge) { correct in
                store.completeChallenge(challenge, correct: correct)
            }
        }
    }

    private var statsRow: some View {
        HStack(spacing: 10) {
            statCard("Total", "\(challenges.count)", "target", .purple)
            statCard("Completed", "\(store.results.count)", "trophy.fill", .green)
            let percentage = challenges.isEmpty ? 0 : Int((Double(store.results.count) / Double(challenges.count)) * 100)
            statCard("Progress", "\(percentage)%", "line.3.horizontal.decrease.circle", .blue)
        }
    }

    private func statCard(_ title: String, _ value: String, _ icon: String, _ color: Color) -> some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .foregroundStyle(color)
            Text(value).font(.headline)
            Text(title).font(.caption).foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(8)
        .background(Color(uiColor: .secondarySystemBackground), in: RoundedRectangle(cornerRadius: 10))
    }

    private func challengeRow(_ challenge: Challenge) -> some View {
        let completed = store.isChallengeCompleted(challenge.id)

        return VStack(alignment: .leading, spacing: 10) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 6) {
                    HStack {
                        Text(challenge.difficulty.title)
                            .font(.caption2.weight(.semibold))
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(difficultyColor(challenge.difficulty).opacity(0.15), in: Capsule())
                            .foregroundStyle(difficultyColor(challenge.difficulty))

                        if completed {
                            Text("✓ Done")
                                .font(.caption2.weight(.semibold))
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.green.opacity(0.15), in: Capsule())
                                .foregroundStyle(.green)
                        }
                    }

                    Text(challenge.title).font(.headline)
                    Text(challenge.description).font(.subheadline).foregroundStyle(.secondary)
                }

                Spacer()
                Text(ChallengeData.categoryEmoji(challenge.category))
                    .font(.title2)
            }

            HStack {
                Text("🎯 \(challenge.category)")
                Text("⭐ \(challenge.points) pts")
                Spacer()

                Button(completed ? "Retry" : "Start") {
                    selectedChallenge = challenge
                }
                .buttonStyle(.borderedProminent)
                .tint(completed ? .gray : .purple)
            }
            .font(.caption)
            .foregroundStyle(.secondary)
        }
        .padding(.vertical, 4)
    }

    private func difficultyColor(_ difficulty: DifficultyLevel) -> Color {
        switch difficulty {
        case .beginner: return .green
        case .intermediate: return .orange
        case .advanced: return .red
        }
    }
}
