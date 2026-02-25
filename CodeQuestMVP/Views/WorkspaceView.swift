//
//  WorkspaceView.swift
//  CodeQuest MVP
//
//  The coding workspace where blocks are arranged
//

import SwiftUI

struct WorkspaceView: View {
    @Binding var blocks: [Block]
    let availableBlocks: [BlockType]
    let isExecuting: Bool
    
    @State private var draggingBlock: Block?
    @State private var dragOffset: CGSize = .zero
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Header
            HStack {
                Text("Your Code")
                    .font(.headline)
                    .padding()
                
                Spacer()
                
                if !blocks.isEmpty {
                    Text("\(blocks.count) block\(blocks.count == 1 ? "" : "s")")
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .padding()
                }
            }
            .background(Color(red: 0.95, green: 0.95, blue: 0.98))
            
            Divider()
            
            // Workspace area
            ScrollView {
                if blocks.isEmpty {
                    VStack(spacing: 20) {
                        Spacer()
                        
                        Image(systemName: "arrow.down.circle")
                            .font(.system(size: 50))
                            .foregroundColor(.gray.opacity(0.5))
                        
                        Text("Drag blocks here to build your code")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                        
                        Spacer()
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .padding()
                } else {
                    VStack(spacing: 8) {
                        ForEach(Array(blocks.enumerated()), id: \.element.id) { index, block in
                            BlockView(block: block, index: index)
                                .onDrag {
                                    draggingBlock = block
                                    return NSItemProvider(object: block.id.uuidString as NSString)
                                }
                                .onDrop(of: [.text], delegate: BlockDropDelegate(
                                    blocks: $blocks,
                                    draggingBlock: $draggingBlock,
                                    currentIndex: index
                                ))
                        }
                    }
                    .padding()
                }
            }
            .background(Color.white)
        }
        .disabled(isExecuting)
        .opacity(isExecuting ? 0.7 : 1.0)
    }
}

// MARK: - Block View

struct BlockView: View {
    let block: Block
    let index: Int
    @State private var isEditing = false
    
    var body: some View {
        HStack(spacing: 8) {
            // Block number
            Text("\(index + 1)")
                .font(.caption)
                .foregroundColor(.white)
                .frame(width: 24, height: 24)
                .background(Circle().fill(Color.gray))
            
            // Block content
            VStack(alignment: .leading, spacing: 4) {
                HStack {
                    Text(block.displayText)
                        .font(.subheadline)
                        .foregroundColor(.white)
                    
                    Spacer()
                    
                    // Edit icon for blocks with parameters
                    if block.type.isContainer || block.type == .repeatLoop {
                        Image(systemName: "slider.horizontal.3")
                            .font(.caption)
                            .foregroundColor(.white.opacity(0.7))
                    }
                }
                
                // Child blocks indicator
                if !block.childBlocks.isEmpty {
                    HStack(spacing: 4) {
                        Image(systemName: "arrow.turn.down.right")
                            .font(.caption2)
                        Text("\(block.childBlocks.count) nested block\(block.childBlocks.count == 1 ? "" : "s")")
                            .font(.caption2)
                    }
                    .foregroundColor(.white.opacity(0.8))
                    .padding(.leading, 4)
                }
            }
            .padding(.vertical, 12)
            .padding(.horizontal, 12)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(block.type.color)
            .cornerRadius(10)
        }
    }
}

// MARK: - Drop Delegate for reordering

struct BlockDropDelegate: DropDelegate {
    @Binding var blocks: [Block]
    @Binding var draggingBlock: Block?
    let currentIndex: Int
    
    func performDrop(info: DropInfo) -> Bool {
        draggingBlock = nil
        return true
    }
    
    func dropEntered(info: DropInfo) {
        guard let draggingBlock = draggingBlock,
              let fromIndex = blocks.firstIndex(where: { $0.id == draggingBlock.id }),
              fromIndex != currentIndex else {
            return
        }
        
        withAnimation {
            let toIndex = currentIndex
            blocks.move(fromOffsets: IndexSet(integer: fromIndex),
                       toOffset: toIndex > fromIndex ? toIndex + 1 : toIndex)
        }
    }
}

// MARK: - Preview

struct WorkspaceView_Previews: PreviewProvider {
    static var previews: some View {
        WorkspaceView(
            blocks: .constant([
                Block(type: .moveForward),
                Block(type: .turnRight),
                Block(type: .repeatLoop, parameter: 3, childBlocks: [
                    Block(type: .moveForward)
                ])
            ]),
            availableBlocks: [.moveForward, .turnLeft, .turnRight, .repeatLoop],
            isExecuting: false
        )
        .frame(height: 400)
    }
}
