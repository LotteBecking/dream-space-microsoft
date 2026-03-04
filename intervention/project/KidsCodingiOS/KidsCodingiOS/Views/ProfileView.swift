import SwiftUI

struct ProfileView: View {
    @EnvironmentObject private var store: AppStore

    @State private var isEditing = false
    @State private var editName = ""
    @State private var editAge = 10

    private var completed: Int {
        store.results.filter(\.completed).count
    }

    private var correct: Int {
        store.results.filter(\.correct).count
    }

    private var accuracy: Int {
        guard !store.results.isEmpty else { return 0 }
        return Int((Double(correct) / Double(store.results.count)) * 100)
    }

    var body: some View {
        List {
            if let profile = store.profile {
                Section("Profile") {
                    if !isEditing {
                        HStack(spacing: 16) {
                            Text(profile.avatar)
                                .font(.system(size: 56))
                            VStack(alignment: .leading, spacing: 4) {
                                Text(profile.name).font(.title3.bold())
                                Text("\(profile.age) years old")
                                    .foregroundStyle(.secondary)
                                Text(store.userTeam?.name ?? "No Team")
                                    .font(.caption)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.purple.opacity(0.15), in: Capsule())
                            }
                            Spacer()
                        }

                        Button("Edit Profile") {
                            editName = profile.name
                            editAge = profile.age
                            isEditing = true
                        }
                    } else {
                        TextField("Name", text: $editName)
                        Picker("Age", selection: $editAge) {
                            ForEach(8...18, id: \.self) { age in
                                Text("\(age)").tag(age)
                            }
                        }

                        HStack {
                            Button("Cancel", role: .cancel) {
                                isEditing = false
                            }
                            Spacer()
                            Button("Save") {
                                store.updateProfile(name: editName.trimmingCharacters(in: .whitespacesAndNewlines), age: editAge)
                                isEditing = false
                            }
                            .disabled(editName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                        }
                    }
                }

                Section("Stats") {
                    HStack {
                        stat("Points", "\(store.totalPoints)", "trophy.fill", .yellow)
                        stat("Streak", "\(store.streak)", "flame.fill", .orange)
                        stat("Accuracy", "\(accuracy)%", "target", .green)
                        stat("Completed", "\(completed)", "checkmark.circle", .purple)
                    }
                }

                Section("Learning Summary") {
                    ProgressRow(label: "Challenges Completed", value: Double(completed), total: Double(ChallengeData.all.count))
                    ProgressRow(label: "Correct Answers", value: Double(correct), total: Double(max(completed, 1)))
                    ProgressRow(label: "Current Streak", value: Double(store.streak), total: 7)
                }

                Section("Recent Activity") {
                    let recent = Array(store.results.suffix(5).reversed())

                    if recent.isEmpty {
                        Text("No activity yet. Start completing challenges!")
                            .foregroundStyle(.secondary)
                    } else {
                        ForEach(recent) { result in
                            HStack {
                                Image(systemName: result.correct ? "checkmark.circle.fill" : "xmark.circle.fill")
                                    .foregroundStyle(result.correct ? .green : .red)
                                VStack(alignment: .leading) {
                                    Text(ChallengeData.challenge(by: result.challengeId)?.title ?? result.challengeId)
                                    Text(result.date, style: .date)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                                Spacer()
                                Text("+\(result.points)")
                                    .foregroundStyle(.purple)
                            }
                        }
                    }
                }
            } else {
                ContentUnavailableView("No Profile Found", systemImage: "person.crop.circle", description: Text("Complete onboarding to create your profile."))
            }
        }
        .navigationTitle("My Profile")
    }

    private func stat(_ title: String, _ value: String, _ icon: String, _ color: Color) -> some View {
        VStack(spacing: 4) {
            Image(systemName: icon).foregroundStyle(color)
            Text(value).font(.headline)
            Text(title).font(.caption2).foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
    }
}

private struct ProgressRow: View {
    let label: String
    let value: Double
    let total: Double

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text(label)
                    .font(.subheadline)
                Spacer()
                Text("\(Int(value))/\(Int(max(total, 1)))")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            SwiftUI.ProgressView(value: min(value, max(total, 1)), total: max(total, 1))
        }
    }
}
