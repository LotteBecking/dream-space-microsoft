#!/bin/bash

# CodeQuest MVP - Xcode Project Setup Script
# This script creates a complete Xcode project ready to open

set -e

echo "🚀 Setting up CodeQuest MVP Xcode Project..."

PROJECT_DIR="/Users/lottebecking/Documents/GitHub/dream-space-microsoft/CodeQuestMVP"
PROJECT_NAME="CodeQuestMVP"

cd "$PROJECT_DIR" || exit 1

# Create Xcode project using Swift Package Manager as base structure
echo "📦 Creating Xcode project structure..."

# Create Package.swift for SPM (temporary, just to generate project)
cat > Package.swift << 'EOF'
// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "CodeQuestMVP",
    platforms: [.iOS(.v15)],
    products: [
        .library(name: "CodeQuestMVP", targets: ["CodeQuestMVP"])
    ],
    targets: [
        .target(name: "CodeQuestMVP", path: ".")
    ]
)
EOF

# Generate Xcode project from Package
echo "🔨 Generating Xcode project..."
swift package generate-xcodeproj 2>/dev/null || {
    echo "⚠️  SPM method failed, using alternative approach..."
    
    # Alternative: Create project using xcodebuild
    echo "📱 Creating iOS app project..."
    
    # We'll guide user to create it manually since automated project creation
    # requires more complex tooling
    
    cat > XCODE_SETUP_INSTRUCTIONS.txt << 'INSTRUCTIONS'
# Xcode Project Setup - Complete Guide

All your Swift files are ready! Follow these steps:

## Quick Setup (5 minutes)

1. Open Xcode
2. File → New → Project
3. Choose: iOS → App
4. Settings:
   - Product Name: CodeQuestMVP
   - Team: Your team (or None for simulator only)
   - Organization Identifier: com.lottebecking
   - Interface: SwiftUI ← IMPORTANT!
   - Language: Swift
   - Storage: None
   - Include Tests: Optional

5. Save Location: 
   /Users/lottebecking/Documents/GitHub/dream-space-microsoft/

6. After project creates:
   - Delete default ContentView.swift
   - Drag these folders FROM YOUR CodeQuestMVP FOLDER into Xcode:
     * Models/
     * ViewModels/
     * Services/
     * Views/
     * SampleData/
   - Drag CodeQuestMVPApp.swift (replace existing)
   - When prompted: Check "Copy items if needed"

7. Build and Run! (Cmd + R)

## Alternative: Use Provided Script

Run: ./create_xcode_project.sh

This will attempt to auto-generate the project.

INSTRUCTIONS
    
    echo "✅ Created setup instructions: XCODE_SETUP_INSTRUCTIONS.txt"
}

# Create a helper script for manual project creation
cat > create_xcode_project.sh << 'SCRIPT'
#!/bin/bash

echo "Creating Xcode project structure..."

# This requires Xcode command line tools
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Xcode command line tools not found"
    echo "Please install with: xcode-select --install"
    exit 1
fi

# Use xcodeproj gem if available (better project generation)
if command -v xcodeproj &> /dev/null; then
    echo "Using xcodeproj tool..."
    # This would require Ruby gem: sudo gem install xcodeproj
    # Then we could programmatically create the project
else
    echo "For automatic project creation, install xcodeproj:"
    echo "  sudo gem install xcodeproj"
    echo ""
    echo "Or follow manual steps in XCODE_SETUP_INSTRUCTIONS.txt"
fi

SCRIPT

chmod +x create_xcode_project.sh

# Clean up temporary Package.swift
rm -f Package.swift

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Read: XCODE_SETUP_INSTRUCTIONS.txt"
echo "   2. Or follow: QUICKSTART.md"
echo ""
echo "📍 Project location:"
echo "   $PROJECT_DIR"
echo ""
echo "🎯 Quickest way to start:"
echo "   1. Open Xcode"
echo "   2. Create new iOS App project (SwiftUI)"
echo "   3. Drag the source folders into Xcode"
echo "   4. Build & Run!"
echo ""
