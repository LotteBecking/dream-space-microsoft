import { useMemo } from 'react';
import { Trophy, TrendingUp, Calendar, Flame, Target, Award } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Progress as ProgressBar } from './ui/progress';
import { Badge } from './ui/badge';
import { getResults, getStreak, getTotalPoints } from '../lib/storage';
import { challenges } from '../lib/challenges';

export default function Progress() {
  const results = getResults();
  const streak = getStreak();
  const totalPoints = getTotalPoints();

  const stats = useMemo(() => {
    const completed = results.filter(r => r.completed).length;
    const correct = results.filter(r => r.correct).length;
    const accuracy = completed > 0 ? Math.round((correct / completed) * 100) : 0;
    
    // Calculate category performance
    const categoryStats = new Map<string, { total: number; correct: number }>();
    results.forEach(result => {
      const challenge = challenges.find(c => c.id === result.challengeId);
      if (challenge) {
        const current = categoryStats.get(challenge.category) || { total: 0, correct: 0 };
        categoryStats.set(challenge.category, {
          total: current.total + 1,
          correct: current.correct + (result.correct ? 1 : 0)
        });
      }
    });

    // Calculate weekly progress
    const weeklyProgress = Array(7).fill(0);
    const today = new Date();
    results.forEach(result => {
      const resultDate = new Date(result.date);
      const dayDiff = Math.floor((today.getTime() - resultDate.getTime()) / (1000 * 60 * 60 * 24));
      if (dayDiff >= 0 && dayDiff < 7 && result.correct) {
        weeklyProgress[6 - dayDiff] += result.points;
      }
    });

    return {
      completed,
      correct,
      accuracy,
      categoryStats,
      weeklyProgress
    };
  }, [results]);

  const achievements = [
    {
      id: 'first-challenge',
      title: 'First Steps',
      description: 'Complete your first challenge',
      icon: '🎯',
      unlocked: results.length > 0
    },
    {
      id: 'streak-3',
      title: '3-Day Streak',
      description: 'Complete challenges 3 days in a row',
      icon: '🔥',
      unlocked: streak >= 3
    },
    {
      id: 'streak-7',
      title: 'Week Warrior',
      description: 'Maintain a 7-day streak',
      icon: '⭐',
      unlocked: streak >= 7
    },
    {
      id: 'points-100',
      title: 'Century Club',
      description: 'Earn 100 points',
      icon: '💯',
      unlocked: totalPoints >= 100
    },
    {
      id: 'perfect-score',
      title: 'Perfect Score',
      description: 'Get 5 challenges correct in a row',
      icon: '🏆',
      unlocked: stats.accuracy === 100 && results.length >= 5
    },
    {
      id: 'challenge-master',
      title: 'Challenge Master',
      description: 'Complete 10 challenges',
      icon: '🎓',
      unlocked: stats.completed >= 10
    }
  ];

  const maxWeeklyPoints = Math.max(...stats.weeklyProgress, 1);
  const dayLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  return (
    <div className="space-y-6 pb-20 md:pb-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Your Progress</h1>
        <p className="text-gray-600">Track your learning journey and achievements</p>
      </div>

      {/* Key Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Trophy className="w-6 h-6 text-yellow-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{totalPoints}</div>
                <div className="text-sm text-gray-600">Total Points</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <Flame className="w-6 h-6 text-orange-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{streak}</div>
                <div className="text-sm text-gray-600">Day Streak</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.accuracy}%</div>
                <div className="text-sm text-gray-600">Accuracy</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Calendar className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{stats.completed}</div>
                <div className="text-sm text-gray-600">Completed</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Weekly Activity */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            Weekly Activity
          </CardTitle>
          <CardDescription>Points earned each day this week</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-end gap-2 h-48">
            {stats.weeklyProgress.map((points, index) => (
              <div key={index} className="flex-1 flex flex-col items-center gap-2">
                <div className="w-full bg-gray-100 rounded-lg flex items-end justify-center relative group">
                  <div
                    className="w-full bg-gradient-to-t from-purple-500 to-pink-500 rounded-lg transition-all hover:opacity-80 cursor-pointer"
                    style={{ 
                      height: `${Math.max((points / maxWeeklyPoints) * 160, points > 0 ? 20 : 0)}px`,
                      minHeight: points > 0 ? '20px' : '0'
                    }}
                  >
                    <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                      {points} points
                    </div>
                  </div>
                </div>
                <span className="text-xs text-gray-600">{dayLabels[index]}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Category Performance */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Target className="w-5 h-5 text-purple-600" />
            Category Performance
          </CardTitle>
          <CardDescription>Your performance across different topics</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.from(stats.categoryStats.entries()).map(([category, data]) => {
              const percentage = Math.round((data.correct / data.total) * 100);
              
              return (
                <div key={category}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">{category}</span>
                    <span className="text-sm text-gray-600">
                      {data.correct}/{data.total} correct ({percentage}%)
                    </span>
                  </div>
                  <ProgressBar value={percentage} className="h-2" />
                </div>
              );
            })}
            
            {stats.categoryStats.size === 0 && (
              <div className="text-center py-8 text-gray-500">
                Complete some challenges to see your category performance!
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Achievements */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Award className="w-5 h-5 text-yellow-600" />
            Achievements
          </CardTitle>
          <CardDescription>
            {achievements.filter(a => a.unlocked).length} of {achievements.length} unlocked
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {achievements.map((achievement) => (
              <div
                key={achievement.id}
                className={`p-4 rounded-lg border-2 transition-all ${
                  achievement.unlocked
                    ? 'border-yellow-200 bg-yellow-50'
                    : 'border-gray-200 bg-gray-50 opacity-60'
                }`}
              >
                <div className="flex items-start gap-3">
                  <div className="text-3xl">{achievement.icon}</div>
                  <div className="flex-1">
                    <h3 className="font-semibold mb-1">{achievement.title}</h3>
                    <p className="text-sm text-gray-600">{achievement.description}</p>
                    {achievement.unlocked && (
                      <Badge className="mt-2 bg-yellow-100 text-yellow-700">
                        Unlocked!
                      </Badge>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
