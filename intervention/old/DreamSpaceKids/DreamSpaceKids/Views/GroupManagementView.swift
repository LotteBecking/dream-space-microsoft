import SwiftUI

struct GroupManagementView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    @Environment(\.dismiss) private var dismiss
    @State private var showCreateForm = false
    @State private var selectedTab = 0
    
    var body: some View {
        NavigationStack {
            ZStack {
                Theme.background.ignoresSafeArea()
                
                VStack(spacing: 0) {
                    // Tab selector
                    Picker("Mode", selection: $selectedTab) {
                        Text("Join Team").tag(0)
                        Text("Create Team").tag(1)
                    }
                    .pickerStyle(.segmented)
                    .padding()
                    
                    if selectedTab == 0 {
                        JoinGroupView()
                    } else {
                        CreateGroupView()
                    }
                }
            }
            .navigationTitle("Teams")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct JoinGroupView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                Text("Pick a team to join! 🎉")
                    .font(.title3.bold())
                    .foregroundColor(Theme.accent)
                    .padding(.top)
                
                ForEach(progressStore.allGroups) { group in
                    GroupCardView(group: group) {
                        progressStore.joinGroup(group)
                        dismiss()
                    }
                }
            }
            .padding()
        }
    }
}

struct CreateGroupView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    @Environment(\.dismiss) private var dismiss
    @State private var groupName = ""
    @State private var selectedEmoji = "⭐️"
    
    private let emojiOptions = ["⭐️", "🚀", "🎨", "💎", "🐛", "🌈", "🔥", "⚡️", "🎯", "🏆", "🎪", "🦄"]
    
    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                Text("Create Your Dream Team! 🌟")
                    .font(.title3.bold())
                    .foregroundColor(Theme.accent)
                    .padding(.top)
                
                // Team name input
                VStack(alignment: .leading, spacing: 8) {
                    Text("Team Name")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    TextField("Enter team name", text: $groupName)
                        .textFieldStyle(.plain)
                        .padding()
                        .background(Theme.card)
                        .cornerRadius(12)
                }
                
                // Emoji picker
                VStack(alignment: .leading, spacing: 8) {
                    Text("Team Emoji")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    LazyVGrid(columns: [GridItem(.adaptive(minimum: 60))], spacing: 12) {
                        ForEach(emojiOptions, id: \.self) { emoji in
                            Button(action: { selectedEmoji = emoji }) {
                                Text(emoji)
                                    .font(.system(size: 40))
                                    .frame(width: 60, height: 60)
                                    .background(selectedEmoji == emoji ? Theme.accent.opacity(0.2) : Theme.card)
                                    .cornerRadius(12)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 12)
                                            .stroke(selectedEmoji == emoji ? Theme.accent : Color.clear, lineWidth: 3)
                                    )
                            }
                        }
                    }
                }
                
                // Preview
                VStack(spacing: 12) {
                    Text("Preview")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    HStack {
                        Text(selectedEmoji)
                            .font(.system(size: 50))
                        
                        Text(groupName.isEmpty ? "Your Team" : groupName)
                            .font(.title2.bold())
                            .foregroundColor(.primary)
                    }
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Theme.card)
                    .cornerRadius(16)
                }
                
                // Create button
                Button(action: {
                    let newGroup = Group(
                        name: groupName.isEmpty ? "Awesome Team" : groupName,
                        emoji: selectedEmoji,
                        memberIds: [progressStore.currentUserId]
                    )
                    progressStore.createGroup(newGroup)
                    dismiss()
                }) {
                    HStack {
                        Image(systemName: "sparkles")
                        Text("Create Team")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Theme.accent)
                    .foregroundColor(.white)
                    .cornerRadius(16)
                    .shadow(color: Theme.accent.opacity(0.3), radius: 8, y: 4)
                }
                .padding(.top)
            }
            .padding()
        }
    }
}

struct GroupCardView: View {
    let group: Group
    let onJoin: () -> Void
    
    var body: some View {
        HStack(spacing: 16) {
            Text(group.emoji)
                .font(.system(size: 50))
            
            VStack(alignment: .leading, spacing: 4) {
                Text(group.name)
                    .font(.headline)
                
                HStack(spacing: 4) {
                    Image(systemName: "person.3.fill")
                        .font(.caption)
                    Text("\(group.memberIds.count) members")
                        .font(.subheadline)
                }
                .foregroundColor(.secondary)
                
                HStack(spacing: 4) {
                    Image(systemName: "star.fill")
                        .font(.caption)
                        .foregroundColor(Theme.highlight)
                    Text("\(group.totalPoints) points")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
            
            Spacer()
            
            Button(action: onJoin) {
                Text("Join")
                    .fontWeight(.semibold)
                    .padding(.horizontal, 20)
                    .padding(.vertical, 10)
                    .background(Theme.accent)
                    .foregroundColor(.white)
                    .cornerRadius(20)
            }
        }
        .padding()
        .background(Theme.card)
        .cornerRadius(16)
    }
}

#Preview {
    GroupManagementView()
        .environmentObject(ProgressStore())
}
