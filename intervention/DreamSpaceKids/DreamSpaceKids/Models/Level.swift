import Foundation

struct Level: Identifiable, Hashable {
    let id: String
    let title: String
    let summary: String
    let lessons: [Lesson]

    static let sampleLevels: [Level] = [
        Level(
            id: "level-1",
            title: "Level 1: Sequences",
            summary: "Put steps in the right order.",
            lessons: [Lesson.sampleLessons[0]]
        ),
        Level(
            id: "level-2",
            title: "Level 2: Loops",
            summary: "Repeat actions with ease.",
            lessons: [Lesson.sampleLessons[1]]
        ),
        Level(
            id: "level-3",
            title: "Level 3: Conditions",
            summary: "Make smart choices in code.",
            lessons: [Lesson.sampleLessons[2]]
        ),
        Level(
            id: "level-4",
            title: "Level 4: Functions",
            summary: "Bundle your favorite actions.",
            lessons: [Lesson.sampleLessons[3]]
        )
    ]

    static var allLessons: [Lesson] {
        sampleLevels.flatMap { $0.lessons }
    }
}
