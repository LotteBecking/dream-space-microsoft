import Foundation

enum ChallengeData {
    static let all: [Challenge] = [
        Challenge(id: "pattern-1", title: "Pattern Recognition", description: "Identify the next item in a sequence", difficulty: .beginner, category: "Patterns", points: 10, question: "What comes next in this pattern? 🔴 🔵 🔴 🔵 🔴 ?", options: ["🔴 Red", "🔵 Blue", "🟢 Green", "🟡 Yellow"], correctAnswer: 1, explanation: "The pattern alternates between red and blue circles. After red comes blue!", ageGroup: "8-12"),
        Challenge(id: "sequence-1", title: "Number Sequence", description: "Find the pattern in numbers", difficulty: .beginner, category: "Logic", points: 10, question: "What number comes next? 2, 4, 6, 8, __", options: ["9", "10", "11", "12"], correctAnswer: 1, explanation: "Each number increases by 2. After 8, we add 2 to get 10!", ageGroup: "8-12"),
        Challenge(id: "sorting-1", title: "Sort the Animals", description: "Understanding sorting algorithms", difficulty: .beginner, category: "Algorithms", points: 15, question: "Which order sorts these animals by size (smallest to largest)? 🐘 🐕 🐁", options: ["🐘 🐕 🐁", "🐁 🐕 🐘", "🐕 🐁 🐘", "🐁 🐘 🐕"], correctAnswer: 1, explanation: "Mouse is smallest, dog is medium, elephant is largest!", ageGroup: "8-12"),
        Challenge(id: "loops-1", title: "Repeat the Action", description: "Understanding loops", difficulty: .beginner, category: "Loops", points: 15, question: "If you clap 3 times, then repeat that 2 times, how many claps total?", options: ["3", "5", "6", "9"], correctAnswer: 2, explanation: "You clap 3 times, twice. That's 3 + 3 = 6 claps!", ageGroup: "8-12"),

        Challenge(id: "variables-1", title: "Variable Storage", description: "Understanding variables", difficulty: .intermediate, category: "Variables", points: 20, question: "If x = 5 and y = 3, what is x + y?", options: ["2", "8", "15", "53"], correctAnswer: 1, explanation: "Variables store values. We replace x with 5 and y with 3, then add: 5 + 3 = 8", ageGroup: "12-15"),
        Challenge(id: "conditionals-1", title: "If-Then Thinking", description: "Conditional logic", difficulty: .intermediate, category: "Conditionals", points: 20, question: "If temperature > 30°C, wear shorts. It's 32°C. What do you wear?", options: ["Jacket", "Shorts", "Sweater", "Raincoat"], correctAnswer: 1, explanation: "Since 32 > 30 is true, the condition is met, so wear shorts!", ageGroup: "12-15"),
        Challenge(id: "functions-1", title: "Function Magic", description: "Understanding functions", difficulty: .intermediate, category: "Functions", points: 25, question: "A function double(x) returns x * 2. What is double(7)?", options: ["7", "9", "14", "49"], correctAnswer: 2, explanation: "The function multiplies input by 2. So double(7) = 7 * 2 = 14", ageGroup: "12-15"),
        Challenge(id: "arrays-1", title: "List Indexing", description: "Working with arrays", difficulty: .intermediate, category: "Data Structures", points: 25, question: "fruits = [\"apple\", \"banana\", \"cherry\"]. What is fruits[1]?", options: ["apple", "banana", "cherry", "error"], correctAnswer: 1, explanation: "Arrays start counting at 0! So [0]=apple, [1]=banana, [2]=cherry", ageGroup: "12-15"),

        Challenge(id: "recursion-1", title: "Recursive Thinking", description: "Understanding recursion", difficulty: .advanced, category: "Recursion", points: 30, question: "What is the factorial of 4? (4! = 4 × 3 × 2 × 1)", options: ["10", "16", "24", "32"], correctAnswer: 2, explanation: "Factorial multiplies all numbers down to 1: 4 × 3 × 2 × 1 = 24", ageGroup: "15-18"),
        Challenge(id: "algorithms-1", title: "Binary Search", description: "Search algorithms", difficulty: .advanced, category: "Algorithms", points: 30, question: "How many steps max to find a number in a sorted list of 16 items using binary search?", options: ["4", "8", "16", "32"], correctAnswer: 0, explanation: "Binary search divides in half each time: 16→8→4→2→1 = 4 steps max!", ageGroup: "15-18"),
        Challenge(id: "complexity-1", title: "Time Complexity", description: "Algorithm efficiency", difficulty: .advanced, category: "Optimization", points: 35, question: "Which grows fastest as n increases: n, n², or 2ⁿ?", options: ["n", "n²", "2ⁿ", "All the same"], correctAnswer: 2, explanation: "Exponential (2ⁿ) grows much faster than polynomial (n²) or linear (n)!", ageGroup: "15-18"),
        Challenge(id: "data-structures-1", title: "Stack Operations", description: "Understanding stacks", difficulty: .advanced, category: "Data Structures", points: 35, question: "Push 5, Push 3, Pop, Push 7. What's on top of the stack?", options: ["5", "3", "7", "Empty"], correctAnswer: 2, explanation: "Stack is LIFO (Last In First Out). After operations: [5, 7], so 7 is on top!", ageGroup: "15-18")
    ]

    static func dailyChallenge(for date: Date) -> Challenge {
        let day = Calendar.current.ordinality(of: .day, in: .year, for: date) ?? 1
        let index = day % all.count
        return all[index]
    }

    static func challenge(by id: String) -> Challenge? {
        all.first { $0.id == id }
    }

    static func forAge(_ age: Int, from list: [Challenge]) -> [Challenge] {
        if (8...12).contains(age) {
            return list.filter { $0.ageGroup == "8-12" }
        }

        if (13...15).contains(age) {
            return list.filter { $0.ageGroup == "8-12" || $0.ageGroup == "12-15" }
        }

        return list
    }

    static func categoryEmoji(_ category: String) -> String {
        switch category {
        case "Patterns": return "🔄"
        case "Logic": return "🧩"
        case "Algorithms": return "⚙️"
        case "Loops": return "🔁"
        case "Variables": return "📦"
        case "Conditionals": return "🔀"
        case "Functions": return "🎯"
        case "Data Structures": return "📊"
        case "Recursion": return "🌀"
        case "Optimization": return "⚡"
        default: return "🎮"
        }
    }
}
