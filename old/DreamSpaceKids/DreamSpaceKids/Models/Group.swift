import Foundation

struct Group: Identifiable, Codable, Hashable {
    let id: String
    var name: String
    var emoji: String
    var memberIds: [String]
    var totalPoints: Int
    
    init(id: String = UUID().uuidString, name: String, emoji: String, memberIds: [String] = [], totalPoints: Int = 0) {
        self.id = id
        self.name = name
        self.emoji = emoji
        self.memberIds = memberIds
        self.totalPoints = totalPoints
    }
    
    static let sampleGroups: [Group] = [
        Group(name: "Code Stars", emoji: "⭐️", memberIds: ["user1", "user2"], totalPoints: 1250),
        Group(name: "Bug Hunters", emoji: "🐛", memberIds: ["user3", "user4", "user5"], totalPoints: 980),
        Group(name: "Pixel Pals", emoji: "🎨", memberIds: ["user6", "user7"], totalPoints: 875),
        Group(name: "Cyber Squad", emoji: "🚀", memberIds: ["user8"], totalPoints: 760),
        Group(name: "Bit Buddies", emoji: "💎", memberIds: ["user9", "user10", "user11"], totalPoints: 650)
    ]
}

struct LeaderboardEntry: Identifiable, Hashable {
    let id: String
    let name: String
    let emoji: String
    let points: Int
    let rank: Int
    
    init(group: Group, rank: Int) {
        self.id = group.id
        self.name = group.name
        self.emoji = group.emoji
        self.points = group.totalPoints
        self.rank = rank
    }
}
