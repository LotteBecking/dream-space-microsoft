//
//  User.swift
//  CodeQuest MVP
//
//  Model representing a user's profile and progress
//

import Foundation

/// Represents a user/player
struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var totalPoints: Int
    var currentStreak: Int
    var lastPlayedDate: Date?
    var completedMissions: [UUID] // Mission IDs
    var badges: [String] // Badge emojis earned
    var missionResults: [MissionResult] // Detailed results
    
    init(
        id: UUID = UUID(),
        name: String,
        totalPoints: Int = 0,
        currentStreak: Int = 0,
        lastPlayedDate: Date? = nil,
        completedMissions: [UUID] = [],
        badges: [String] = [],
        missionResults: [MissionResult] = []
    ) {
        self.id = id
        self.name = name
        self.totalPoints = totalPoints
        self.currentStreak = currentStreak
        self.lastPlayedDate = lastPlayedDate
        self.completedMissions = completedMissions
        self.badges = badges
        self.missionResults = missionResults
    }
    
    /// Check if a specific mission has been completed
    func hasMissionCompleted(_ missionId: UUID) -> Bool {
        return completedMissions.contains(missionId)
    }
    
    /// Get stars earned for a specific mission
    func starsForMission(_ missionId: UUID) -> Int {
        return missionResults.first { $0.missionId == missionId }?.stars ?? 0
    }
}
