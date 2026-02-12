import Foundation
import Combine

final class ProgressStore: ObservableObject {
    @Published private(set) var completedLessons: Set<String>
    @Published private(set) var hasCompletedOnboarding: Bool
    @Published private(set) var allGroups: [Group]
    @Published private(set) var currentGroup: Group?
    
    let currentUserId = "current-user" // In a real app, this would be authenticated

    private let storageKey = "DreamSpaceKids.completedLessons"
    private let onboardingKey = "DreamSpaceKids.hasCompletedOnboarding"
    private let groupsKey = "DreamSpaceKids.allGroups"
    private let currentGroupKey = "DreamSpaceKids.currentGroup"

    init() {
        if let data = UserDefaults.standard.data(forKey: storageKey),
           let decoded = try? JSONDecoder().decode(Set<String>.self, from: data) {
            completedLessons = decoded
        } else {
            completedLessons = []
        }
        
        hasCompletedOnboarding = UserDefaults.standard.bool(forKey: onboardingKey)
        
        if let data = UserDefaults.standard.data(forKey: groupsKey),
           let decoded = try? JSONDecoder().decode([Group].self, from: data) {
            allGroups = decoded
        } else {
            allGroups = Group.sampleGroups
        }
        
        if let data = UserDefaults.standard.data(forKey: currentGroupKey),
           let decoded = try? JSONDecoder().decode(Group.self, from: data) {
            currentGroup = decoded
        } else {
            currentGroup = nil
        }
    }

    func isCompleted(_ lesson: Lesson) -> Bool {
        completedLessons.contains(lesson.id)
    }

    func markCompleted(_ lesson: Lesson) {
        completedLessons.insert(lesson.id)
        
        // Award points to current group
        if currentGroup != nil {
            addPointsToCurrentGroup(100) // 100 points per completed lesson
        }
        
        persist()
    }

    func resetProgress() {
        completedLessons.removeAll()
        hasCompletedOnboarding = false
        persist()
    }

    func completeOnboarding() {
        hasCompletedOnboarding = true
        UserDefaults.standard.set(true, forKey: onboardingKey)
    }

    private func persist() {
        if let data = try? JSONEncoder().encode(completedLessons) {
            UserDefaults.standard.set(data, forKey: storageKey)
        }
    }

    func isLevelUnlocked(_ level: Level, index: Int) -> Bool {
        if index == 0 { return true }
        let previousLevel = Level.sampleLevels[index - 1]
        return previousLevel.lessons.allSatisfy { completedLessons.contains($0.id) }
    }

    func isLevelCompleted(_ level: Level) -> Bool {
        level.lessons.allSatisfy { completedLessons.contains($0.id) }
    }
    
    // MARK: - Group Management
    
    func createGroup(_ group: Group) {
        var newGroup = group
        newGroup.memberIds.append(currentUserId)
        allGroups.append(newGroup)
        currentGroup = newGroup
        persistGroups()
    }
    
    func joinGroup(_ group: Group) {
        if let index = allGroups.firstIndex(where: { $0.id == group.id }) {
            var updatedGroup = allGroups[index]
            if !updatedGroup.memberIds.contains(currentUserId) {
                updatedGroup.memberIds.append(currentUserId)
                allGroups[index] = updatedGroup
            }
            currentGroup = updatedGroup
            persistGroups()
        }
    }
    
    func leaveCurrentGroup() {
        currentGroup = nil
        persistGroups()
    }
    
    private func addPointsToCurrentGroup(_ points: Int) {
        guard let current = currentGroup,
              let index = allGroups.firstIndex(where: { $0.id == current.id }) else {
            return
        }
        
        allGroups[index].totalPoints += points
        currentGroup = allGroups[index]
        persistGroups()
    }
    
    private func persistGroups() {
        if let data = try? JSONEncoder().encode(allGroups) {
            UserDefaults.standard.set(data, forKey: groupsKey)
        }
        if let current = currentGroup,
           let data = try? JSONEncoder().encode(current) {
            UserDefaults.standard.set(data, forKey: currentGroupKey)
        } else {
            UserDefaults.standard.removeObject(forKey: currentGroupKey)
        }
    }
}
