import Foundation
import Combine

final class ProgressStore: ObservableObject {
    @Published private(set) var completedLessons: Set<String>
    @Published private(set) var hasCompletedOnboarding: Bool

    private let storageKey = "DreamSpaceKids.completedLessons"
    private let onboardingKey = "DreamSpaceKids.hasCompletedOnboarding"

    init() {
        if let data = UserDefaults.standard.data(forKey: storageKey),
           let decoded = try? JSONDecoder().decode(Set<String>.self, from: data) {
            completedLessons = decoded
        } else {
            completedLessons = []
        }
        hasCompletedOnboarding = UserDefaults.standard.bool(forKey: onboardingKey)
    }

    func isCompleted(_ lesson: Lesson) -> Bool {
        completedLessons.contains(lesson.id)
    }

    func markCompleted(_ lesson: Lesson) {
        completedLessons.insert(lesson.id)
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
}
