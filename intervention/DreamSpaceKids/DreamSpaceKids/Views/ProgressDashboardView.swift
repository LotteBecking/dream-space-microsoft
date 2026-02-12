import SwiftUI

struct ProgressDashboardView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    private let lessons = Level.allLessons
    @State private var isChatbotPresented = false

    var body: some View {
        VStack(spacing: 16) {
            HStack {
                Spacer()
                Button {
                    isChatbotPresented = true
                } label: {
                    Label("Ask A Buddy", systemImage: "message.fill")
                }
                .buttonStyle(.bordered)
                .tint(Theme.accent)
            }
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
        .sheet(isPresented: $isChatbotPresented) {
            ChatbotPopupView()
        }
    }
}

struct ChatbotPopupView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var message = ""

    var body: some View {
        NavigationView {
            VStack(spacing: 16) {
                VStack(spacing: 8) {
                    Text("Hi! I am your Buddy.")
                        .font(.title2.bold())
                    Text("Ask a question and I will guide you to the right place.")
                        .font(.subheadline)
                        .multilineTextAlignment(.center)
                        .foregroundStyle(.secondary)
                }

                ScrollView {
                    VStack(spacing: 12) {
                        ChatbotBubble(text: "Try: I don't understand strings, can you explain?", isUser: false)
                        ChatbotBubble(text: "Try: What is my next lesson?", isUser: false)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                }

                HStack(spacing: 12) {
                    TextField("Type your question...", text: $message)
                        .textFieldStyle(.roundedBorder)
                    Button("Send") {
                        message = ""
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(Theme.accent)
                }
            }
            .padding()
            .navigationTitle("Ask Buddy")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Close") {
                        dismiss()
                    }
                }
            }
            .background(Theme.background.ignoresSafeArea())
        }
    }
}

struct ChatbotBubble: View {
    let text: String
    let isUser: Bool

    var body: some View {
        HStack {
            if isUser {
                Spacer()
            }

            Text(text)
                .padding(12)
                .background(isUser ? Theme.accent.opacity(0.2) : Theme.card.opacity(0.7))
                .foregroundStyle(.primary)
                .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))

            if !isUser {
                Spacer()
            }
        }
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
