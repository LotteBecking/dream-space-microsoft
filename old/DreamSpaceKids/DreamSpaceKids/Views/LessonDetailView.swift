import SwiftUI

struct LessonDetailView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    let lesson: Lesson

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text(lesson.title)
                    .font(.largeTitle.bold())
                Text(lesson.concept)
                    .font(.body)
                CodeCardView(code: lesson.example)
                ChallengeCardView(lesson: lesson)
                if progressStore.isCompleted(lesson) {
                    Text("Great job! You completed this lesson.")
                        .font(.headline)
                        .foregroundStyle(Theme.accent)
                }
            }
            .padding()
        }
        .navigationTitle(lesson.title)
        .background(Theme.background.ignoresSafeArea())
    }
}

struct CodeCardView: View {
    let code: String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Example")
                .font(.headline)
            Text(code)
                .font(.system(.body, design: .monospaced))
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Theme.card)
                .clipShape(RoundedRectangle(cornerRadius: 12))
        }
    }
}

struct ChallengeCardView: View {
    let lesson: Lesson

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Mini Challenge")
                .font(.headline)
            ChallengeView(lesson: lesson)
        }
    }
}
