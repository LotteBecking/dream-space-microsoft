import SwiftUI

struct ProgressDashboardView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    private let lessons = Level.allLessons

    var body: some View {
        VStack(spacing: 16) {
            Text("Your Progress")
                .font(.largeTitle.bold())
            ProgressSummaryView(completedCount: progressStore.completedLessons.count, totalCount: lessons.count)
            BadgeGridView(completedLessons: progressStore.completedLessons)
            Button("Reset Progress") {
                progressStore.resetProgress()
            }
            .buttonStyle(.borderedProminent)
            .tint(Theme.accent)
        }
        .padding()
        .background(Theme.background.ignoresSafeArea())
    }
}

struct ProgressSummaryView: View {
    let completedCount: Int
    let totalCount: Int

    var body: some View {
        VStack(spacing: 8) {
            Text("Lessons completed")
                .font(.headline)
            Text("\(completedCount) of \(totalCount)")
                .font(.title2.bold())
            ProgressView(value: Double(completedCount), total: Double(max(totalCount, 1)))
        }
    }
}

struct BadgeGridView: View {
    let completedLessons: Set<String>

    var body: some View {
        LazyVGrid(columns: [GridItem(.adaptive(minimum: 120))], spacing: 12) {
            ForEach(Level.allLessons) { lesson in
                BadgeView(title: lesson.title, isEarned: completedLessons.contains(lesson.id))
            }
        }
    }
}
