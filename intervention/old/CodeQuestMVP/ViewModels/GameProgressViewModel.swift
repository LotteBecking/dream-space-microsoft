//
//  GameProgressViewModel.swift
//  CodeQuest MVP
//
//  Manages user progress, levels, and missions across the app
//

import Foundation
import SwiftUI

class GameProgressViewModel: ObservableObject {
    @Published var currentUser: User
    @Published var levels: [Level]
    @Published var missions: [Mission]
    
    init() {
        // Initialize with sample data
        self.currentUser = User(name: "Player")
        
        // Create levels first
        let initialLevels = SampleData.createLevels()
        self.levels = initialLevels
        
        // Then create missions using the levels
        self.missions = SampleData.createMissions(levels: initialLevels)
        
        // Unlock first level
        if self.levels.count > 0 {
            self.levels[0].isUnlocked = true
        }
        
        // Load saved progress if available
        loadProgress()
    }
    
    // MARK: - Level Management
    
    /// Get missions for a specific level
    func missions(for level: Level) -> [Mission] {
        return missions.filter { $0.levelId == level.id }
    }
    
    /// Check if all missions in a level are completed
    func isLevelCompleted(_ level: Level) -> Bool {
        let levelMissions = missions(for: level)
        return !levelMissions.isEmpty && levelMissions.allSatisfy { currentUser.hasMissionCompleted($0.id) }
    }
    
    // MARK: - Mission Completion
    
    /// Complete a mission and award points/badges
    func completeMission(_ mission: Mission, blocksUsed: Int) {
        guard !currentUser.hasMissionCompleted(mission.id) else {
            // Already completed, but update if better score
            updateMissionScore(mission, blocksUsed: blocksUsed)
            return
        }
        
        // Calculate stars based on efficiency
        let stars = calculateStars(mission: mission, blocksUsed: blocksUsed)
        
        // Create mission result
        let result = MissionResult(
            missionId: mission.id,
            completed: true,
            stars: stars,
            blocksUsed: blocksUsed
        )
        
        // Update user progress
        currentUser.completedMissions.append(mission.id)
        currentUser.missionResults.append(result)
        
        // Award points
        let points = calculatePoints(stars: stars, difficulty: mission.difficulty)
        currentUser.totalPoints += points
        
        // Update streak
        updateStreak()
        
        // Check if level is completed and unlock next
        if let levelIndex = levels.firstIndex(where: { $0.id == mission.levelId }) {
            let levelCompleted = isLevelCompleted(levels[levelIndex])
            
            if levelCompleted {
                levels[levelIndex].isCompleted = true
                
                // Award level badge
                if !currentUser.badges.contains(levels[levelIndex].badge) {
                    currentUser.badges.append(levels[levelIndex].badge)
                }
                
                // Unlock next level
                if levelIndex + 1 < levels.count {
                    levels[levelIndex + 1].isUnlocked = true
                }
            }
        }
        
        // Save progress
        saveProgress()
        
        // Trigger UI update
        objectWillChange.send()
    }
    
    /// Update mission score if better than previous
    private func updateMissionScore(_ mission: Mission, blocksUsed: Int) {
        guard let index = currentUser.missionResults.firstIndex(where: { $0.missionId == mission.id }) else {
            return
        }
        
        let oldResult = currentUser.missionResults[index]
        let newStars = calculateStars(mission: mission, blocksUsed: blocksUsed)
        
        if newStars > oldResult.stars || (newStars == oldResult.stars && blocksUsed < oldResult.blocksUsed) {
            currentUser.missionResults[index] = MissionResult(
                missionId: mission.id,
                completed: true,
                stars: newStars,
                blocksUsed: blocksUsed
            )
            
            // Award additional points for improvement
            let additionalPoints = (newStars - oldResult.stars) * 50
            currentUser.totalPoints += additionalPoints
            
            saveProgress()
            objectWillChange.send()
        }
    }
    
    // MARK: - Calculations
    
    /// Calculate stars (1-3) based on solution efficiency
    private func calculateStars(mission: Mission, blocksUsed: Int) -> Int {
        let optimal = mission.optimalSolutionLength
        
        if blocksUsed <= optimal {
            return 3 // Perfect solution
        } else if blocksUsed <= optimal + 3 {
            return 2 // Good solution
        } else {
            return 1 // Completed but inefficient
        }
    }
    
    /// Calculate points based on stars and difficulty
    private func calculatePoints(stars: Int, difficulty: MissionDifficulty) -> Int {
        let basePoints: Int
        switch difficulty {
        case .easy: basePoints = 100
        case .medium: basePoints = 200
        case .hard: basePoints = 300
        }
        
        return basePoints * stars
    }
    
    /// Update daily streak
    private func updateStreak() {
        let calendar = Calendar.current
        let today = Date()
        
        if let lastPlayed = currentUser.lastPlayedDate {
            if calendar.isDateInToday(lastPlayed) {
                // Already played today, keep streak
                return
            } else if calendar.isDateInYesterday(lastPlayed) {
                // Played yesterday, increment streak
                currentUser.currentStreak += 1
            } else {
                // Missed a day, reset streak
                currentUser.currentStreak = 1
            }
        } else {
            // First time playing
            currentUser.currentStreak = 1
        }
        
        currentUser.lastPlayedDate = today
    }
    
    // MARK: - Persistence
    
    private func saveProgress() {
        // Save to UserDefaults (simple local storage)
        if let encoded = try? JSONEncoder().encode(currentUser) {
            UserDefaults.standard.set(encoded, forKey: "currentUser")
        }
        
        if let encodedLevels = try? JSONEncoder().encode(levels) {
            UserDefaults.standard.set(encodedLevels, forKey: "levels")
        }
    }
    
    private func loadProgress() {
        // Load from UserDefaults
        if let userData = UserDefaults.standard.data(forKey: "currentUser"),
           let user = try? JSONDecoder().decode(User.self, from: userData) {
            self.currentUser = user
        }
        
        if let levelsData = UserDefaults.standard.data(forKey: "levels"),
           let savedLevels = try? JSONDecoder().decode([Level].self, from: levelsData) {
            self.levels = savedLevels
        }
    }
    
    /// Reset all progress (for testing)
    func resetProgress() {
        UserDefaults.standard.removeObject(forKey: "currentUser")
        UserDefaults.standard.removeObject(forKey: "levels")
        
        self.currentUser = User(name: currentUser.name)
        self.levels = SampleData.createLevels()
        self.missions = SampleData.createMissions(levels: self.levels)
        
        if !self.levels.isEmpty {
            self.levels[0].isUnlocked = true
        }
        
        objectWillChange.send()
    }
}
