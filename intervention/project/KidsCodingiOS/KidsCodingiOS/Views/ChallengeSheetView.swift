import SwiftUI

struct ChallengeSheetView: View {
    let challenge: Challenge
    let onComplete: (Bool) -> Void

    @Environment(\.dismiss) private var dismiss
    @State private var selectedAnswer: Int?
    @State private var showResult = false
    @State private var isCorrect = false

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    HStack(spacing: 8) {
                        Text(challenge.difficulty.title)
                            .font(.caption.weight(.semibold))
                            .padding(.horizontal, 10)
                            .padding(.vertical, 6)
                            .background(difficultyColor.opacity(0.15), in: Capsule())
                            .foregroundStyle(difficultyColor)

                        Text(challenge.category)
                            .font(.caption.weight(.semibold))
                            .padding(.horizontal, 10)
                            .padding(.vertical, 6)
                            .background(.gray.opacity(0.15), in: Capsule())
                    }

                    Text(challenge.title)
                        .font(.title2.bold())
                    Text(challenge.description)
                        .foregroundStyle(.secondary)

                    VStack(alignment: .leading, spacing: 8) {
                        Text("Question")
                            .font(.headline)
                        Text(challenge.question)
                    }
                    .padding()
                    .background(Color.purple.opacity(0.08), in: RoundedRectangle(cornerRadius: 12))

                    if !showResult {
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Choose your answer")
                                .font(.headline)

                            ForEach(Array(challenge.options.enumerated()), id: \.offset) { index, option in
                                Button {
                                    selectedAnswer = index
                                } label: {
                                    HStack(spacing: 10) {
                                        Image(systemName: selectedAnswer == index ? "largecircle.fill.circle" : "circle")
                                        Text(option)
                                        Spacer()
                                    }
                                    .padding()
                                    .background(
                                        RoundedRectangle(cornerRadius: 12)
                                            .fill(selectedAnswer == index ? Color.purple.opacity(0.15) : Color.gray.opacity(0.08))
                                    )
                                }
                                .buttonStyle(.plain)
                            }
                        }

                        Button("Submit Answer") {
                            guard let selectedAnswer else { return }
                            isCorrect = selectedAnswer == challenge.correctAnswer
                            showResult = true
                        }
                        .buttonStyle(.borderedProminent)
                        .frame(maxWidth: .infinity)
                        .disabled(selectedAnswer == nil)
                    } else {
                        VStack(alignment: .leading, spacing: 12) {
                            Label(isCorrect ? "🎉 Correct!" : "❌ Not quite right", systemImage: isCorrect ? "checkmark.circle.fill" : "xmark.circle.fill")
                                .font(.headline)
                                .foregroundStyle(isCorrect ? Color.green : Color.red)

                            Text(isCorrect ? "Great job! You earned \(challenge.points) points." : "The correct answer was: \(challenge.options[challenge.correctAnswer])")
                                .foregroundStyle(.secondary)
                        }
                        .padding()
                        .background((isCorrect ? Color.green : Color.red).opacity(0.08), in: RoundedRectangle(cornerRadius: 12))

                        VStack(alignment: .leading, spacing: 8) {
                            Label("Explanation", systemImage: "lightbulb.fill")
                                .font(.headline)
                            Text(challenge.explanation)
                        }
                        .padding()
                        .background(Color.blue.opacity(0.08), in: RoundedRectangle(cornerRadius: 12))

                        Button("Continue") {
                            onComplete(isCorrect)
                            dismiss()
                        }
                        .buttonStyle(.borderedProminent)
                    }
                }
                .padding()
            }
            .navigationTitle("Challenge")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }

    private var difficultyColor: Color {
        switch challenge.difficulty {
        case .beginner: return .green
        case .intermediate: return .orange
        case .advanced: return .red
        }
    }
}
