import SwiftUI

enum AppTab: Hashable {
    case dashboard
    case challenges
    case progress
    case teams
    case profile
}

struct RootView: View {
    @EnvironmentObject private var store: AppStore
    @State private var selectedTab: AppTab = .dashboard
    @State private var showOnboarding = false

    var body: some View {
        TabView(selection: $selectedTab) {
            NavigationStack {
                DashboardView(selectedTab: $selectedTab)
            }
            .tabItem { Label("Home", systemImage: "house.fill") }
            .tag(AppTab.dashboard)

            NavigationStack {
                ChallengesView()
            }
            .tabItem { Label("Challenges", systemImage: "trophy.fill") }
            .tag(AppTab.challenges)

            NavigationStack {
                ProgressView()
            }
            .tabItem { Label("Progress", systemImage: "chart.bar.fill") }
            .tag(AppTab.progress)

            NavigationStack {
                TeamsView()
            }
            .tabItem { Label("Teams", systemImage: "person.3.fill") }
            .tag(AppTab.teams)

            NavigationStack {
                ProfileView()
            }
            .tabItem { Label("Profile", systemImage: "person.fill") }
            .tag(AppTab.profile)
        }
        .sheet(isPresented: $showOnboarding) {
            OnboardingView(isPresented: $showOnboarding)
                .interactiveDismissDisabled()
        }
        .onAppear {
            showOnboarding = store.profile == nil
        }
        .onChange(of: store.profile) { _, newValue in
            showOnboarding = newValue == nil
        }
    }
}
