# KidsCodingiOS (SwiftUI)

iOS SwiftUI replication of the Kids Coding Learning App with:
- Onboarding (name + age)
- Dashboard daily challenge
- Challenge library + difficulty filters
- Progress analytics + achievements
- Team leaderboard (teams + individuals)
- Editable profile and recent activity

## Build locally

1. Generate the project:
   ```bash
   xcodegen generate
   ```
2. Open `KidsCodingiOS.xcodeproj` in Xcode.
3. Select an iOS simulator and run.

## Notes
- Data is persisted using `UserDefaults`.
- Team/member points update when a challenge is answered correctly.
