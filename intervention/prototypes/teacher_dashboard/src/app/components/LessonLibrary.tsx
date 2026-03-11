import { useState } from 'react';
import { Link } from 'react-router';
import { Search, Filter, Clock, BookOpen } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './ui/select';
import { lessons, searchLessons, type DifficultyLevel, type AgeGroup, type Topic } from '../lib/lessons';

export default function LessonLibrary() {
  const [searchQuery, setSearchQuery] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState<DifficultyLevel | 'all'>('all');
  const [ageFilter, setAgeFilter] = useState<AgeGroup | 'all'>('all');
  const [topicFilter, setTopicFilter] = useState<Topic | 'all'>('all');

  const filteredLessons = lessons.filter((lesson) => {
    const matchesSearch = searchQuery === '' || searchLessons(searchQuery).some(l => l.id === lesson.id);
    const matchesDifficulty = difficultyFilter === 'all' || lesson.difficulty === difficultyFilter;
    const matchesAge = ageFilter === 'all' || lesson.ageGroup === ageFilter;
    const matchesTopic = topicFilter === 'all' || lesson.topic === topicFilter;

    return matchesSearch && matchesDifficulty && matchesAge && matchesTopic;
  });

  const getDifficultyColor = (difficulty: DifficultyLevel) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-700';
      case 'intermediate': return 'bg-yellow-100 text-yellow-700';
      case 'advanced': return 'bg-red-100 text-red-700';
    }
  };

  return (
    <div className="space-y-6 pb-20 md:pb-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
          Lesson Library 📚
        </h1>
        <p className="text-gray-600 mt-2">
          Browse and assign curriculum-aligned coding lessons
        </p>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardContent className="p-6 space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <Input
              placeholder="Search lessons by title, topic, or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Filters */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Difficulty</label>
              <Select value={difficultyFilter} onValueChange={(value) => setDifficultyFilter(value as DifficultyLevel | 'all')}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Levels</SelectItem>
                  <SelectItem value="beginner">Beginner</SelectItem>
                  <SelectItem value="intermediate">Intermediate</SelectItem>
                  <SelectItem value="advanced">Advanced</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Age Group</label>
              <Select value={ageFilter} onValueChange={(value) => setAgeFilter(value as AgeGroup | 'all')}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Ages</SelectItem>
                  <SelectItem value="8-10">8-10 years</SelectItem>
                  <SelectItem value="10-12">10-12 years</SelectItem>
                  <SelectItem value="12-15">12-15 years</SelectItem>
                  <SelectItem value="15-18">15-18 years</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Topic</label>
              <Select value={topicFilter} onValueChange={(value) => setTopicFilter(value as Topic | 'all')}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Topics</SelectItem>
                  <SelectItem value="patterns">Patterns</SelectItem>
                  <SelectItem value="logic">Logic</SelectItem>
                  <SelectItem value="algorithms">Algorithms</SelectItem>
                  <SelectItem value="loops">Loops</SelectItem>
                  <SelectItem value="variables">Variables</SelectItem>
                  <SelectItem value="conditionals">Conditionals</SelectItem>
                  <SelectItem value="functions">Functions</SelectItem>
                  <SelectItem value="data-structures">Data Structures</SelectItem>
                  <SelectItem value="recursion">Recursion</SelectItem>
                  <SelectItem value="optimization">Optimization</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Filter className="w-4 h-4" />
            Showing {filteredLessons.length} of {lessons.length} lessons
          </div>
        </CardContent>
      </Card>

      {/* Lesson Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredLessons.map((lesson) => (
          <Card key={lesson.id} className="hover:shadow-xl transition-shadow overflow-hidden">
            {/* Video Thumbnail */}
            <div className="relative aspect-video bg-gray-200 overflow-hidden">
              <img
                src={lesson.thumbnailUrl}
                alt={lesson.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                <div className="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center">
                  <BookOpen className="w-8 h-8 text-purple-600" />
                </div>
              </div>
            </div>

            <CardHeader>
              <div className="flex items-start justify-between gap-2 mb-2">
                <Badge className={getDifficultyColor(lesson.difficulty)}>
                  {lesson.difficulty}
                </Badge>
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <Clock className="w-4 h-4" />
                  {lesson.duration} min
                </div>
              </div>
              <CardTitle className="text-lg">{lesson.title}</CardTitle>
              <CardDescription className="line-clamp-2">{lesson.description}</CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="flex flex-wrap gap-2">
                <Badge variant="outline" className="text-xs">{lesson.ageGroup} years</Badge>
                <Badge variant="outline" className="text-xs capitalize">{lesson.topic}</Badge>
              </div>

              <div className="space-y-2">
                <p className="text-sm font-medium">Learning Objectives:</p>
                <ul className="text-sm text-gray-600 space-y-1">
                  {lesson.learningObjectives.slice(0, 2).map((objective, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="text-purple-500 mt-0.5">•</span>
                      <span className="line-clamp-1">{objective}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <Link to={`/lessons/${lesson.id}`} className="block">
                <Button className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600">
                  View Lesson
                </Button>
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredLessons.length === 0 && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold mb-2">No lessons found</h3>
            <p className="text-gray-600">Try adjusting your search or filters</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
