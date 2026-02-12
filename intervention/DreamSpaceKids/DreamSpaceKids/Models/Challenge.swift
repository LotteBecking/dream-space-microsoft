import Foundation

struct Challenge: Hashable {
    let prompt: String
    let choices: [String]
    let correctIndex: Int
    let explanation: String
}
