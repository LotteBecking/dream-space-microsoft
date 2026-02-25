//
//  SampleData.swift
//  CodeQuest MVP
//
//  Sample missions and levels for testing
//

import Foundation

struct SampleData {
    
    // MARK: - Create Levels
    
    static func createLevels() -> [Level] {
        return [
            Level(
                number: 1,
                title: "Sequencing",
                description: "Learn the basics of giving commands in order",
                concept: .movement,
                badge: "🎯",
                isUnlocked: true
            ),
            Level(
                number: 2,
                title: "Loops",
                description: "Repeat commands to do more with less",
                concept: .loops,
                badge: "🔄"
            ),
            Level(
                number: 3,
                title: "Conditionals",
                description: "Make decisions based on conditions",
                concept: .conditionals,
                badge: "🤔"
            ),
            Level(
                number: 4,
                title: "Variables",
                description: "Store and use information",
                concept: .variables,
                badge: "📦"
            )
        ]
    }
    
    // MARK: - Create Missions
    
    static func createMissions(levels: [Level]) -> [Mission] {
        guard levels.count >= 3 else { return [] }
        
        var missions: [Mission] = []
        
        // LEVEL 1: Sequencing - Mission 1
        missions.append(Mission(
            levelId: levels[0].id,
            title: "First Steps",
            description: "Move the robot forward to reach the goal. Use Move Forward blocks to guide your robot!",
            difficulty: .easy,
            estimatedMinutes: 5,
            conceptsFocused: [.movement],
            availableBlocks: [.moveForward],
            gridSize: GridSize(width: 5, height: 3),
            startPosition: Position(x: 0, y: 1),
            goalPosition: Position(x: 4, y: 1),
            obstacles: [],
            items: [],
            optimalSolutionLength: 4
        ))
        
        // LEVEL 1: Sequencing - Mission 2
        missions.append(Mission(
            levelId: levels[0].id,
            title: "Turn and Move",
            description: "Navigate around obstacles! Use Move Forward, Turn Left, and Turn Right to reach the goal.",
            difficulty: .easy,
            estimatedMinutes: 7,
            conceptsFocused: [.movement],
            availableBlocks: [.moveForward, .turnLeft, .turnRight],
            gridSize: GridSize(width: 5, height: 5),
            startPosition: Position(x: 0, y: 0),
            goalPosition: Position(x: 4, y: 4),
            obstacles: [Position(x: 2, y: 1), Position(x: 2, y: 2), Position(x: 2, y: 3)],
            items: [],
            optimalSolutionLength: 9
        ))
        
        // LEVEL 2: Loops - Mission 1
        missions.append(Mission(
            levelId: levels[1].id,
            title: "Repeat Pattern",
            description: "Use a Repeat loop to move forward efficiently. Why write the same block many times?",
            difficulty: .medium,
            estimatedMinutes: 8,
            conceptsFocused: [.loops, .movement],
            availableBlocks: [.moveForward, .repeatLoop],
            gridSize: GridSize(width: 6, height: 3),
            startPosition: Position(x: 0, y: 1),
            goalPosition: Position(x: 5, y: 1),
            obstacles: [],
            items: [],
            optimalSolutionLength: 2 // Repeat 5 times { Move Forward }
        ))
        
        // LEVEL 2: Loops - Mission 2
        missions.append(Mission(
            levelId: levels[1].id,
            title: "Square Path",
            description: "Make a square! Use loops to repeat a pattern of moves and turns.",
            difficulty: .medium,
            estimatedMinutes: 10,
            conceptsFocused: [.loops, .movement],
            availableBlocks: [.moveForward, .turnRight, .repeatLoop],
            gridSize: GridSize(width: 6, height: 6),
            startPosition: Position(x: 1, y: 1),
            goalPosition: Position(x: 1, y: 1),
            obstacles: [],
            items: [Position(x: 4, y: 1), Position(x: 4, y: 4), Position(x: 1, y: 4)],
            optimalSolutionLength: 3 // Repeat 4 times { Move 3, Turn }
        ))
        
        // LEVEL 3: Conditionals - Mission 1
        missions.append(Mission(
            levelId: levels[2].id,
            title: "Smart Robot",
            description: "Use IF blocks to check if the path ahead is clear before moving.",
            difficulty: .hard,
            estimatedMinutes: 10,
            conceptsFocused: [.conditionals, .movement],
            availableBlocks: [.moveForward, .turnRight, .turnLeft, .ifCondition, .repeatLoop],
            gridSize: GridSize(width: 5, height: 5),
            startPosition: Position(x: 0, y: 0),
            goalPosition: Position(x: 4, y: 0),
            obstacles: [Position(x: 2, y: 0), Position(x: 2, y: 1)],
            items: [],
            optimalSolutionLength: 8
        ))
        
        return missions
    }
}
