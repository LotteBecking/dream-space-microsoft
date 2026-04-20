import SwiftUI

struct BadgeView: View {
    let title: String
    let isEarned: Bool

    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: isEarned ? "star.fill" : "star")
                .font(.title)
                .foregroundStyle(isEarned ? Theme.highlight : .gray)
            Text(title)
                .font(.caption)
                .multilineTextAlignment(.center)
                .foregroundStyle(isEarned ? .primary : .secondary)
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(isEarned ? Theme.highlight.opacity(0.2) : Theme.card)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}
