import SwiftUI

enum StoryType {
    case ada
    case maya
}

struct StorytellingView: View {
    let storyType: StoryType
    @State private var currentPage = 0
    
    private var story: [StoryPage] {
        switch storyType {
        case .ada:
            return adaStory
        case .maya:
            return mayaStory
        }
    }
    
    private var nextLevelIndex: Int? {
        switch storyType {
        case .ada:
            return 4 // Level 5
        case .maya:
            return nil // No next level after Maya's story
        }
    }
    
    private let adaStory = [
        StoryPage(
            emoji: "👩‍💻",
            title: "Meet Ada Lovelace",
            text: "Long ago, in 1815, a girl named Ada was born in London. She loved math and dreamed of using machines to solve problems!",
            backgroundColor: Color.purple
        ),
        StoryPage(
            emoji: "✨",
            title: "The First Programmer",
            text: "Ada worked with a machine called the Analytical Engine. She wrote the very first computer program ever - before computers even existed!",
            backgroundColor: Color.blue
        ),
        StoryPage(
            emoji: "🚀",
            title: "Ada's Big Idea",
            text: "Ada imagined that machines could do more than just math - they could create music, art, and so much more! She was right!",
            backgroundColor: Color.pink
        ),
        StoryPage(
            emoji: "💡",
            title: "Your Turn!",
            text: "Just like Ada, you can use code to create amazing things! Keep learning, keep dreaming, and who knows what you'll build!",
            backgroundColor: Color.orange
        )
    ]
    
    private let mayaStory = [
        StoryPage(
            emoji: "👧🏻",
            title: "Meet Maya",
            text: "Maya is 12 years old and LOVES animals! She wanted to help people learn about endangered species, so she decided to build an app.",
            backgroundColor: Color.green
        ),
        StoryPage(
            emoji: "📱",
            title: "Building the App",
            text: "Maya learned to code and built 'Animal Heroes' - an app with fun facts, photos, and ways to help endangered animals. It took many tries, but she never gave up!",
            backgroundColor: Color.blue
        ),
        StoryPage(
            emoji: "🏆",
            title: "Winning Awards",
            text: "Maya's app won awards at her school, then her city, and even a national young developer competition! Thousands of kids now use her app to learn about animals.",
            backgroundColor: Color.orange
        ),
        StoryPage(
            emoji: "✨",
            title: "You Can Too!",
            text: "Maya started just like you - learning the basics of coding. Now she's making a real difference! What amazing app will YOU create?",
            backgroundColor: Color.purple
        )
    ]
    
    var body: some View {
        ZStack {
            story[currentPage].backgroundColor.opacity(0.2)
                .ignoresSafeArea()
            
            VStack(spacing: 30) {
                Spacer()
                
                // Emoji
                Text(story[currentPage].emoji)
                    .font(.system(size: 100))
                    .transition(.scale.combined(with: .opacity))
                
                // Title
                Text(story[currentPage].title)
                    .font(.largeTitle.bold())
                    .foregroundColor(story[currentPage].backgroundColor)
                    .multilineTextAlignment(.center)
                    .transition(.slide)
                
                // Story text
                Text(story[currentPage].text)
                    .font(.title3)
                    .foregroundColor(.primary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal, 30)
                    .lineSpacing(8)
                    .transition(.opacity)
                
                Spacer()
                
                // Page indicator
                HStack(spacing: 8) {
                    ForEach(0..<story.count, id: \.self) { index in
                        Circle()
                            .fill(index == currentPage ? story[currentPage].backgroundColor : Color.gray.opacity(0.3))
                            .frame(width: 10, height: 10)
                    }
                }
                .padding(.bottom, 20)
                
                // Navigation buttons
                HStack(spacing: 20) {
                    if currentPage > 0 {
                        Button(action: {
                            withAnimation(.spring()) {
                                currentPage -= 1
                            }
                        }) {
                            HStack {
                                Image(systemName: "arrow.left")
                                Text("Back")
                            }
                            .fontWeight(.semibold)
                            .padding(.horizontal, 30)
                            .padding(.vertical, 15)
                            .background(Color.gray.opacity(0.2))
                            .foregroundColor(.primary)
                            .cornerRadius(25)
                        }
                    }
                    
                    Spacer()
                    
                    if currentPage < story.count - 1 {
                        Button(action: {
                            withAnimation(.spring()) {
                                currentPage += 1
                            }
                        }) {
                            HStack {
                                Text("Next")
                                Image(systemName: "arrow.right")
                            }
                            .fontWeight(.semibold)
                            .padding(.horizontal, 30)
                            .padding(.vertical, 15)
                            .background(story[currentPage].backgroundColor)
                            .foregroundColor(.white)
                            .cornerRadius(25)
                            .shadow(color: story[currentPage].backgroundColor.opacity(0.3), radius: 8, y: 4)
                        }
                    } else {
                        if let nextIndex = nextLevelIndex {
                            NavigationLink(value: Level.sampleLevels[nextIndex]) {
                                HStack {
                                    Text("Start Level \(nextIndex + 1)")
                                    Image(systemName: "star.fill")
                                }
                                .fontWeight(.semibold)
                                .padding(.horizontal, 30)
                                .padding(.vertical, 15)
                                .background(
                                    LinearGradient(
                                        colors: [Color.purple, Color.pink],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    )
                                )
                                .foregroundColor(.white)
                                .cornerRadius(25)
                                .shadow(color: Color.purple.opacity(0.3), radius: 8, y: 4)
                            }
                        } else {
                            Button(action: {
                                // Go back to level list
                            }) {
                                HStack {
                                    Text("Keep Coding!")
                                    Image(systemName: "sparkles")
                                }
                                .fontWeight(.semibold)
                                .padding(.horizontal, 30)
                                .padding(.vertical, 15)
                                .background(
                                    LinearGradient(
                                        colors: [Color.green, Color.blue],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    )
                                )
                                .foregroundColor(.white)
                                .cornerRadius(25)
                                .shadow(color: Color.green.opacity(0.3), radius: 8, y: 4)
                            }
                        }
                    }
                }
                .padding(.horizontal, 30)
                .padding(.bottom, 40)
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .navigationDestination(for: Level.self) { level in
            LevelDetailView(level: level)
        }
    }
}

struct StoryPage {
    let emoji: String
    let title: String
    let text: String
    let backgroundColor: Color
}

#Preview {
    NavigationStack {
        StorytellingView(storyType: .ada)
    }
}
