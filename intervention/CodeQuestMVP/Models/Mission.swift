//
//  Mission.swift
//  CodeQuest MVP
//
//  Model representing a coding mission/puzzle
//

import Foundation

/// Difficulty level of a mission
enum MissionDifficulty: String, Codable {
    case easy = "Easy"
    case medium = "Medium"
    case hard = "Hard"
}

/// Represents a coding mission/puzzle
struct Mission: Identifiable, Codable {
    let id: UUID
    let levelId: UUID
    let title: String
    let description: String
    let difficulty: MissionDifficulty
    let estimatedMinutes: Int
    let conceptsFocused: [BlockCategory]
    let availableBlocks: [BlockType]
    let gridSize: GridSize
    let startPosition: Position
    let goalPosition: Position
    let obstacles: [Position]
    let items: [Position] // Items to collect
    let optimalSolutionLength: Int // For star rating
    
    init(
        id: UUID = UUID(),
        levelId: UUID,
        title: String,
        description: String,
        difficulty: MissionDifficulty,
        estimatedMinutes: Int,
        conceptsFocused: [BlockCategory],
        availableBlocks: [BlockType],
        gridSize: GridSize = GridSize(width: 5, height: 5),
        startPosition: Position,
        goalPosition: Position,
        obstacles: [Position] = [],
        items: [Position] = [],
        optimalSolutionLength: Int
    ) {
        self.id = id
        self.levelId = levelId
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.estimatedMinutes = estimatedMinutes
        self.conceptsFocused = conceptsFocused
        self.availableBlocks = availableBlocks
        self.gridSize = gridSize
        self.startPosition = startPosition
        self.goalPosition = goalPosition
        self.obstacles = obstacles
        self.items = items
        self.optimalSolutionLength = optimalSolutionLength
    }
}

/// Grid size for mission
struct GridSize: Codable, Equatable {
    let width: Int
    let height: Int
}

/// Position on the grid
struct Position: Codable, Equatable, Hashable {
    let x: Int
    let y: Int
}

/// Direction the robot is facing
enum Direction: String, Codable {
    case north, south, east, west
    
    mutating func turnLeft() {
        switch self {
        case .north: self = .west
        case .west: self = .south
        case .south: self = .east
        case .east: self = .north
        }
    }
    
    mutating func turnRight() {
        switch self {
        case .north: self = .east
        case .east: self = .south
        case .south: self = .west
        case .west: self = .north
        }
    }
    
    func forwardPosition(from position: Position) -> Position {
        switch self {
        case .north: return Position(x: position.x, y: position.y - 1)
        case .south: return Position(x: position.x, y: position.y + 1)
        case .east: return Position(x: position.x + 1, y: position.y)
        case .west: return Position(x: position.x - 1, y: position.y)
        }
    }
}

/// Result of mission completion
struct MissionResult: Codable {
    let missionId: UUID
    let completed: Bool
    let stars: Int // 1-3 stars based on efficiency
    let blocksUsed: Int
    let completionDate: Date
    
    init(missionId: UUID, completed: Bool, stars: Int, blocksUsed: Int, completionDate: Date = Date()) {
        self.missionId = missionId
        self.completed = completed
        self.stars = stars
        self.blocksUsed = blocksUsed
        self.completionDate = completionDate
    }
}
