import { useState } from 'react';
import { Trophy, Users, Medal, TrendingUp, Crown } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { getTeams, getProfile } from '../lib/storage';

export default function Teams() {
  const teams = getTeams();
  const profile = getProfile();
  const [view, setView] = useState<'teams' | 'individuals'>('teams');

  const sortedTeams = [...teams].sort((a, b) => b.totalPoints - a.totalPoints);
  
  const allMembers = teams.flatMap(team => 
    team.members.map(member => ({
      ...member,
      teamName: team.name,
      teamId: team.id
    }))
  ).sort((a, b) => b.points - a.points);

  const userTeam = teams.find(t => t.id === profile?.teamId);
  const teamRank = sortedTeams.findIndex(t => t.id === profile?.teamId) + 1;

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1: return <Crown className="w-5 h-5 text-yellow-500" />;
      case 2: return <Medal className="w-5 h-5 text-gray-400" />;
      case 3: return <Medal className="w-5 h-5 text-orange-600" />;
      default: return null;
    }
  };

  const getRankBadge = (rank: number) => {
    switch (rank) {
      case 1: return 'bg-yellow-100 text-yellow-700';
      case 2: return 'bg-gray-100 text-gray-700';
      case 3: return 'bg-orange-100 text-orange-700';
      default: return 'bg-blue-100 text-blue-700';
    }
  };

  return (
    <div className="space-y-6 pb-20 md:pb-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Team Competition</h1>
        <p className="text-gray-600">Compete with other teams and climb the leaderboard!</p>
      </div>

      {/* Your Team Stats */}
      {userTeam && (
        <Card className="border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-pink-50">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle className="text-2xl flex items-center gap-2">
                  {getRankIcon(teamRank)}
                  {userTeam.name}
                </CardTitle>
                <CardDescription>Your team's current standing</CardDescription>
              </div>
              <Badge className={getRankBadge(teamRank)}>
                Rank #{teamRank}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg p-4">
                <div className="flex items-center gap-2 mb-1">
                  <Trophy className="w-4 h-4 text-purple-600" />
                  <span className="text-sm text-gray-600">Total Points</span>
                </div>
                <div className="text-2xl font-bold">{userTeam.totalPoints}</div>
              </div>
              
              <div className="bg-white rounded-lg p-4">
                <div className="flex items-center gap-2 mb-1">
                  <Users className="w-4 h-4 text-blue-600" />
                  <span className="text-sm text-gray-600">Team Members</span>
                </div>
                <div className="text-2xl font-bold">{userTeam.members.length}</div>
              </div>
              
              <div className="bg-white rounded-lg p-4">
                <div className="flex items-center gap-2 mb-1">
                  <TrendingUp className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-gray-600">Avg per Member</span>
                </div>
                <div className="text-2xl font-bold">
                  {Math.round(userTeam.totalPoints / userTeam.members.length)}
                </div>
              </div>
            </div>

            {/* Team Members */}
            <div className="mt-4 space-y-2">
              <h3 className="font-semibold text-sm text-gray-700">Your Teammates:</h3>
              <div className="grid md:grid-cols-3 gap-2">
                {userTeam.members.map((member) => (
                  <div 
                    key={member.id}
                    className="bg-white rounded-lg p-3 flex items-center gap-2"
                  >
                    <span className="text-2xl">{member.avatar}</span>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium truncate">{member.name}</div>
                      <div className="text-sm text-purple-600">{member.points} pts</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Leaderboard */}
      <Tabs value={view} onValueChange={(value) => setView(value as any)} className="w-full">
        <TabsList className="grid w-full md:w-auto grid-cols-2">
          <TabsTrigger value="teams" className="flex items-center gap-2">
            <Users className="w-4 h-4" />
            Teams
          </TabsTrigger>
          <TabsTrigger value="individuals" className="flex items-center gap-2">
            <Trophy className="w-4 h-4" />
            Top Coders
          </TabsTrigger>
        </TabsList>

        {/* Team Leaderboard */}
        <TabsContent value="teams" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Trophy className="w-5 h-5 text-yellow-600" />
                Team Rankings
              </CardTitle>
              <CardDescription>Current standings of all teams</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {sortedTeams.map((team, index) => {
                  const rank = index + 1;
                  const isUserTeam = team.id === profile?.teamId;
                  
                  return (
                    <div
                      key={team.id}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        isUserTeam
                          ? 'border-purple-300 bg-purple-50'
                          : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-lg flex items-center justify-center font-bold text-lg ${
                          rank === 1 ? 'bg-yellow-100 text-yellow-700' :
                          rank === 2 ? 'bg-gray-100 text-gray-700' :
                          rank === 3 ? 'bg-orange-100 text-orange-700' :
                          'bg-blue-50 text-blue-600'
                        }`}>
                          {getRankIcon(rank) || `#${rank}`}
                        </div>
                        
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className="font-semibold text-lg">{team.name}</h3>
                            {isUserTeam && (
                              <Badge className="bg-purple-100 text-purple-700">Your Team</Badge>
                            )}
                          </div>
                          <div className="flex items-center gap-4 text-sm text-gray-600">
                            <span>{team.members.length} members</span>
                            <span>•</span>
                            <span>{Math.round(team.totalPoints / team.members.length)} avg pts</span>
                          </div>
                        </div>
                        
                        <div className="text-right">
                          <div className="text-2xl font-bold text-purple-600">
                            {team.totalPoints}
                          </div>
                          <div className="text-sm text-gray-600">total points</div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Individual Leaderboard */}
        <TabsContent value="individuals" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Medal className="w-5 h-5 text-purple-600" />
                Top Coders
              </CardTitle>
              <CardDescription>Individual rankings across all teams</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {allMembers.map((member, index) => {
                  const rank = index + 1;
                  const isCurrentUser = member.name === profile?.name;
                  
                  return (
                    <div
                      key={`${member.teamId}-${member.id}`}
                      className={`p-4 rounded-lg border transition-all ${
                        isCurrentUser
                          ? 'border-purple-300 bg-purple-50'
                          : 'border-gray-200 hover:bg-gray-50'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold ${
                          rank === 1 ? 'bg-yellow-100 text-yellow-700' :
                          rank === 2 ? 'bg-gray-100 text-gray-700' :
                          rank === 3 ? 'bg-orange-100 text-orange-700' :
                          'bg-blue-50 text-blue-600'
                        }`}>
                          {rank <= 3 ? getRankIcon(rank) : rank}
                        </div>
                        
                        <span className="text-3xl">{member.avatar}</span>
                        
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold">{member.name}</span>
                            {isCurrentUser && (
                              <Badge className="bg-purple-100 text-purple-700">You</Badge>
                            )}
                          </div>
                          <div className="text-sm text-gray-600">{member.teamName}</div>
                        </div>
                        
                        <div className="text-right">
                          <div className="text-xl font-bold text-purple-600">
                            {member.points}
                          </div>
                          <div className="text-xs text-gray-600">points</div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Competition Info */}
      <Card className="border-blue-200 bg-blue-50/50">
        <CardHeader>
          <CardTitle className="text-lg">💡 How Team Competition Works</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-gray-700">
          <p>• Complete daily challenges to earn points for yourself and your team</p>
          <p>• Your team's score is the sum of all members' points</p>
          <p>• Rankings update in real-time as challenges are completed</p>
          <p>• Work together with your teammates to climb the leaderboard!</p>
        </CardContent>
      </Card>
    </div>
  );
}
