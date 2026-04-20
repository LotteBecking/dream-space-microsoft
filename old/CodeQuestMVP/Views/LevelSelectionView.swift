//
//  LevelSelectionView.swift
//  CodeQuest MVP
//
//  Level selection screen showing all available levels
//

import SwiftUI

struct LevelSelectionView: View {
    @EnvironmentObject var gameProgress: GameProgressViewModel
    
    var body: some View {
        ZStack {
            // Background
            Color(red: 0.95, green: 0.95, blue: 0.98)
                .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 20) {
                    // Header
                    VStack(spacing: 8) {
                        Text("Choose Your Level")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                        
                        Text("Complete missions to unlock new levels")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.top)
                    
                    // Levels grid
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 20) {
                        ForEach(gameProgress.levels) { level in
                            LevelCard(level: level)
                        }
                    }
                    .padding()
                }
            }
        }
        .navigationTitle("Levels")
        .navigationBarTitleDisplayMode(.inline)
    }
}

// MARK: - Level Card

struct LevelCard: View {
    @EnvironmentObject var gameProgress: GameProgressViewModel
    let level: Level
    
    var body: some View {
        NavigationLink(
            destination: MissionListView(level: level),
            label: {
                VStack(spacing: 12) {
                    // Badge
                    ZStack {
                        Circle()
                            .fill(level.isUnlocked ? levelColor : Color.gray.opacity(0.3))
                            .frame(width: 80, height: 80)
                        
                        if level.isUnlocked {
                            Text(level.badge)
                                .font(.system(size: 40))
                        } else {
                            Image(systemName: "lock.fill")
                                .font(.system(size: 30))
                                .foregroundColor(.white)
                        }
                        
                        // Completed checkmark
                        if level.isCompleted {
                            Image(systemName: "checkmark.circle.fill")
                                .font(.title2)
                                .foregroundColor(.green)
                                .background(Circle().fill(Color.white))
                                .offset(x: 30, y: -30)
                        }
                    }
                    
                    // Level info
                    VStack(spacing: 4) {
                        Text("Level \(level.number)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Text(level.title)
                            .font(.headline)
                            .foregroundColor(.primary)
                            .multilineTextAlignment(.center)
                        
                        Text(level.description)
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                            .lineLimit(2)
                    }
                    
                    // Progress indicator
                    if level.isUnlocked {
                        let missions = gameProgress.missions(for: level)
                        let completed = missions.filter { gameProgress.currentUser.hasMissionCompleted($0.id) }.count
                        
                        ProgressBar(current: completed, total: missions.count)
                            .frame(height: 8)
                    }
                }
                .padding()
                .frame(maxWidth: .infinity)
                .background(Color.white)
                .cornerRadius(20)
                .shadow(color: Color.black.opacity(0.1), radius: 10, x: 0, y: 5)
            }
        )
        .disabled(!level.isUnlocked)
        .opacity(level.isUnlocked ? 1.0 : 0.6)
    }
    
    var levelColor: Color {
        switch level.concept {
        case .movement: return .blue
        case .loops: return .orange
        case .conditionals: return .green
        case .variables: return .purple
        }
    }
}

// MARK: - Progress Bar

struct ProgressBar: View {
    let current: Int
    let total: Int
    
    var progress: Double {
        guard total > 0 else { return 0 }
        return Double(current) / Double(total)
    }
    
    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                Rectangle()
                    .fill(Color.gray.opacity(0.2))
                    .cornerRadius(4)
                
                Rectangle()
                    .fill(Color.green)
                    .frame(width: geometry.size.width * progress)
                    .cornerRadius(4)
            }
        }
    }
}

// MARK: - Preview

struct LevelSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            LevelSelectionView()
                .environmentObject(GameProgressViewModel())
        }
    }
}
