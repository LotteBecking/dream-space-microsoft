import SwiftUI

struct ContentView: View {
    @EnvironmentObject private var progressStore: ProgressStore

    var body: some View {
        if progressStore.hasCompletedOnboarding {
            TabView {
                LevelListView()
                    .tabItem {
                        Label("Levels", systemImage: "flag.checkered")
                    }
                
                LeaderboardView()
                    .tabItem {
                        Label("Teams", systemImage: "trophy.fill")
                    }
                
                SpaceGameView()
                    .tabItem {
                        Label("Play", systemImage: "airplane")
                    }
                
                ProgressDashboardView()
                    .tabItem {
                        Label("Progress", systemImage: "chart.bar.fill")
                    }
            }
        } else {
            OnboardingView()
        }
    }
}
