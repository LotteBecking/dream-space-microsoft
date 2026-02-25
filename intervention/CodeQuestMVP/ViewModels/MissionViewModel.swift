//
//  MissionViewModel.swift
//  CodeQuest MVP
//
//  ViewModel for managing mission state and user interactions
//

import Foundation
import SwiftUI

class MissionViewModel: ObservableObject {
    @Published var mission: Mission
    @Published var workspace: [Block] = []
    @Published var isExecuting: Bool = false
    
    let executor: BlockExecutor
    
    init(mission: Mission) {
        self.mission = mission
        self.executor = BlockExecutor(mission: mission)
    }
    
    // MARK: - Block Management
    
    func addBlock(_ blockType: BlockType) {
        let newBlock = Block(type: blockType, parameter: defaultParameter(for: blockType))
        workspace.append(newBlock)
    }
    
    func removeBlock(at index: Int) {
        guard index < workspace.count else { return }
        workspace.remove(at: index)
    }
    
    func moveBlock(from source: Int, to destination: Int) {
        guard source < workspace.count, destination <= workspace.count else { return }
        let block = workspace.remove(at: source)
        workspace.insert(block, at: destination)
    }
    
    func clearWorkspace() {
        workspace.removeAll()
    }
    
    // MARK: - Execution
    
    func executeCode(completion: @escaping (ExecutionResult) -> Void) {
        guard !workspace.isEmpty, !isExecuting else {
            completion(.error("Workspace is empty or already executing"))
            return
        }
        
        isExecuting = true
        
        executor.executeBlocks(workspace) { [weak self] result in
            self?.isExecuting = false
            completion(result)
        }
    }
    
    func resetSimulation() {
        executor.reset()
        isExecuting = false
    }
    
    // MARK: - Helpers
    
    private func defaultParameter(for blockType: BlockType) -> Int? {
        switch blockType {
        case .repeatLoop:
            return 3
        case .setVariable:
            return 0
        case .increaseVariable:
            return 1
        default:
            return nil
        }
    }
    
    func countTotalBlocks() -> Int {
        return executor.countBlocks(workspace)
    }
}
