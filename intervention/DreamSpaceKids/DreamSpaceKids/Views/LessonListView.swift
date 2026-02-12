import SwiftUI

struct LevelListView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    private let levels = Level.sampleLevels

    var body: some View {
        NavigationStack {
            List(levels.indices, id: \.self) { index in
                let level = levels[index]
                let unlocked = progressStore.isLevelUnlocked(level, index: index)
                NavigationLink(value: level) {
                    HStack {
                        VStack(alignment: .leading, spacing: 6) {
                            Text(level.title)
                                .font(.headline)
                            Text(level.summary)
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        if progressStore.isLevelCompleted(level) {
                            CompletedBadgeView(label: "Done")
                        } else {
                            CompletedBadgeView(label: unlocked ? "New" : "Locked")
                        }
                    }
                }
                .disabled(!unlocked)
            }
            .navigationTitle("DreamSpace Levels")
            .navigationDestination(for: Level.self) { level in
                LevelDetailView(level: level)
            }
        }
        .background(Theme.background.ignoresSafeArea())
    }
}

struct CompletedBadgeView: View {
    let label: String

    var body: some View {
        let isDone = label == "Done"
        let isLocked = label == "Locked"
        Text(label)
            .font(.caption2)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(isDone ? Color.green.opacity(0.2) : Theme.card)
            .clipShape(Capsule())
            .foregroundStyle(isLocked ? .secondary : (isDone ? .green : Theme.accent))
    }
}

struct LevelDetailView: View {
    let level: Level

    var body: some View {
        List(level.lessons) { lesson in
            NavigationLink(value: lesson) {
                VStack(alignment: .leading, spacing: 6) {
                    Text(lesson.title)
                        .font(.headline)
                    Text(lesson.summary)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
            }
        }
        .navigationTitle(level.title)
        .navigationDestination(for: Lesson.self) { lesson in
            LessonDetailView(lesson: lesson)
        }
    }
}
