import SwiftUI

@main
struct DreamSpaceKidsApp: App {
    @StateObject private var progressStore = ProgressStore()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(progressStore)
                .tint(Theme.accent)
        }
    }
}
