import SwiftUI

struct TeamsView: View {
    @EnvironmentObject private var store: AppStore

    @State private var showIndividuals = false

    var body: some View {
        List {
            if let team = store.userTeam, let profile = store.profile {
                Section("Your Team") {
                    HStack {
                        VStack(alignment: .leading, spacing: 6) {
                            Text(team.name).font(.headline)
                            Text("Rank #\(store.teamRank(for: profile.teamId))").foregroundStyle(.secondary)
                        }
                        Spacer()
                        Text("\(team.totalPoints) pts")
                            .font(.headline)
                            .foregroundStyle(.purple)
                    }

                    HStack {
                        metric("Members", "\(team.members.count)", "person.3.fill", .blue)
                        metric("Avg", "\(Int(team.totalPoints / max(team.members.count, 1)))", "chart.line.uptrend.xyaxis", .green)
                        metric("Total", "\(team.totalPoints)", "trophy.fill", .yellow)
                    }

                    ForEach(team.members) { member in
                        HStack {
                            Text(member.avatar)
                            Text(member.name)
                            Spacer()
                            Text("\(member.points)")
                                .foregroundStyle(.purple)
                        }
                    }
                }
            }

            Section {
                Picker("Leaderboard", selection: $showIndividuals) {
                    Text("Teams").tag(false)
                    Text("Top Coders").tag(true)
                }
                .pickerStyle(.segmented)
            }

            if !showIndividuals {
                Section("Team Rankings") {
                    ForEach(Array(store.sortedTeams.enumerated()), id: \.element.id) { index, team in
                        teamRankRow(rank: index + 1, team: team)
                    }
                }
            } else {
                Section("Top Coders") {
                    ForEach(Array(store.allRankedMembers.enumerated()), id: \.element.id) { index, member in
                        memberRankRow(rank: index + 1, member: member)
                    }
                }
            }

            Section("How Competition Works") {
                Text("• Complete daily challenges to earn points for you and your team")
                Text("• Team score is the sum of member points")
                Text("• Rankings update as challenges are completed")
                Text("• Collaborate to climb the leaderboard")
            }
        }
        .navigationTitle("Team Competition")
    }

    private func metric(_ title: String, _ value: String, _ icon: String, _ color: Color) -> some View {
        VStack(spacing: 4) {
            Image(systemName: icon).foregroundStyle(color)
            Text(value).font(.headline)
            Text(title).font(.caption2).foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
    }

    private func teamRankRow(rank: Int, team: Team) -> some View {
        HStack {
            rankView(rank)
            VStack(alignment: .leading) {
                Text(team.name).font(.headline)
                Text("\(team.members.count) members · \(Int(team.totalPoints / max(team.members.count, 1))) avg")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            Spacer()
            Text("\(team.totalPoints)")
                .font(.headline)
                .foregroundStyle(.purple)
        }
        .padding(.vertical, 4)
    }

    private func memberRankRow(rank: Int, member: RankedMember) -> some View {
        HStack {
            rankView(rank)
            Text(member.avatar)
            VStack(alignment: .leading) {
                Text(member.name).font(.headline)
                Text(member.teamName).font(.caption).foregroundStyle(.secondary)
            }
            Spacer()
            Text("\(member.points)")
                .font(.headline)
                .foregroundStyle(.purple)
        }
        .padding(.vertical, 4)
    }

    private func rankView(_ rank: Int) -> some View {
        let symbol: String
        let color: Color
        switch rank {
        case 1:
            symbol = "crown.fill"
            color = .yellow
        case 2:
            symbol = "medal.fill"
            color = .gray
        case 3:
            symbol = "medal.fill"
            color = .orange
        default:
            symbol = "\(rank).circle.fill"
            color = .blue
        }

        return Image(systemName: symbol)
            .foregroundStyle(color)
            .frame(width: 26)
    }
}
