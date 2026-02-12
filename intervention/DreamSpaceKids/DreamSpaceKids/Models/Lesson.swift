import Foundation

struct Lesson: Identifiable, Hashable {
    let id: String
    let title: String
    let summary: String
    let concept: String
    let example: String
    let challenge: Challenge

    static let sampleLessons: [Lesson] = [
        Lesson(
            id: "sequence",
            title: "Sequences",
            summary: "Put steps in the right order.",
            concept: "Computers follow instructions step by step. A sequence is the order of those steps.",
            example: "let steps = [\"Wake up\", \"Brush teeth\", \"Eat breakfast\"]",
            challenge: Challenge(
                prompt: "Which step should come first to make a sandwich?",
                choices: ["Eat it", "Put bread on plate", "Clean the table"],
                correctIndex: 1,
                explanation: "Start by putting the bread on the plate so you can build the sandwich."
            )
        ),
        Lesson(
            id: "loops",
            title: "Loops",
            summary: "Repeat actions without extra effort.",
            concept: "A loop repeats instructions. Use loops when a task happens more than once.",
            example: "for _ in 1...3 { print(\"Jump!\") }",
            challenge: Challenge(
                prompt: "Which loop makes the robot hop 5 times?",
                choices: ["for _ in 1...5", "if hops == 5", "repeat once"],
                correctIndex: 0,
                explanation: "A for-loop from 1 to 5 repeats exactly five times."
            )
        ),
        Lesson(
            id: "conditions",
            title: "Conditions",
            summary: "Make decisions in code.",
            concept: "An if-statement chooses different paths based on a condition.",
            example: "if hasKey { openDoor() } else { knock() }",
            challenge: Challenge(
                prompt: "What does an if-statement do?",
                choices: ["Repeats a task", "Chooses a path", "Stores a number"],
                correctIndex: 1,
                explanation: "If-statements decide which code runs based on a condition."
            )
        ),
        Lesson(
            id: "functions",
            title: "Functions",
            summary: "Save your favorite actions.",
            concept: "A function is a named set of instructions you can reuse.",
            example: "func dance() { print(\"Spin\") }",
            challenge: Challenge(
                prompt: "Why do we use functions?",
                choices: ["To repeat steps safely", "To hide all code", "To stop the program"],
                correctIndex: 0,
                explanation: "Functions let you reuse steps without rewriting them."
            )
        )
    ]
}
