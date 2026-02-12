import SwiftUI

struct LeaderboardView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    @State private var showCreateGroup = false
    
    private var leaderboard: [LeaderboardEntry] {
        let sorted = progressStore.allGroups.sorted { $0.totalPoints > $1.totalPoints }
        return sorted.enumerated().map { index, group in
            LeaderboardEntry(group: group, rank: index + 1)
        }
    }
    
    var body: some View {
        NavigationStack {
            ZStack {
                Theme.background.ignoresSafeArea()
                
                VStack(spacing: 0) {
                    // Header with trophy
                    VStack(spacing: 12) {
                        Text("🏆")
                            .font(.system(size: 60))
                        Text("Team Leaderboard")
                            .font(.title.bold())
                            .foregroundColor(Theme.accent)
                    }
                    .padding(.top, 20)
                    .padding(.bottom, 24)
                    
                    ScrollView {
                        VStack(spacing: 12) {
                            ForEach(leaderboard) { entry in
                                LeaderboardRowView(entry: entry)
                            }
                        }
                        .padding(.horizontal)
                        .padding(.bottom, 20)
                    }
                    
                    // Create/Join Group Button
                    Button(action: { showCreateGroup = true }) {
                        HStack {
                            Image(systemName: "person.3.fill")
                            Text("Create or Join a Team")
                                .fontWeight(.semibold)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Theme.accent)
                        .foregroundColor(.white)
                        .cornerRadius(16)
                        .shadow(color: Theme.accent.opacity(0.3), radius: 8, y: 4)
                    }
                    .padding()
                }
            }
            .sheet(isPresented: $showCreateGroup) {
                GroupManagementView()
            }
        }
    }
}

struct LeaderboardRowView: View {
    let entry: LeaderboardEntry
    
    private var medalEmoji: String? {
        switch entry.rank {
        case 1: return "🥇"
        case 2: return "🥈"
        case 3: return "🥉"
        default: return nil
        }
    }
    
    private var backgroundColor: Color {
        switch entry.rank {
        case 1: return Color.yellow.opacity(0.15)
        case 2: return Color.gray.opacity(0.15)
        case 3: return Color.orange.opacity(0.15)
        default: return Theme.card
        }
    }
    
    var body: some View {
        HStack(spacing: 16) {
            // Rank indicator
            ZStack {
                Circle()
                    .fill(backgroundColor)
                    .frame(width: 50, height: 50)
                
                if let medal = medalEmoji {
                    Text(medal)
                        .font(.system(size: 28))
                } else {
                    Text("\(entry.rank)")
                        .font(.title2.bold())
                        .foregroundColor(Theme.accent)
                }
            }
            
            // Group emoji
            Text(entry.emoji)
                .font(.system(size: 40))
            
            // Group name and points
            VStack(alignment: .leading, spacing: 4) {
                Text(entry.name)
                    .font(.headline)
                    .foregroundColor(.primary)
                
                HStack(spacing: 4) {
                    Image(systemName: "star.fill")
                        .font(.caption)
                        .foregroundColor(Theme.highlight)
                    Text("\(entry.points) points")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
            
            Spacer()
            
            // Sparkles for top 3
            if entry.rank <= 3 {
                Text("✨")
                    .font(.title2)
            }
        }
        .padding()
        .background(backgroundColor)
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(entry.rank <= 3 ? Theme.highlight.opacity(0.3) : Color.clear, lineWidth: 2)
        )
    }
}

#Preview {
    LeaderboardView()
        .environmentObject(ProgressStore())
}
