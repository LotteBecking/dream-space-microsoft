import { useState } from 'react';
import { Target, Trophy, Filter } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { challenges, DifficultyLevel } from '../lib/challenges';
import { getProfile, saveResult, getResults } from '../lib/storage';
import ChallengeCard from './ChallengeCard';

export default function Challenges() {
  const [selectedChallenge, setSelectedChallenge] = useState<any>(null);
  const [filter, setFilter] = useState<DifficultyLevel | 'all'>('all');
  const profile = getProfile();
  const completedChallenges = getResults();

  const handleChallengeComplete = (correct: boolean) => {
    if (selectedChallenge) {
      const result = {
        challengeId: selectedChallenge.id,
        completed: true,
        correct,
        date: new Date().toISOString(),
        points: correct ? selectedChallenge.points : 0
      };
      
      saveResult(result);
      setSelectedChallenge(null);
    }
  };

  const isChallengeCompleted = (challengeId: string) => {
    return completedChallenges.some(r => r.challengeId === challengeId && r.completed);
  };

  const filteredChallenges = filter === 'all' 
    ? challenges 
    : challenges.filter(c => c.difficulty === filter);

  const getChallengesByAge = () => {
    if (!profile) return challenges;
    
    const age = profile.age;
    if (age >= 8 && age <= 12) {
      return filteredChallenges.filter(c => c.ageGroup === '8-12');
    } else if (age >= 13 && age <= 15) {
      return filteredChallenges.filter(c => c.ageGroup === '8-12' || c.ageGroup === '12-15');
    }
    return filteredChallenges;
  };

  const ageFilteredChallenges = getChallengesByAge();

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-700';
      case 'intermediate': return 'bg-yellow-100 text-yellow-700';
      case 'advanced': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="space-y-6 pb-20 md:pb-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Challenge Library</h1>
        <p className="text-gray-600">Test your skills with coding challenges at every level</p>
      </div>

      {/* Stats */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{ageFilteredChallenges.length}</div>
                <div className="text-sm text-gray-600">Total Challenges</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Trophy className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{completedChallenges.length}</div>
                <div className="text-sm text-gray-600">Completed</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Filter className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">
                  {Math.round((completedChallenges.length / ageFilteredChallenges.length) * 100) || 0}%
                </div>
                <div className="text-sm text-gray-600">Progress</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Tabs value={filter} onValueChange={(value) => setFilter(value as any)} className="w-full">
        <TabsList className="grid w-full md:w-auto grid-cols-4">
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="beginner">Beginner</TabsTrigger>
          <TabsTrigger value="intermediate">Intermediate</TabsTrigger>
          <TabsTrigger value="advanced">Advanced</TabsTrigger>
        </TabsList>

        <TabsContent value={filter} className="mt-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {ageFilteredChallenges.map((challenge) => {
              const completed = isChallengeCompleted(challenge.id);
              
              return (
                <Card 
                  key={challenge.id}
                  className={`hover:shadow-lg transition-shadow ${
                    completed ? 'border-green-200 bg-green-50/30' : ''
                  }`}
                >
                  <CardHeader>
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Badge className={getDifficultyColor(challenge.difficulty)}>
                            {challenge.difficulty}
                          </Badge>
                          {completed && (
                            <Badge className="bg-green-100 text-green-700">
                              ✓ Done
                            </Badge>
                          )}
                        </div>
                        <CardTitle className="text-lg">{challenge.title}</CardTitle>
                      </div>
                      <div className="text-2xl">
                        {challenge.category === 'Patterns' && '🔄'}
                        {challenge.category === 'Logic' && '🧩'}
                        {challenge.category === 'Algorithms' && '⚙️'}
                        {challenge.category === 'Loops' && '🔁'}
                        {challenge.category === 'Variables' && '📦'}
                        {challenge.category === 'Conditionals' && '🔀'}
                        {challenge.category === 'Functions' && '🎯'}
                        {challenge.category === 'Data Structures' && '📊'}
                        {challenge.category === 'Recursion' && '🌀'}
                        {challenge.category === 'Optimization' && '⚡'}
                      </div>
                    </div>
                    <CardDescription>{challenge.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span>🎯 {challenge.category}</span>
                        <span>⭐ {challenge.points} pts</span>
                      </div>
                      <Button
                        onClick={() => setSelectedChallenge(challenge)}
                        size="sm"
                        variant={completed ? "outline" : "default"}
                        className={!completed ? "bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600" : ""}
                      >
                        {completed ? 'Retry' : 'Start'}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {ageFilteredChallenges.length === 0 && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-2">No challenges found</h3>
              <p className="text-gray-600">Try selecting a different difficulty level</p>
            </div>
          )}
        </TabsContent>
      </Tabs>

      {/* Challenge Modal */}
      {selectedChallenge && (
        <ChallengeCard
          challenge={selectedChallenge}
          onComplete={handleChallengeComplete}
          onClose={() => setSelectedChallenge(null)}
        />
      )}
    </div>
  );
}
