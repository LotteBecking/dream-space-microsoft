import SwiftUI

struct ChallengeView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    let lesson: Lesson

    @State private var selectedIndex: Int? = nil
    @State private var showResult = false

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(lesson.challenge.prompt)
                .font(.headline)

            ForEach(lesson.challenge.choices.indices, id: \.self) { index in
                Button {
                    selectedIndex = index
                    showResult = true
                    if index == lesson.challenge.correctIndex {
                        progressStore.markCompleted(lesson)
                    }
                } label: {
                    HStack {
                        Text(lesson.challenge.choices[index])
                            .frame(maxWidth: .infinity, alignment: .leading)
                        if showResult, selectedIndex == index {
                            Image(systemName: index == lesson.challenge.correctIndex ? "checkmark.circle.fill" : "xmark.circle.fill")
                                .foregroundStyle(index == lesson.challenge.correctIndex ? Theme.accent : .red)
                        }
                    }
                    .padding()
                    .background(Theme.card)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                }
                .buttonStyle(.plain)
            }

            if showResult, let selectedIndex {
                let correct = selectedIndex == lesson.challenge.correctIndex
                Text(correct ? "Nice work!" : "Try again")
                    .font(.headline)
                    .foregroundStyle(correct ? Theme.accent : .orange)
                Text(lesson.challenge.explanation)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
        }
    }
}
