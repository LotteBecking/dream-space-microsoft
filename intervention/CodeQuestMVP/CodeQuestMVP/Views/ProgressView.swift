//
//  ProgressView.swift
//  CodeQuest MVP
//
//  Shows user's overall progress, badges, and stats
//

import SwiftUI

struct ProgressView: View {
    let user: User
    let levels: [Level]
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 25) {
                    // User stats card
                    VStack(spacing: 20) {
                        Text("👨‍💻")
                            .font(.system(size: 80))
                        
                        Text(user.name)
                            .font(.title)
                            .fontWeight(.bold)
                        
                        HStack(spacing: 40) {
                            StatItem(value: "\(user.totalPoints)", label: "Points", icon: "star.fill", color: .yellow)
                            StatItem(value: "\(user.completedMissions.count)", label: "Missions", icon: "flag.fill", color: .blue)
                            StatItem(value: "\(user.currentStreak)", label: "Day Streak", icon: "flame.fill", color: .orange)
                        }
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(20)
                    .shadow(radius: 5)
                    
                    // Badges section
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Badges Earned")
                            .font(.headline)
                            .padding(.horizontal)
                        
                        if user.badges.isEmpty {
                            Text("Complete levels to earn badges!")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                                .padding()
                        } else {
                            LazyVGrid(columns: [GridItem(.adaptive(minimum: 80))], spacing: 15) {
                                ForEach(user.badges, id: \.self) { badge in
                                    BadgeView(badge: badge)
                                }
                            }
                            .padding(.horizontal)
                        }
                    }
                    .padding(.vertical)
                    
                    // Level progress
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Level Progress")
                            .font(.headline)
                            .padding(.horizontal)
                        
                        ForEach(levels.filter { $0.isUnlocked }) { level in
                            LevelProgressRow(level: level, user: user)
                        }
                        .padding(.horizontal)
                    }
                    
                    Spacer(minLength: 30)
                }
                .padding()
            }
            .background(Color(red: 0.95, green: 0.95, blue: 0.98))
            .navigationTitle("My Progress")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// MARK: - Stat Item

struct StatItem: View {
    let value: String
    let label: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
            
            Text(value)
                .font(.title2)
                .fontWeight(.bold)
            
            Text(label)
                .font(.caption)
                .foregroundColor(.secondary)
        }
    }
}

// MARK: - Badge View

struct BadgeView: View {
    let badge: String
    
    var body: some View {
        VStack {
            ZStack {
                Circle()
                    .fill(Color.yellow.opacity(0.2))
                    .frame(width: 70, height: 70)
                
                Text(badge)
                    .font(.system(size: 35))
            }
        }
        .padding(8)
        .background(Color.white)
        .cornerRadius(15)
        .shadow(radius: 3)
    }
}

// MARK: - Level Progress Row

struct LevelProgressRow: View {
    let level: Level
    let user: User
    
    var body: some View {
        HStack {
            Text(level.badge)
                .font(.title)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(level.title)
                    .font(.headline)
                
                if level.isCompleted {
                    HStack {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                        Text("Completed!")
                            .font(.subheadline)
                            .foregroundColor(.green)
                    }
                } else {
                    Text("In Progress")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
            
            Spacer()
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}

// MARK: - Preview

struct ProgressView_Previews: PreviewProvider {
    static var previews: some View {
        let gameProgress = GameProgressViewModel()
        ProgressView(user: gameProgress.currentUser, levels: gameProgress.levels)
    }
}
