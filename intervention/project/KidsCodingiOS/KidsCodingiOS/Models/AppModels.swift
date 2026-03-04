import Foundation

enum DifficultyLevel: String, Codable, CaseIterable, Identifiable {
    case beginner
    case intermediate
    case advanced

    var id: String { rawValue }
    var title: String { rawValue.capitalized }
}

enum DifficultyFilter: String, CaseIterable, Identifiable {
    case all
    case beginner
    case intermediate
    case advanced

    var id: String { rawValue }
    var title: String { rawValue.capitalized }

    var asDifficulty: DifficultyLevel? {
        switch self {
        case .all: return nil
        case .beginner: return .beginner
        case .intermediate: return .intermediate
        case .advanced: return .advanced
        }
    }
}

struct Challenge: Codable, Identifiable, Hashable {
    let id: String
    let title: String
    let description: String
    let difficulty: DifficultyLevel
    let category: String
    let points: Int
    let question: String
    let options: [String]
    let correctAnswer: Int
    let explanation: String
    let ageGroup: String
}

struct ChallengeResult: Codable, Identifiable, Hashable {
    let id: UUID
    let challengeId: String
    let completed: Bool
    let correct: Bool
    let date: Date
    let points: Int

    init(
        id: UUID = UUID(),
        challengeId: String,
        completed: Bool,
        correct: Bool,
        date: Date,
        points: Int
    ) {
        self.id = id
        self.challengeId = challengeId
        self.completed = completed
        self.correct = correct
        self.date = date
        self.points = points
    }
}

struct UserProfile: Codable, Hashable {
    let memberId: String
    var name: String
    var age: Int
    var teamId: String
    var avatar: String
}

struct TeamMember: Codable, Identifiable, Hashable {
    let id: String
    var name: String
    var avatar: String
    var points: Int
}

struct Team: Codable, Identifiable, Hashable {
    let id: String
    var name: String
    var members: [TeamMember]
    var totalPoints: Int
}

struct RankedMember: Identifiable {
    let id: String
    let name: String
    let avatar: String
    let points: Int
    let teamName: String
    let teamId: String
}
