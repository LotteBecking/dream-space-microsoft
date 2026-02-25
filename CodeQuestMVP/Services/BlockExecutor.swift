//
//  BlockExecutor.swift
//  CodeQuest MVP
//
//  Executes blocks and simulates robot movement on the grid
//

import Foundation
import Combine

/// State of the robot/simulation
struct RobotState {
    var position: Position
    var direction: Direction
    var itemsCollected: Int
    var variables: [String: Int] // For variable blocks
    
    init(position: Position, direction: Direction = .east) {
        self.position = position
        self.direction = direction
        self.itemsCollected = 0
        self.variables = ["counter": 0]
    }
}

/// Result of block execution
enum ExecutionResult: Equatable {
    case success
    case collision // Hit obstacle or boundary
    case goalReached
    case error(String)
}

/// Executes coding blocks and manages simulation state
class BlockExecutor: ObservableObject {
    @Published var robotState: RobotState
    @Published var isExecuting: Bool = false
    @Published var executionHistory: [Position] = []
    @Published var currentBlockIndex: Int? = nil
    
    let mission: Mission
    private var executionSpeed: TimeInterval = 0.5 // Seconds between blocks
    
    init(mission: Mission) {
        self.mission = mission
        self.robotState = RobotState(position: mission.startPosition)
        self.executionHistory = [mission.startPosition]
    }
    
    // MARK: - Execution
    
    /// Execute a list of blocks
    func executeBlocks(_ blocks: [Block], completion: @escaping (ExecutionResult) -> Void) {
        guard !isExecuting else { return }
        
        isExecuting = true
        executionHistory = [robotState.position]
        currentBlockIndex = nil
        
        // Execute blocks asynchronously with delays for animation
        Task { @MainActor in
            let result = await executeBlocksRecursive(blocks)
            isExecuting = false
            currentBlockIndex = nil
            completion(result)
        }
    }
    
    /// Recursively execute blocks (handles nested blocks in loops/conditionals)
    private func executeBlocksRecursive(_ blocks: [Block]) async -> ExecutionResult {
        for (index, block) in blocks.enumerated() {
            await MainActor.run {
                currentBlockIndex = index
            }
            
            let result = await executeBlock(block)
            
            // Wait for animation
            try? await Task.sleep(nanoseconds: UInt64(executionSpeed * 1_000_000_000))
            
            switch result {
            case .goalReached:
                return .goalReached
            case .collision:
                return .collision
            case .error(let message):
                return .error(message)
            case .success:
                continue
            }
        }
        
        // Check if goal reached after all blocks
        if robotState.position == mission.goalPosition {
            return .goalReached
        }
        
        return .success
    }
    
    /// Execute a single block
    private func executeBlock(_ block: Block) async -> ExecutionResult {
        switch block.type {
        case .moveForward:
            return await moveForward()
            
        case .turnLeft:
            await MainActor.run {
                robotState.direction.turnLeft()
            }
            return .success
            
        case .turnRight:
            await MainActor.run {
                robotState.direction.turnRight()
            }
            return .success
            
        case .pickUp:
            await MainActor.run {
                if mission.items.contains(robotState.position) {
                    robotState.itemsCollected += 1
                }
            }
            return .success
            
        case .repeatLoop:
            let repeatCount = block.parameter ?? 3
            for _ in 0..<repeatCount {
                let result = await executeBlocksRecursive(block.childBlocks)
                if result != .success {
                    return result
                }
            }
            return .success
            
        case .ifCondition:
            // Check if path ahead is clear
            let ahead = robotState.direction.forwardPosition(from: robotState.position)
            let isPathClear = isPositionValid(ahead) && !mission.obstacles.contains(ahead)
            
            if isPathClear {
                return await executeBlocksRecursive(block.childBlocks)
            }
            return .success
            
        case .setVariable:
            await MainActor.run {
                robotState.variables["counter"] = block.parameter ?? 0
            }
            return .success
            
        case .increaseVariable:
            await MainActor.run {
                let current = robotState.variables["counter"] ?? 0
                robotState.variables["counter"] = current + (block.parameter ?? 1)
            }
            return .success
        }
    }
    
    /// Move robot forward in current direction
    private func moveForward() async -> ExecutionResult {
        let newPosition = robotState.direction.forwardPosition(from: robotState.position)
        
        // Check boundaries
        guard isPositionValid(newPosition) else {
            return .collision
        }
        
        // Check obstacles
        guard !mission.obstacles.contains(newPosition) else {
            return .collision
        }
        
        // Move robot
        await MainActor.run {
            robotState.position = newPosition
            executionHistory.append(newPosition)
        }
        
        // Check if goal reached
        if newPosition == mission.goalPosition {
            return .goalReached
        }
        
        return .success
    }
    
    // MARK: - Helpers
    
    /// Check if position is within grid boundaries
    private func isPositionValid(_ position: Position) -> Bool {
        return position.x >= 0 && position.x < mission.gridSize.width &&
               position.y >= 0 && position.y < mission.gridSize.height
    }
    
    /// Reset simulation to initial state
    func reset() {
        robotState = RobotState(position: mission.startPosition)
        executionHistory = [mission.startPosition]
        isExecuting = false
        currentBlockIndex = nil
    }
    
    /// Count total blocks in a list (including nested blocks)
    func countBlocks(_ blocks: [Block]) -> Int {
        var count = 0
        for block in blocks {
            count += 1
            count += countBlocks(block.childBlocks)
        }
        return count
    }
}
