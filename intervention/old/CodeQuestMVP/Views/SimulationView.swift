//
//  SimulationView.swift
//  CodeQuest MVP
//
//  Visual grid showing robot, obstacles, goal, and items
//

import SwiftUI

struct SimulationView: View {
    let mission: Mission
    let robotState: RobotState
    let executionHistory: [Position]
    
    var body: some View {
        VStack(spacing: 10) {
            Text("Simulation")
                .font(.headline)
                .padding(.top)
            
            // Grid
            GeometryReader { geometry in
                let cellSize = min(
                    geometry.size.width / CGFloat(mission.gridSize.width),
                    geometry.size.height / CGFloat(mission.gridSize.height)
                ) * 0.9
                
                let gridWidth = cellSize * CGFloat(mission.gridSize.width)
                let gridHeight = cellSize * CGFloat(mission.gridSize.height)
                
                VStack(spacing: 0) {
                    ForEach(0..<mission.gridSize.height, id: \.self) { row in
                        HStack(spacing: 0) {
                            ForEach(0..<mission.gridSize.width, id: \.self) { col in
                                GridCell(
                                    position: Position(x: col, y: row),
                                    cellSize: cellSize,
                                    mission: mission,
                                    robotState: robotState,
                                    executionHistory: executionHistory
                                )
                            }
                        }
                    }
                }
                .frame(width: gridWidth, height: gridHeight)
                .position(x: geometry.size.width / 2, y: geometry.size.height / 2)
            }
            
            // Legend
            HStack(spacing: 15) {
                LegendItem(symbol: "🤖", label: "Robot")
                LegendItem(symbol: "🎯", label: "Goal")
                LegendItem(symbol: "🧱", label: "Obstacle")
            }
            .font(.caption)
            .padding(.bottom)
        }
        .background(Color(red: 0.98, green: 0.98, blue: 1.0))
    }
}

// MARK: - Grid Cell

struct GridCell: View {
    let position: Position
    let cellSize: CGFloat
    let mission: Mission
    let robotState: RobotState
    let executionHistory: [Position]
    
    var isRobot: Bool {
        robotState.position == position
    }
    
    var isGoal: Bool {
        mission.goalPosition == position
    }
    
    var isObstacle: Bool {
        mission.obstacles.contains(position)
    }
    
    var isItem: Bool {
        mission.items.contains(position)
    }
    
    var hasVisited: Bool {
        executionHistory.contains(position)
    }
    
    var body: some View {
        ZStack {
            // Cell background
            Rectangle()
                .fill(hasVisited ? Color.blue.opacity(0.1) : Color.white)
                .border(Color.gray.opacity(0.3), width: 1)
            
            // Content
            if isObstacle {
                Text("🧱")
                    .font(.system(size: cellSize * 0.6))
            } else if isGoal {
                Text("🎯")
                    .font(.system(size: cellSize * 0.6))
            } else if isItem && !robotState.itemsCollected.description.contains("\(position.x),\(position.y)") {
                Text("⭐")
                    .font(.system(size: cellSize * 0.5))
            }
            
            // Robot (rendered on top)
            if isRobot {
                RobotView(direction: robotState.direction, size: cellSize * 0.7)
            }
        }
        .frame(width: cellSize, height: cellSize)
    }
}

// MARK: - Robot View

struct RobotView: View {
    let direction: Direction
    let size: CGFloat
    
    var rotation: Double {
        switch direction {
        case .north: return 0
        case .east: return 90
        case .south: return 180
        case .west: return 270
        }
    }
    
    var body: some View {
        Text("🤖")
            .font(.system(size: size))
            .rotationEffect(.degrees(rotation))
            .animation(.easeInOut(duration: 0.3), value: rotation)
    }
}

// MARK: - Legend Item

struct LegendItem: View {
    let symbol: String
    let label: String
    
    var body: some View {
        HStack(spacing: 4) {
            Text(symbol)
            Text(label)
                .foregroundColor(.secondary)
        }
    }
}

// MARK: - Preview

struct SimulationView_Previews: PreviewProvider {
    static var previews: some View {
        let mission = Mission(
            levelId: UUID(),
            title: "Test",
            description: "Test mission",
            difficulty: .easy,
            estimatedMinutes: 5,
            conceptsFocused: [.movement],
            availableBlocks: [.moveForward],
            gridSize: GridSize(width: 5, height: 5),
            startPosition: Position(x: 0, y: 0),
            goalPosition: Position(x: 4, y: 4),
            obstacles: [Position(x: 2, y: 2)],
            optimalSolutionLength: 5
        )
        
        SimulationView(
            mission: mission,
            robotState: RobotState(position: Position(x: 0, y: 0)),
            executionHistory: [Position(x: 0, y: 0)]
        )
        .frame(height: 400)
    }
}
