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
                ChallengeView(lesson: Level.allLessons.first ?? Lesson.sampleLessons[0])
                    .tabItem {
                        Label("Practice", systemImage: "puzzlepiece.extension")
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
