//
//  MissionView.swift
//  CodeQuest MVP
//
//  Main mission/puzzle view with block coding interface
//

import SwiftUI

struct MissionView: View {
    @EnvironmentObject var gameProgress: GameProgressViewModel
    @StateObject private var executor: BlockExecutor
    @State private var workspace: [Block] = []
    @State private var showCompletionAlert = false
    @State private var completionMessage = ""
    @State private var earnedStars = 0
    @Environment(\.dismiss) var dismiss
    
    let mission: Mission
    
    init(mission: Mission) {
        self.mission = mission
        _executor = StateObject(wrappedValue: BlockExecutor(mission: mission))
    }
    
    var body: some View {
        GeometryReader { geometry in
            VStack(spacing: 0) {
                // Top bar with mission info
                missionHeader
                    .frame(height: geometry.size.height * 0.12)
                
                // Main content area
                HStack(spacing: 0) {
                    // Left: Grid simulation
                    SimulationView(
                        mission: mission,
                        robotState: executor.robotState,
                        executionHistory: executor.executionHistory
                    )
                    .frame(width: geometry.size.width * 0.45)
                    .background(Color.white)
                    
                    Divider()
                    
                    // Right: Coding workspace and palette
                    VStack(spacing: 0) {
                        // Workspace (where blocks are arranged)
                        WorkspaceView(
                            blocks: $workspace,
                            availableBlocks: mission.availableBlocks,
                            isExecuting: executor.isExecuting
                        )
                        .frame(height: geometry.size.height * 0.55)
                        
                        Divider()
                        
                        // Block palette
                        BlockPaletteView(
                            availableBlocks: mission.availableBlocks,
                            onBlockSelected: { blockType in
                                addBlockToWorkspace(blockType)
                            }
                        )
                        .frame(height: geometry.size.height * 0.21)
                    }
                    .frame(width: geometry.size.width * 0.55)
                }
                .frame(height: geometry.size.height * 0.76)
                
                Divider()
                
                // Bottom: Control buttons
                controlButtons
                    .frame(height: geometry.size.height * 0.12)
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .alert("Mission Complete! 🎉", isPresented: $showCompletionAlert) {
            Button("Continue") {
                dismiss()
            }
            Button("Try Again") {
                resetMission()
            }
        } message: {
            Text(completionMessage)
        }
    }
    
    // MARK: - Mission Header
    
    private var missionHeader: some View {
        VStack(spacing: 8) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(mission.title)
                        .font(.headline)
                    Text(mission.description)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                // Current mission stats
                HStack(spacing: 15) {
                    Label("Blocks: \(workspace.count)", systemImage: "cube.fill")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            .padding(.horizontal)
        }
        .padding(.vertical, 8)
        .background(Color(red: 0.95, green: 0.95, blue: 0.98))
    }
    
    // MARK: - Control Buttons
    
    private var controlButtons: some View {
        HStack(spacing: 15) {
            // Run button
            Button(action: runCode) {
                HStack {
                    Image(systemName: executor.isExecuting ? "stop.fill" : "play.fill")
                    Text(executor.isExecuting ? "Running..." : "Run Code")
                }
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(executor.isExecuting ? Color.orange : Color.green)
                .cornerRadius(12)
            }
            .disabled(executor.isExecuting || workspace.isEmpty)
            
            // Reset button
            Button(action: resetMission) {
                HStack {
                    Image(systemName: "arrow.counterclockwise")
                    Text("Reset")
                }
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .cornerRadius(12)
            }
            .disabled(executor.isExecuting)
            
            // Clear button
            Button(action: clearWorkspace) {
                HStack {
                    Image(systemName: "trash")
                    Text("Clear")
                }
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.red)
                .cornerRadius(12)
            }
            .disabled(executor.isExecuting || workspace.isEmpty)
        }
        .padding()
        .background(Color(red: 0.95, green: 0.95, blue: 0.98))
    }
    
    // MARK: - Actions
    
    private func addBlockToWorkspace(_ blockType: BlockType) {
        let newBlock = Block(type: blockType, parameter: blockType == .repeatLoop ? 3 : nil)
        workspace.append(newBlock)
    }
    
    private func runCode() {
        guard !workspace.isEmpty else { return }
        
        executor.executeBlocks(workspace) { result in
            handleExecutionResult(result)
        }
    }
    
    private func handleExecutionResult(_ result: ExecutionResult) {
        switch result {
        case .goalReached:
            // Mission completed!
            let blocksUsed = executor.countBlocks(workspace)
            gameProgress.completeMission(mission, blocksUsed: blocksUsed)
            
            earnedStars = gameProgress.currentUser.starsForMission(mission.id)
            completionMessage = "You earned \(earnedStars) star\(earnedStars == 1 ? "" : "s")! Used \(blocksUsed) blocks."
            showCompletionAlert = true
            
        case .collision:
            completionMessage = "Oops! The robot hit an obstacle. Try again!"
            showCompletionAlert = true
            
        case .success:
            completionMessage = "Code executed, but didn't reach the goal. Keep trying!"
            showCompletionAlert = true
            
        case .error(let message):
            completionMessage = "Error: \(message)"
            showCompletionAlert = true
        }
    }
    
    private func resetMission() {
        executor.reset()
        showCompletionAlert = false
    }
    
    private func clearWorkspace() {
        workspace.removeAll()
    }
}

// MARK: - Preview

struct MissionView_Previews: PreviewProvider {
    static var previews: some View {
        let gameProgress = GameProgressViewModel()
        let mission = gameProgress.missions.first!
        
        NavigationView {
            MissionView(mission: mission)
                .environmentObject(gameProgress)
        }
    }
}
