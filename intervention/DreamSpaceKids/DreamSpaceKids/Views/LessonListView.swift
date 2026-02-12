import SwiftUI

struct LevelListView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    private let levels = Level.sampleLevels

    var body: some View {
        NavigationStack {
            ZStack {
                Theme.background.ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 24) {
                        Text("Your Coding Journey")
                            .font(.title.bold())
                            .foregroundColor(Theme.accent)
                            .padding(.top, 20)
                        
                        ForEach(levels.indices, id: \.self) { index in
                            let level = levels[index]
                            let unlocked = progressStore.isLevelUnlocked(level, index: index)
                            let isCompleted = progressStore.isLevelCompleted(level)
                            
                            VStack(spacing: 16) {
                                NavigationLink(value: level) {
                                    LevelCardView(
                                        levelNumber: index + 1,
                                        level: level,
                                        isUnlocked: unlocked,
                                        isCompleted: isCompleted
                                    )
                                }
                                .disabled(!unlocked)
                                
                                // Show storytelling after level 4
                                if index == 3 && isCompleted {
                                    NavigationLink(value: "storytelling-ada") {
                                        StorytellingCardView()
                                    }
                                }
                                
                                // Show second storytelling after level 7
                                if index == 6 && isCompleted {
                                    NavigationLink(value: "storytelling-maya") {
                                        StorytellingCardView(
                                            title: "Meet Another Coding Hero!",
                                            subtitle: "Maya's Amazing Animal App",
                                            emoji: "🏆"
                                        )
                                    }
                                }
                                
                                // Arrow to next level
                                if index < levels.count - 1 {
                                    Image(systemName: "arrow.down")
                                        .font(.system(size: 30, weight: .bold))
                                        .foregroundColor(isCompleted ? Theme.accent : .secondary.opacity(0.3))
                                        .padding(.vertical, 8)
                                }
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.bottom, 40)
                }
            }
            .navigationDestination(for: Level.self) { level in
                LevelDetailView(level: level)
            }
            .navigationDestination(for: String.self) { destination in
                if destination == "storytelling-ada" {
                    StorytellingView(storyType: .ada)
                } else if destination == "storytelling-maya" {
                    StorytellingView(storyType: .maya)
                }
            }
        }
    }
}

struct LevelCardView: View {
    let levelNumber: Int
    let level: Level
    let isUnlocked: Bool
    let isCompleted: Bool
    
    private var cardColor: Color {
        let colors: [Color] = [.blue, .purple, .pink, .orange, .green, .cyan, .indigo]
        return colors[levelNumber % colors.count]
    }
    
    var body: some View {
        HStack(spacing: 20) {
            // Big level number
            ZStack {
                Circle()
                    .fill(isUnlocked ? cardColor.opacity(0.2) : Color.gray.opacity(0.1))
                    .frame(width: 80, height: 80)
                
                if isUnlocked {
                    Text("\(levelNumber)")
                        .font(.system(size: 40, weight: .black))
                        .foregroundColor(cardColor)
                } else {
                    Image(systemName: "lock.fill")
                        .font(.system(size: 30))
                        .foregroundColor(.secondary)
                }
            }
            
            // Level info
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Text(level.title)
                        .font(.title3.bold())
                        .foregroundColor(.primary)
                    
                    if isCompleted {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                            .font(.title3)
                    }
                }
                
                Text(level.summary)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .foregroundColor(isUnlocked ? Theme.accent : .secondary.opacity(0.3))
                .font(.title3)
        }
        .padding(20)
        .background(isUnlocked ? Theme.card : Color.gray.opacity(0.05))
        .cornerRadius(20)
        .overlay(
            RoundedRectangle(cornerRadius: 20)
                .stroke(isCompleted ? cardColor.opacity(0.5) : Color.clear, lineWidth: 3)
        )
        .shadow(color: isUnlocked ? cardColor.opacity(0.2) : Color.clear, radius: 10, y: 5)
    }
}

struct StorytellingCardView: View {
    var title: String = "Meet a Coding Hero!"
    var subtitle: String = "Inspiring story of Ada Lovelace"
    var emoji: String = "📖"
    
    var body: some View {
        HStack(spacing: 16) {
            Text(emoji)
                .font(.system(size: 50))
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                    .foregroundColor(Theme.accent)
                
                Text(subtitle)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .foregroundColor(Theme.accent)
        }
        .padding(20)
        .background(
            LinearGradient(
                colors: [Color.purple.opacity(0.1), Color.pink.opacity(0.1)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .cornerRadius(20)
        .overlay(
            RoundedRectangle(cornerRadius: 20)
                .stroke(Color.purple.opacity(0.3), lineWidth: 2)
        )
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
    @EnvironmentObject private var progressStore: ProgressStore
    @Environment(\.dismiss) private var dismiss
    
    private var levelIndex: Int {
        Level.sampleLevels.firstIndex(where: { $0.id == level.id }) ?? 0
    }
    
    private var nextLevel: Level? {
        let nextIndex = levelIndex + 1
        return nextIndex < Level.sampleLevels.count ? Level.sampleLevels[nextIndex] : nil
    }
    
    private var isLevelCompleted: Bool {
        progressStore.isLevelCompleted(level)
    }

    var body: some View {
        ZStack {
            Theme.background.ignoresSafeArea()
            
            VStack(spacing: 0) {
                List(level.lessons) { lesson in
                    NavigationLink(value: lesson) {
                        HStack {
                            VStack(alignment: .leading, spacing: 6) {
                                Text(lesson.title)
                                    .font(.headline)
                                Text(lesson.summary)
                                    .font(.subheadline)
                                    .foregroundStyle(.secondary)
                            }
                            
                            Spacer()
                            
                            if progressStore.isCompleted(lesson) {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.green)
                            }
                        }
                    }
                }
                .scrollContentBackground(.hidden)
                
                // Next level button
                if isLevelCompleted, let next = nextLevel {
                    NavigationLink(value: next) {
                        HStack {
                            Image(systemName: "arrow.right.circle.fill")
                                .font(.title2)
                            Text("Continue to \(next.title)")
                                .fontWeight(.semibold)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(
                            LinearGradient(
                                colors: [Theme.accent, Theme.highlight],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .foregroundColor(.white)
                        .cornerRadius(16)
                        .shadow(color: Theme.accent.opacity(0.3), radius: 8, y: 4)
                    }
                    .padding()
                    .background(Theme.background)
                }
            }
        }
        .navigationTitle(level.title)
        .navigationBarTitleDisplayMode(.large)
        .navigationDestination(for: Lesson.self) { lesson in
            LessonDetailView(lesson: lesson)
        }
        .navigationDestination(for: Level.self) { nextLevel in
            LevelDetailView(level: nextLevel)
        }
    }
}
