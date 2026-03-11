import { useState, useEffect } from 'react';
import { Link } from 'react-router';
import { Trophy, Flame, Target, Users, ChevronRight, Sparkles, Calendar } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { getDailyChallenge } from '../lib/challenges';
import { getProfile, getTodayResult, getStreak, getTotalPoints, saveResult, getTeams } from '../lib/storage';
import ChallengeCard from './ChallengeCard';

export default function Dashboard() {
  const [profile, setProfile] = useState(getProfile());
  const [todayChallenge] = useState(getDailyChallenge(new Date()));
  const [completed, setCompleted] = useState<boolean>(false);
  const [streak, setStreak] = useState(getStreak());
  const [totalPoints, setTotalPoints] = useState(getTotalPoints());
  const [showChallenge, setShowChallenge] = useState(false);
  const [teams] = useState(getTeams());

  useEffect(() => {
    const result = getTodayResult();
    if (result) {
      setCompleted(result.completed);
    }
  }, []);

  const handleChallengeComplete = (correct: boolean) => {
    const result = {
      challengeId: todayChallenge.id,
      completed: true,
      correct,
      date: new Date().toISOString(),
      points: correct ? todayChallenge.points : 0
    };
    
    saveResult(result);
    setCompleted(true);
    setStreak(getStreak());
    setTotalPoints(getTotalPoints());
    setShowChallenge(false);
  };

  const userTeam = teams.find(t => t.id === profile?.teamId);
  const sortedTeams = [...teams].sort((a, b) => b.totalPoints - a.totalPoints);
  const teamRank = sortedTeams.findIndex(t => t.id === profile?.teamId) + 1;

  return (
    <div className="space-y-6 pb-20 md:pb-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500 rounded-2xl p-8 text-white shadow-xl">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              Welcome back, {profile?.name}! {profile?.avatar}
            </h1>
            <p className="text-purple-100 text-lg">
              Ready to tackle today's coding challenge?
            </p>
          </div>
          <div className="hidden sm:block text-6xl">🎯</div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-4 mt-6">
          <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4">
            <div className="flex items-center gap-2 mb-1">
              <Flame className="w-5 h-5 text-orange-200" />
              <span className="text-sm opacity-90">Streak</span>
            </div>
            <div className="text-2xl font-bold">{streak} days</div>
          </div>
          
          <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4">
            <div className="flex items-center gap-2 mb-1">
              <Trophy className="w-5 h-5 text-yellow-200" />
              <span className="text-sm opacity-90">Points</span>
            </div>
            <div className="text-2xl font-bold">{totalPoints}</div>
          </div>
          
          <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4">
            <div className="flex items-center gap-2 mb-1">
              <Users className="w-5 h-5 text-blue-200" />
              <span className="text-sm opacity-90">Team Rank</span>
            </div>
            <div className="text-2xl font-bold">#{teamRank}</div>
          </div>
        </div>
      </div>

      {/* Daily Challenge Section */}
      <Card className="border-2 border-purple-200 shadow-lg">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Calendar className="w-5 h-5 text-purple-600" />
              <CardTitle>Today's Challenge</CardTitle>
            </div>
            <Badge variant="secondary" className="bg-purple-100 text-purple-700">
              {todayChallenge.difficulty}
            </Badge>
          </div>
          <CardDescription>Complete your daily challenge to keep your streak!</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-400 rounded-lg flex items-center justify-center text-2xl flex-shrink-0">
                🎯
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-lg mb-1">{todayChallenge.title}</h3>
                <p className="text-sm text-gray-600 mb-2">{todayChallenge.description}</p>
                <div className="flex items-center gap-3 text-sm">
                  <span className="flex items-center gap-1">
                    <Target className="w-4 h-4 text-purple-600" />
                    <span className="text-gray-600">{todayChallenge.category}</span>
                  </span>
                  <span className="flex items-center gap-1">
                    <Sparkles className="w-4 h-4 text-yellow-600" />
                    <span className="text-gray-600">{todayChallenge.points} points</span>
                  </span>
                </div>
              </div>
            </div>

            {completed ? (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center gap-3">
                <div className="text-2xl">✅</div>
                <div>
                  <div className="font-semibold text-green-800">Challenge Complete!</div>
                  <div className="text-sm text-green-600">Come back tomorrow for a new challenge</div>
                </div>
              </div>
            ) : (
              <Button 
                onClick={() => setShowChallenge(true)}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                size="lg"
              >
                Start Challenge
                <ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Quick Stats */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Team Progress */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="w-5 h-5 text-blue-600" />
              Your Team: {userTeam?.name}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">Team Progress</span>
                <span className="font-semibold">{userTeam?.totalPoints} pts</span>
              </div>
              <Progress value={(userTeam?.totalPoints || 0) / 15} className="h-2" />
            </div>
            
            <div className="space-y-2">
              {userTeam?.members.map((member) => (
                <div key={member.id} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{member.avatar}</span>
                    <span className="text-sm">{member.name}</span>
                  </div>
                  <span className="text-sm font-semibold text-purple-600">{member.points} pts</span>
                </div>
              ))}
            </div>

            <Link to="/teams">
              <Button variant="outline" className="w-full">
                View Leaderboard
                <ChevronRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Trophy className="w-5 h-5 text-yellow-600" />
              Quick Actions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link to="/challenges">
              <Button variant="outline" className="w-full justify-between">
                <span className="flex items-center gap-2">
                  <Target className="w-4 h-4" />
                  Browse All Challenges
                </span>
                <ChevronRight className="w-4 h-4" />
              </Button>
            </Link>
            
            <Link to="/progress">
              <Button variant="outline" className="w-full justify-between">
                <span className="flex items-center gap-2">
                  <Trophy className="w-4 h-4" />
                  View Your Progress
                </span>
                <ChevronRight className="w-4 h-4" />
              </Button>
            </Link>
            
            <Link to="/teams">
              <Button variant="outline" className="w-full justify-between">
                <span className="flex items-center gap-2">
                  <Users className="w-4 h-4" />
                  Team Competition
                </span>
                <ChevronRight className="w-4 h-4" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>

      {/* Challenge Modal */}
      {showChallenge && (
        <ChallengeCard
          challenge={todayChallenge}
          onComplete={handleChallengeComplete}
          onClose={() => setShowChallenge(false)}
        />
      )}
    </div>
  );
}
