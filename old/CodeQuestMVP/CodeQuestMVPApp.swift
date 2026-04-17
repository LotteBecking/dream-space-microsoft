//
//  CodeQuestMVPApp.swift
//  CodeQuest MVP
//
//  Main app entry point for CodeQuest - A block-based coding learning app for kids
//

import SwiftUI

@main
struct CodeQuestMVPApp: App {
    @StateObject private var gameProgress = GameProgressViewModel()
    
    var body: some Scene {
        WindowGroup {
            MainMenuView()
                .environmentObject(gameProgress)
        }
    }
}
