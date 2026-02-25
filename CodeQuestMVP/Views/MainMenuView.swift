//
//  MainMenuView.swift
//  CodeQuest MVP
//
//  Main menu / home screen
//

import SwiftUI

struct MainMenuView: View {
    @EnvironmentObject var gameProgress: GameProgressViewModel
    @State private var showProgress = false
    
    var body: some View {
        NavigationView {
            ZStack {
                // Background gradient
                LinearGradient(
                    colors: [Color.blue.opacity(0.6), Color.purple.opacity(0.6)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                VStack(spacing: 30) {
                    Spacer()
                    
                    // Title
                    VStack(spacing: 10) {
                        Text("CodeQuest")
                            .font(.system(size: 56, weight: .bold, design: .rounded))
                            .foregroundColor(.white)
                            .shadow(radius: 10)
                        
                        Text("Learn Coding Through Play")
                            .font(.title3)
                            .foregroundColor(.white.opacity(0.9))
                    }
                    .padding(.bottom, 20)
                    
                    // Player info card
                    PlayerInfoCard(user: gameProgress.currentUser)
                        .padding(.horizontal)
                    
                    // Main buttons
                    VStack(spacing: 20) {
                        NavigationLink(destination: LevelSelectionView()) {
                            MenuButton(
                                title: "Start Learning",
                                icon: "play.fill",
                                color: .green
                            )
                        }
                        
                        Button(action: { showProgress = true }) {
                            MenuButton(
                                title: "My Progress",
                                icon: "chart.bar.fill",
                                color: .orange
                            )
                        }
                        
                        Button(action: resetProgress) {
                            MenuButton(
                                title: "Reset Progress",
                                icon: "arrow.counterclockwise",
                                color: .red
                            )
                        }
                    }
                    .padding(.horizontal)
                    
                    Spacer()
                    
                    // Footer
                    Text("Made with ❤️ for young coders")
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.7))
                        .padding(.bottom)
                }
            }
            .sheet(isPresented: $showProgress) {
                ProgressView(user: gameProgress.currentUser, levels: gameProgress.levels)
            }
        }
    }
    
    private func resetProgress() {
        gameProgress.resetProgress()
    }
}

// MARK: - Player Info Card

struct PlayerInfoCard: View {
    let user: User
    
    var body: some View {
        HStack(spacing: 20) {
            // Avatar
            Circle()
                .fill(Color.white.opacity(0.3))
                .frame(width: 60, height: 60)
                .overlay(
                    Text("👨‍💻")
                        .font(.system(size: 30))
                )
            
            VStack(alignment: .leading, spacing: 5) {
                Text(user.name)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                
                HStack(spacing: 15) {
                    Label("\(user.totalPoints)", systemImage: "star.fill")
                    Label("\(user.currentStreak) days", systemImage: "flame.fill")
                }
                .font(.subheadline)
                .foregroundColor(.white.opacity(0.9))
            }
            
            Spacer()
        }
        .padding()
        .background(Color.white.opacity(0.2))
        .cornerRadius(15)
    }
}

// MARK: - Menu Button

struct MenuButton: View {
    let title: String
    let icon: String
    let color: Color
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .font(.title2)
            Text(title)
                .font(.title3)
                .fontWeight(.semibold)
            Spacer()
        }
        .foregroundColor(.white)
        .padding()
        .frame(maxWidth: .infinity)
        .background(color)
        .cornerRadius(15)
        .shadow(radius: 5)
    }
}

// MARK: - Preview

struct MainMenuView_Previews: PreviewProvider {
    static var previews: some View {
        MainMenuView()
            .environmentObject(GameProgressViewModel())
    }
}
