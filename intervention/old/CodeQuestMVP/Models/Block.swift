//
//  Block.swift
//  CodeQuest MVP
//
//  Model representing a coding block that can be dragged and dropped
//

import Foundation
import SwiftUI

/// Types of blocks available in the coding palette
enum BlockType: String, Codable, CaseIterable {
    case moveForward = "Move Forward"
    case turnLeft = "Turn Left"
    case turnRight = "Turn Right"
    case pickUp = "Pick Up"
    case repeatLoop = "Repeat"
    case ifCondition = "If"
    case setVariable = "Set"
    case increaseVariable = "Increase"
    
    /// Color coding for different block categories
    var color: Color {
        switch self {
        case .moveForward, .turnLeft, .turnRight, .pickUp:
            return .blue
        case .repeatLoop:
            return .orange
        case .ifCondition:
            return .green
        case .setVariable, .increaseVariable:
            return .purple
        }
    }
    
    /// Block category for organizing palette
    var category: BlockCategory {
        switch self {
        case .moveForward, .turnLeft, .turnRight, .pickUp:
            return .movement
        case .repeatLoop:
            return .loops
        case .ifCondition:
            return .conditionals
        case .setVariable, .increaseVariable:
            return .variables
        }
    }
    
    /// Whether this block can contain child blocks
    var isContainer: Bool {
        switch self {
        case .repeatLoop, .ifCondition:
            return true
        default:
            return false
        }
    }
}

/// Categories for organizing blocks
enum BlockCategory: String, Codable, CaseIterable {
    case movement = "Movement"
    case loops = "Loops"
    case conditionals = "Conditionals"
    case variables = "Variables"
}

/// Represents a single coding block in the workspace
struct Block: Identifiable, Codable, Equatable {
    let id: UUID
    let type: BlockType
    var parameter: Int? // For repeat count, variable value, etc.
    var childBlocks: [Block] // For container blocks like repeat/if
    
    init(id: UUID = UUID(), type: BlockType, parameter: Int? = nil, childBlocks: [Block] = []) {
        self.id = id
        self.type = type
        self.parameter = parameter
        self.childBlocks = childBlocks
    }
    
    /// Display text for the block
    var displayText: String {
        switch type {
        case .repeatLoop:
            return "Repeat \(parameter ?? 3) times"
        case .ifCondition:
            return "If path ahead"
        case .setVariable:
            return "Set counter = \(parameter ?? 0)"
        case .increaseVariable:
            return "counter + \(parameter ?? 1)"
        default:
            return type.rawValue
        }
    }
}
