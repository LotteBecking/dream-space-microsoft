import SwiftUI

struct OnboardingView: View {
    @EnvironmentObject private var progressStore: ProgressStore
    @State private var pageIndex = 0

    private let pages: [OnboardingPage] = [
        OnboardingPage(
            title: "Welcome to DreamSpace!",
            message: "Let’s explore coding with stories, puzzles, and badges.",
            systemImage: "sparkles"
        ),
        OnboardingPage(
            title: "Learn New Skills",
            message: "Each level teaches a new coding superpower.",
            systemImage: "wand.and.stars"
        ),
        OnboardingPage(
            title: "Practice & Earn",
            message: "Solve challenges to unlock badges and new levels.",
            systemImage: "star.circle.fill"
        )
    ]

    var body: some View {
        VStack(spacing: 24) {
            TabView(selection: $pageIndex) {
                ForEach(pages.indices, id: \.self) { index in
                    OnboardingPageView(page: pages[index])
                        .tag(index)
                }
            }
            #if os(iOS)
            .tabViewStyle(.page)
            #endif

            HStack(spacing: 8) {
                ForEach(pages.indices, id: \.self) { index in
                    Circle()
                        .fill(index == pageIndex ? Theme.accent : Theme.card)
                        .frame(width: 10, height: 10)
                }
            }

            Button(pageIndex == pages.count - 1 ? "Start Learning" : "Next") {
                if pageIndex == pages.count - 1 {
                    progressStore.completeOnboarding()
                } else {
                    pageIndex += 1
                }
            }
            .buttonStyle(.borderedProminent)
            .tint(Theme.accent)
        }
        .padding()
        .background(Theme.background.ignoresSafeArea())
    }
}

struct OnboardingPageView: View {
    let page: OnboardingPage

    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: page.systemImage)
                .font(.system(size: 64))
                .foregroundStyle(Theme.accent)
            Text(page.title)
                .font(.largeTitle.bold())
            Text(page.message)
                .font(.title3)
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}

struct OnboardingPage: Hashable {
    let title: String
    let message: String
    let systemImage: String
}
