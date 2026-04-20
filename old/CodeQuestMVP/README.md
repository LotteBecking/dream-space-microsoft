# 🚀 CodeQuest MVP - Block-Based Coding App for Kids

A SwiftUI iOS application that teaches children (ages 8-18) coding concepts through interactive, block-based programming missions.

## 📍 Project Location

**Path:** `/Users/lottebecking/Documents/GitHub/dream-space-microsoft/CodeQuestMVP/`

## 🎯 Features

### MVP Core Features
- **Block-Based Coding Engine**: Drag-and-drop visual programming with blocks for:
  - Sequencing (move, turn, pick up)
  - Loops (repeat)
  - Conditionals (if/else)
  - Variables (set/increase)

- **Level-Based Progression**: 4 levels focusing on different coding concepts
  - Level 1: Sequencing
  - Level 2: Loops
  - Level 3: Conditionals
  - Level 4: Variables (framework ready, can be extended)

- **Short Missions**: 5-10 minute coding puzzles with:
  - Visual grid simulation with robot character
  - Clear goals and obstacles
  - Real-time feedback
  - 5 sample missions included

- **Gamification**:
  - Star ratings (1-3 stars based on solution efficiency)
  - Points system
  - Level badges
  - Daily streak tracking
  - Progress tracking

- **Offline Ready**: All progress saved locally with UserDefaults

## 📱 Requirements

- iOS 15.0 or later
- Xcode 13.0 or later
- Swift 5.5 or later

## 🚀 Getting Started

### Installation

1. **Open in Xcode**:
   ```bash
   cd /Users/lottebecking/Documents/GitHub/dream-space-microsoft
   ```
   
   Then in Xcode:
   - File → New → Project
   - iOS → App
   - Name: "CodeQuestMVP"
   - Select SwiftUI as interface
   - Select Swift as language
   - Save in `/Users/lottebecking/Documents/GitHub/dream-space-microsoft/`

2. **Add Existing Files**:
   - Drag the `CodeQuestMVP` folder (with all Swift files) into your Xcode project
   - Check "Copy items if needed"
   - Ensure all files are added to target

3. **Set Bundle Identifier**:
   - In Xcode, select the project in the navigator
   - Under "Signing & Capabilities", set your Team
   - Update the Bundle Identifier (e.g., `com.lottebecking.CodeQuestMVP`)

4. **Run the App**:
   - Select a simulator or connected device
   - Press `Cmd + R` or click the Run button
   - The app will compile and launch

### Project Structure

```
CodeQuestMVP/
├── CodeQuestMVPApp.swift          # App entry point
├── Models/                         # Data models
│   ├── Block.swift                # Block types and structure
│   ├── Mission.swift              # Mission definition
│   ├── Level.swift                # Level progression
│   └── User.swift                 # User profile
├── ViewModels/                     # Business logic
│   ├── GameProgressViewModel.swift # Progress management
│   └── MissionViewModel.swift     # Mission-specific logic
├── Services/                       # Core services
│   └── BlockExecutor.swift        # Code execution engine
├── Views/                          # UI Components
│   ├── MainMenuView.swift         # Home screen
│   ├── LevelSelectionView.swift   # Level selection
│   ├── MissionListView.swift      # Mission list per level
│   ├── MissionView.swift          # Main coding interface
│   ├── SimulationView.swift       # Visual grid simulation
│   ├── WorkspaceView.swift        # Code workspace
│   ├── BlockPaletteView.swift     # Block selection palette
│   └── ProgressView.swift         # User progress screen
├── SampleData/                     # Test data
│   └── SampleData.swift           # Sample missions and levels
└── Info.plist                      # App configuration
```

## 🎮 How to Play

1. **Main Menu**: Start from the home screen showing your profile stats
2. **Select Level**: Choose from unlocked levels (Level 1 starts unlocked)
3. **Choose Mission**: Pick a mission to attempt
4. **Code**: 
   - Tap blocks from the palette to add them to your workspace
   - Drag blocks to reorder them
   - Tap "Run Code" to execute your solution
5. **Complete**: Reach the goal to earn stars and unlock the next mission!

## 🎨 Sample Missions Included

### Level 1: Sequencing
1. **First Steps**: Move forward to reach the goal (4 blocks optimal)
2. **Turn and Move**: Navigate around obstacles (9 blocks optimal)

### Level 2: Loops
1. **Repeat Pattern**: Use loops to move efficiently (2 blocks optimal)
2. **Square Path**: Create a square pattern with loops (3 blocks optimal)

### Level 3: Conditionals
1. **Smart Robot**: Use IF blocks to navigate dynamically (8 blocks optimal)

## 🔧 Customization & Extension

### Adding New Missions

Edit `SampleData/SampleData.swift` and add new missions:

```swift
missions.append(Mission(
    levelId: levels[X].id,
    title: "Your Mission Title",
    description: "Mission description",
    difficulty: .medium,
    estimatedMinutes: 8,
    conceptsFocused: [.loops],
    availableBlocks: [.moveForward, .repeatLoop],
    gridSize: GridSize(width: 6, height: 6),
    startPosition: Position(x: 0, y: 0),
    goalPosition: Position(x: 5, y: 5),
    obstacles: [Position(x: 2, y: 2)],
    items: [],
    optimalSolutionLength: 5
))
```

### Adding New Block Types

1. Add the block type to `BlockType` enum in `Models/Block.swift`
2. Implement execution logic in `Services/BlockExecutor.swift`
3. Add icon mapping in `Views/BlockPaletteView.swift`

### Customizing Appearance

- Colors are defined in each block's `.color` property
- Adjust grid cell sizes in `SimulationView.swift`
- Modify UI spacing and fonts in individual view files

## 🎯 Architecture

### Design Patterns Used

- **MVVM**: ViewModels manage business logic, Views handle UI
- **Observable Pattern**: `@Published` properties for reactive UI updates
- **Strategy Pattern**: Block execution handled by modular `BlockExecutor`
- **Repository Pattern**: `GameProgressViewModel` manages data persistence

### Key Components

1. **BlockExecutor**: Interprets and executes block sequences with visual feedback
2. **GameProgressViewModel**: Manages user progress, unlocking, and persistence
3. **Drag & Drop**: Simplified tap-to-add with reordering support
4. **Grid Simulation**: Real-time visual feedback of code execution

## 📊 Data Persistence

Progress is saved locally using `UserDefaults`:
- User profile (points, streak, badges)
- Level unlock status
- Mission completion results
- Star ratings

To reset progress, use the "Reset Progress" button in the main menu.

## 🚧 Future Enhancements (Beyond MVP)

The codebase is structured to easily add:
- [ ] Multiplayer challenges
- [ ] Sandbox mode for free coding
- [ ] Teacher dashboard for classroom management
- [ ] More block types (functions, events)
- [ ] Sound effects and music
- [ ] Achievement system
- [ ] Cloud save/sync
- [ ] Leaderboards
- [ ] Hint system
- [ ] Tutorial mode

## 🤝 Contributing

To extend this MVP:

1. Follow the existing code structure
2. Add comprehensive comments for educational clarity
3. Test with the target age group (8-18 years)
4. Keep UI simple and intuitive
5. Ensure missions are completable within 5-10 minutes

## 📝 License

This is an educational project. Feel free to use and modify for learning purposes.

## 🎓 Educational Goals

CodeQuest teaches:
- **Computational Thinking**: Breaking problems into steps
- **Sequencing**: Understanding order of operations
- **Pattern Recognition**: Using loops effectively
- **Logic**: Conditional decision-making
- **Debugging**: Trial and error problem-solving
- **Optimization**: Finding efficient solutions

## 💡 Tips for Educators

- Start students with Level 1 missions
- Encourage finding the optimal solution (3 stars)
- Use the star system to teach efficiency
- Let students explain their code to peers
- Challenge students to solve missions differently

---

**Made with ❤️ for young coders**

Built by Lotte Becking • February 2026
