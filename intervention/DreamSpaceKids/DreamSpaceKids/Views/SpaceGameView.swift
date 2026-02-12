import SwiftUI

struct SpaceGameView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    @StateObject private var game = SpaceGame()
    
    var body: some View {
        NavigationStack {
            ZStack {
                // Space background
                LinearGradient(
                    colors: [Color.black, Color.purple.opacity(0.3), Color.blue.opacity(0.3)],
                    startPoint: .top,
                    endPoint: .bottom
                )
                .ignoresSafeArea()
                
                // Stars background
                ForEach(0..<20, id: \.self) { _ in
                    Circle()
                        .fill(Color.white.opacity(0.3))
                        .frame(width: 2, height: 2)
                        .position(
                            x: CGFloat.random(in: 0...400),
                            y: CGFloat.random(in: 0...800)
                        )
                }
                
                if game.gameState == .playing {
                    GamePlayView(game: game)
                } else if game.gameState == .menu {
                    MenuView(game: game)
                } else {
                    GameOverView(game: game)
                }
            }
            .navigationTitle("Space Coder!")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

struct MenuView: View {
    @ObservedObject var game: SpaceGame
    
    var body: some View {
        VStack(spacing: 30) {
            Text("🚀")
                .font(.system(size: 100))
            
            Text("Space Coder")
                .font(.largeTitle.bold())
                .foregroundColor(.white)
            
            Text("Fly through space and learn coding!")
                .font(.headline)
                .foregroundColor(.white.opacity(0.8))
                .multilineTextAlignment(.center)
            
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Text("⭐️")
                        .font(.title)
                    Text("Collect stars for points")
                        .foregroundColor(.white)
                }
                
                HStack {
                    Text("💣")
                        .font(.title)
                    Text("Avoid bombs!")
                        .foregroundColor(.white)
                }
                
                HStack {
                    Text("📚")
                        .font(.title)
                    Text("Learn coding facts")
                        .foregroundColor(.white)
                }
            }
            .padding()
            .background(Color.white.opacity(0.1))
            .cornerRadius(20)
            
            Button(action: {
                game.startGame()
            }) {
                Text("Start Adventure!")
                    .font(.title2.bold())
                    .foregroundColor(.white)
                    .padding(.horizontal, 40)
                    .padding(.vertical, 16)
                    .background(
                        LinearGradient(
                            colors: [Color.green, Color.blue],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .cornerRadius(30)
                    .shadow(color: Color.green.opacity(0.5), radius: 20)
            }
        }
        .padding()
    }
}

struct GamePlayView: View {
    @ObservedObject var game: SpaceGame
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Collectibles and bombs
                ForEach(game.items) { item in
                    Text(item.emoji)
                        .font(.system(size: 40))
                        .position(item.position)
                }
                
                // Player spaceship
                Text("🚀")
                    .font(.system(size: 50))
                    .rotationEffect(.degrees(-90))
                    .position(game.playerPosition)
                    .gesture(
                        DragGesture()
                            .onChanged { value in
                                game.movePlayer(to: value.location, in: geometry.size)
                            }
                    )
                
                // HUD
                VStack {
                    HStack {
                        // Score
                        HStack(spacing: 8) {
                            Text("⭐️")
                                .font(.title2)
                            Text("\(game.score)")
                                .font(.title2.bold())
                                .foregroundColor(.white)
                        }
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(Color.black.opacity(0.5))
                        .cornerRadius(20)
                        
                        Spacer()
                        
                        // Lives
                        HStack(spacing: 4) {
                            ForEach(0..<game.lives, id: \.self) { _ in
                                Text("❤️")
                                    .font(.title3)
                            }
                        }
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(Color.black.opacity(0.5))
                        .cornerRadius(20)
                    }
                    .padding()
                    
                    Spacer()
                    
                    // Coding fact banner
                    if let fact = game.currentFact {
                        Text(fact)
                            .font(.headline)
                            .foregroundColor(.white)
                            .multilineTextAlignment(.center)
                            .padding()
                            .background(
                                LinearGradient(
                                    colors: [Color.purple.opacity(0.8), Color.blue.opacity(0.8)],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(16)
                            .padding(.horizontal)
                            .transition(.move(edge: .bottom).combined(with: .opacity))
                    }
                    
                    Spacer()
                        .frame(height: 20)
                }
            }
            .onAppear {
                game.screenSize = geometry.size
            }
        }
    }
}

struct GameOverView: View {
    @ObservedObject var game: SpaceGame
    @EnvironmentObject private var progressStore: ProgressStore
    
    var body: some View {
        VStack(spacing: 30) {
            Text(game.score >= 50 ? "🎉" : "💫")
                .font(.system(size: 100))
            
            Text(game.score >= 50 ? "Amazing!" : "Good Try!")
                .font(.largeTitle.bold())
                .foregroundColor(.white)
            
            VStack(spacing: 12) {
                Text("Final Score")
                    .font(.headline)
                    .foregroundColor(.white.opacity(0.7))
                
                Text("\(game.score)")
                    .font(.system(size: 60, weight: .bold))
                    .foregroundColor(.yellow)
            }
            .padding()
            .background(Color.white.opacity(0.1))
            .cornerRadius(20)
            
            // Achievement badges
            if game.score >= 50 {
                HStack(spacing: 20) {
                    AchievementBadge(emoji: "🌟", title: "Star Collector")
                    if game.score >= 100 {
                        AchievementBadge(emoji: "🏆", title: "Code Master")
                    }
                }
            }
            
            VStack(spacing: 16) {
                Button(action: {
                    game.startGame()
                }) {
                    Text("Play Again")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.green)
                        .cornerRadius(16)
                }
                
                Button(action: {
                    game.gameState = .menu
                }) {
                    Text("Back to Menu")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue.opacity(0.6))
                        .cornerRadius(16)
                }
            }
            .padding(.horizontal, 40)
        }
        .padding()
    }
}

struct AchievementBadge: View {
    let emoji: String
    let title: String
    
    var body: some View {
        VStack(spacing: 8) {
            Text(emoji)
                .font(.system(size: 40))
            Text(title)
                .font(.caption.bold())
                .foregroundColor(.white)
        }
        .padding()
        .background(Color.orange.opacity(0.3))
        .cornerRadius(12)
    }
}

// MARK: - Game Logic

class SpaceGame: ObservableObject {
    @Published var playerPosition: CGPoint = CGPoint(x: 200, y: 600)
    @Published var items: [GameItem] = []
    @Published var score: Int = 0
    @Published var lives: Int = 3
    @Published var gameState: GameState = .menu
    @Published var currentFact: String?
    
    var screenSize: CGSize = .zero
    private var gameTimer: Timer?
    private var factTimer: Timer?
    private var itemSpeed: Double = 2.0
    
    let codingFacts = [
        "⚡️ Loops help us repeat actions without writing the same code over and over!",
        "🎯 If statements let computers make smart choices, just like you do!",
        "📦 Variables are like boxes that store information we want to remember!",
        "🔧 Functions are named sets of instructions we can use again and again!",
        "📋 Arrays keep lists of things organized, like your favorite games!",
        "🐛 Finding and fixing bugs makes you a better coder - everyone does it!",
        "🎨 Coding is creative - you can build anything you imagine!",
        "🚀 Every programmer started as a beginner, just like you!"
    ]
    
    enum GameState {
        case menu, playing, gameOver
    }
    
    func startGame() {
        score = 0
        lives = 3
        items.removeAll()
        gameState = .playing
        playerPosition = CGPoint(x: screenSize.width / 2, y: screenSize.height - 80)
        
        gameTimer = Timer.scheduledTimer(withTimeInterval: 0.016, repeats: true) { _ in
            self.updateGame()
        }
        
        factTimer = Timer.scheduledTimer(withTimeInterval: 8.0, repeats: true) { _ in
            self.showRandomFact()
        }
        
        showRandomFact()
    }
    
    func updateGame() {
        // Move items down
        for index in items.indices {
            items[index].position.y += itemSpeed
        }
        
        // Remove items that are off screen
        items.removeAll { $0.position.y > screenSize.height + 50 }
        
        // Spawn new items (less frequently)
        if items.count < 4 && Double.random(in: 0...1) < 0.03 {
            spawnItem()
        }
        
        // Check collisions
        checkCollisions()
        
        // Gradually increase difficulty
        itemSpeed = min(4.0, 2.0 + Double(score) * 0.01)
    }
    
    func spawnItem() {
        let isBomb = Double.random(in: 0...1) < 0.25 // 25% chance of bomb
        let item = GameItem(
            emoji: isBomb ? "💣" : "⭐️",
            position: CGPoint(
                x: CGFloat.random(in: 50...(screenSize.width - 50)),
                y: -50
            ),
            isBomb: isBomb
        )
        items.append(item)
    }
    
    func checkCollisions() {
        let collisionDistance: CGFloat = 40
        
        for (index, item) in items.enumerated().reversed() {
            let distance = hypot(
                item.position.x - playerPosition.x,
                item.position.y - playerPosition.y
            )
            
            if distance < collisionDistance {
                if item.isBomb {
                    lives -= 1
                    if lives <= 0 {
                        endGame()
                    }
                } else {
                    score += 10
                }
                items.remove(at: index)
            }
        }
    }
    
    func movePlayer(to position: CGPoint, in size: CGSize) {
        // Only allow horizontal movement, keep at bottom
        let clampedX = max(30, min(size.width - 30, position.x))
        let fixedY = size.height - 80
        playerPosition = CGPoint(x: clampedX, y: fixedY)
    }
    
    func showRandomFact() {
        withAnimation {
            currentFact = codingFacts.randomElement()
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 5) {
            withAnimation {
                self.currentFact = nil
            }
        }
    }
    
    func endGame() {
        gameTimer?.invalidate()
        factTimer?.invalidate()
        gameState = .gameOver
    }
}

struct GameItem: Identifiable {
    let id = UUID()
    let emoji: String
    var position: CGPoint
    let isBomb: Bool
}

#Preview {
    SpaceGameView()
        .environmentObject(ProgressStore())
}
