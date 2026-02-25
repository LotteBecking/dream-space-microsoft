//
//  Level.swift
//  CodeQuest MVP
//
//  Model representing a level containing multiple missions
//

import Foundation

/// Represents a level in the progression system
struct Level: Identifiable, Codable {
    let id: UUID
    let number: Int
    let title: String
    let description: String
    let concept: BlockCategory
    let badge: String // Emoji badge for completion
    var isUnlocked: Bool
    var isCompleted: Bool
    
    init(
        id: UUID = UUID(),
        number: Int,
        title: String,
        description: String,
        concept: BlockCategory,
        badge: String,
        isUnlocked: Bool = false,
        isCompleted: Bool = false
    ) {
        self.id = id
        self.number = number
        self.title = title
        self.description = description
        self.concept = concept
        self.badge = badge
        self.isUnlocked = isUnlocked
        self.isCompleted = isCompleted
    }
}
