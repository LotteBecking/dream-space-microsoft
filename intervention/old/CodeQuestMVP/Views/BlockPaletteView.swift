//
//  BlockPaletteView.swift
//  CodeQuest MVP
//
//  Palette of available blocks that can be dragged to workspace
//

import SwiftUI

struct BlockPaletteView: View {
    let availableBlocks: [BlockType]
    let onBlockSelected: (BlockType) -> Void
    
    // Group blocks by category for better organization
    private var groupedBlocks: [BlockCategory: [BlockType]] {
        Dictionary(grouping: availableBlocks) { $0.category }
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Header
            Text("Block Palette")
                .font(.headline)
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color(red: 0.95, green: 0.95, blue: 0.98))
            
            Divider()
            
            // Blocks grid
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(availableBlocks, id: \.self) { blockType in
                        PaletteBlockButton(blockType: blockType) {
                            onBlockSelected(blockType)
                        }
                    }
                }
                .padding()
            }
            .background(Color.white)
        }
    }
}

// MARK: - Palette Block Button

struct PaletteBlockButton: View {
    let blockType: BlockType
    let action: () -> Void
    
    @State private var isPressed = false
    
    var body: some View {
        Button(action: {
            withAnimation(.spring(response: 0.3)) {
                isPressed = true
            }
            
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                withAnimation(.spring(response: 0.3)) {
                    isPressed = false
                }
            }
            
            action()
        }) {
            VStack(spacing: 8) {
                // Icon
                Image(systemName: iconForBlockType(blockType))
                    .font(.title2)
                    .foregroundColor(.white)
                
                // Label
                Text(blockType.rawValue)
                    .font(.caption)
                    .foregroundColor(.white)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
                    .fixedSize(horizontal: false, vertical: true)
            }
            .frame(width: 100, height: 90)
            .background(blockType.color)
            .cornerRadius(12)
            .shadow(color: blockType.color.opacity(0.3), radius: isPressed ? 2 : 5, y: isPressed ? 2 : 5)
            .scaleEffect(isPressed ? 0.95 : 1.0)
        }
        .buttonStyle(PlainButtonStyle())
    }
    
    private func iconForBlockType(_ type: BlockType) -> String {
        switch type {
        case .moveForward:
            return "arrow.up"
        case .turnLeft:
            return "arrow.turn.up.left"
        case .turnRight:
            return "arrow.turn.up.right"
        case .pickUp:
            return "hand.raised.fill"
        case .repeatLoop:
            return "repeat"
        case .ifCondition:
            return "questionmark.diamond"
        case .setVariable:
            return "equal.square"
        case .increaseVariable:
            return "plus.square"
        }
    }
}

// MARK: - Preview

struct BlockPaletteView_Previews: PreviewProvider {
    static var previews: some View {
        BlockPaletteView(
            availableBlocks: [
                .moveForward,
                .turnLeft,
                .turnRight,
                .repeatLoop,
                .ifCondition
            ],
            onBlockSelected: { blockType in
                print("Selected: \(blockType)")
            }
        )
        .frame(height: 150)
    }
}
