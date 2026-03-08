import SwiftUI

struct ProgressView: View {
    @EnvironmentObject private var store: AppStore

    private var completedCount: Int {
        store.results.filter(\.completed).count
    }

    private var correctCount: Int {
        store.results.filter(\.correct).count
    }

    private var accuracy: Int {
        guard completedCount > 0 else { return 0 }
        return Int((Double(correctCount) / Double(completedCount)) * 100)
    }

    private var categoryStats: [(String, total: Int, correct: Int)] {
        let grouped = Dictionary(grouping: store.results, by: { result in
            ChallengeData.challenge(by: result.challengeId)?.category ?? "Other"
        })

        return grouped.keys.sorted().map { key in
            let values = grouped[key] ?? []
            return (key, values.count, values.filter(\.correct).count)
        }
    }

    private var weeklyPoints: [Int] {
        var values = Array(repeating: 0, count: 7)
        for result in store.results where result.correct {
            let dayDiff = Calendar.current.dateComponents([.day], from: result.date, to: Date()).day ?? 0
            if (0..<7).contains(dayDiff) {
                values[6 - dayDiff] += result.points
            }
        }
        return values
    }

    private var achievements: [(title: String, description: String, icon: String, unlocked: Bool)] {
        [
            ("First Steps", "Complete your first challenge", "🎯", !store.results.isEmpty),
            ("3-Day Streak", "Complete challenges 3 days in a row", "🔥", store.streak >= 3),
            ("Week Warrior", "Maintain a 7-day streak", "⭐", store.streak >= 7),
            ("Century Club", "Earn 100 points", "💯", store.totalPoints >= 100),
            ("Perfect Score", "Get 5 challenges correct in a row", "🏆", accuracy == 100 && store.results.count >= 5),
            ("Challenge Master", "Complete 10 challenges", "🎓", completedCount >= 10)
        ]
    }

    var body: some View {
        List {
            Section {
                HStack(spacing: 10) {
                    statCard("Points", "\(store.totalPoints)", "trophy.fill", .yellow)
                    statCard("Streak", "\(store.streak)", "flame.fill", .orange)
                    statCard("Accuracy", "\(accuracy)%", "target", .green)
                    statCard("Completed", "\(completedCount)", "calendar", .purple)
                }
            }
            .listRowBackground(Color.clear)

            Section("Weekly Activity") {
                VStack(alignment: .leading, spacing: 10) {
                    let maxPoints = max(weeklyPoints.max() ?? 1, 1)
                    HStack(alignment: .bottom, spacing: 8) {
                        ForEach(0..<7, id: \.self) { index in
                            VStack {
                                Spacer(minLength: 0)
                                RoundedRectangle(cornerRadius: 6)
                                    .fill(LinearGradient(colors: [.purple, .pink], startPoint: .bottom, endPoint: .top))
                                    .frame(height: max(weeklyPoints[index] == 0 ? 4 : CGFloat(weeklyPoints[index]) / CGFloat(maxPoints) * 90, 4))
                                Text(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][index])
                                    .font(.caption2)
                                    .foregroundStyle(.secondary)
                            }
                            .frame(maxWidth: .infinity)
                        }
                    }
                    .frame(height: 120)
                }
                .padding(.vertical, 6)
            }

            Section("Category Performance") {
                if categoryStats.isEmpty {
                    Text("Complete challenges to see your category performance.")
                        .foregroundStyle(.secondary)
                } else {
                    ForEach(categoryStats, id: \.0) { item in
                        VStack(alignment: .leading, spacing: 6) {
                            HStack {
                                Text(item.0)
                                Spacer()
                                let pct = item.total > 0 ? Int((Double(item.correct) / Double(item.total)) * 100) : 0
                                Text("\(item.correct)/\(item.total) (\(pct)%)")
                                    .foregroundStyle(.secondary)
                            }
                            SwiftUI.ProgressView(value: Double(item.correct), total: Double(max(item.total, 1)))
                        }
                        .padding(.vertical, 2)
                    }
                }
            }

            Section("Achievements") {
                ForEach(achievements, id: \.title) { achievement in
                    HStack(alignment: .top, spacing: 12) {
                        Text(achievement.icon).font(.title3)
                        VStack(alignment: .leading, spacing: 4) {
                            Text(achievement.title).font(.headline)
                            Text(achievement.description).font(.caption).foregroundStyle(.secondary)
                        }
                        Spacer()
                        if achievement.unlocked {
                            Text("Unlocked")
                                .font(.caption2.weight(.semibold))
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.yellow.opacity(0.2), in: Capsule())
                        }
                    }
                    .opacity(achievement.unlocked ? 1 : 0.6)
                }
            }
        }
        .navigationTitle("Your Progress")
    }

    private func statCard(_ title: String, _ value: String, _ icon: String, _ color: Color) -> some View {
        VStack(spacing: 5) {
            Image(systemName: icon)
                .foregroundStyle(color)
            Text(value).font(.headline)
            Text(title).font(.caption2).foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(8)
        .background(Color(uiColor: .secondarySystemBackground), in: RoundedRectangle(cornerRadius: 10))
    }
}
