//
//  MissionListView.swift
//  CodeQuest MVP
//
//  Shows all missions within a selected level
//

import SwiftUI

struct MissionListView: View {
    @EnvironmentObject var gameProgress: GameProgressViewModel
    let level: Level
    
    var missions: [Mission] {
        gameProgress.missions(for: level)
    }
    
    var body: some View {
        ZStack {
            Color(red: 0.95, green: 0.95, blue: 0.98)
                .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 20) {
                    // Level header
                    VStack(spacing: 12) {
                        Text(level.badge)
                            .font(.system(size: 60))
                        
                        Text(level.title)
                            .font(.title)
                            .fontWeight(.bold)
                        
                        Text(level.description)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding()
                    
                    // Missions list
                    ForEach(missions) { mission in
                        MissionRow(mission: mission)
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical)
            }
        }
        .navigationTitle("Missions")
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Mission Row

struct MissionRow: View {
    @EnvironmentObject var gameProgress: GameProgressViewModel
    let mission: Mission
    
    var isCompleted: Bool {
        gameProgress.currentUser.hasMissionCompleted(mission.id)
    }
    
    var stars: Int {
        gameProgress.currentUser.starsForMission(mission.id)
    }
    
    var body: some View {
        NavigationLink(destination: MissionView(mission: mission)) {
            HStack(spacing: 16) {
                // Mission icon
                ZStack {
                    Circle()
                        .fill(difficultyColor)
                        .frame(width: 60, height: 60)
                    
                    if isCompleted {
                        Image(systemName: "checkmark")
                            .font(.title2)
                            .foregroundColor(.white)
                    } else {
                        Image(systemName: "flag.fill")
                            .font(.title3)
                            .foregroundColor(.white)
                    }
                }
                
                // Mission info
                VStack(alignment: .leading, spacing: 6) {
                    Text(mission.title)
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    Text(mission.description)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .lineLimit(2)
                    
                    HStack(spacing: 12) {
                        Label("\(mission.estimatedMinutes) min", systemImage: "clock")
                        Label(mission.difficulty.rawValue, systemImage: "chart.bar")
                    }
                    .font(.caption)
                    .foregroundColor(.secondary)
                }
                
                Spacer()
                
                // Stars
                if isCompleted {
                    VStack {
                        HStack(spacing: 2) {
                            ForEach(0..<3) { index in
                                Image(systemName: index < stars ? "star.fill" : "star")
                                    .font(.caption)
                                    .foregroundColor(.yellow)
                            }
                        }
                    }
                }
            }
            .padding()
            .background(Color.white)
            .cornerRadius(15)
            .shadow(color: Color.black.opacity(0.05), radius: 5, x: 0, y: 2)
        }
    }
    
    var difficultyColor: Color {
        switch mission.difficulty {
        case .easy: return .green
        case .medium: return .orange
        case .hard: return .red
        }
    }
}

// MARK: - Preview

struct MissionListView_Previews: PreviewProvider {
    static var previews: some View {
        let gameProgress = GameProgressViewModel()
        NavigationView {
            MissionListView(level: gameProgress.levels.first!)
                .environmentObject(gameProgress)
        }
    }
}
