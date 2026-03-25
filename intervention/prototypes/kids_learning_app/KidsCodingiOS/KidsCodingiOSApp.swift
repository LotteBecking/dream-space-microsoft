import SwiftUI

@main
struct KidsCodingiOSApp: App {
    @StateObject private var store = AppStore()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(store)
                .task {
                    // Pull the latest data from the backend on launch.
                    // If the server is unreachable the app keeps working offline.
                    await store.loadFromServerIfAvailable()
                }
        }
    }
}
