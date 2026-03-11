import { useState, useEffect } from 'react';
import { Link } from 'react-router';
import { Play, BookOpen, Users, TrendingUp, Calendar, Clock } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { getClasses, getLastLesson, saveLastLesson } from '../lib/teacherStorage';
import { lessons } from '../lib/lessons';

export default function TeacherHome() {
  const [classes, setClasses] = useState(getClasses());
  const [lastLessonId, setLastLessonId] = useState(getLastLesson());

  const featuredLesson = lessons[0];
  const lastLesson = lastLessonId ? lessons.find(l => l.id === lastLessonId) : null;

  const totalStudents = classes.reduce((sum, c) => sum + c.studentCount, 0);
  const totalAssignments = classes.reduce((sum, c) => sum + c.activeAssignments, 0);
  const avgEngagement = Math.round(classes.reduce((sum, c) => sum + c.engagementRate, 0) / classes.length);

  return (
    <div className="space-y-6 pb-20 md:pb-8">
      {/* Welcome Header */}
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
          Welcome Back, Teacher! 👋
        </h1>
        <p className="text-gray-600">
          Let's inspire young minds with coding today
        </p>
      </div>

      {/* Featured Lesson with Video */}
      <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <Badge className="mb-2 bg-purple-500">Featured Lesson ⭐</Badge>
              <CardTitle className="text-2xl">{featuredLesson.title}</CardTitle>
              <CardDescription className="mt-2">{featuredLesson.description}</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Video Player */}
          <div className="relative aspect-video rounded-lg overflow-hidden bg-gray-900">
            <iframe
              className="w-full h-full"
              src={featuredLesson.videoUrl}
              title={featuredLesson.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>

          {/* Lesson Info */}
          <div className="flex flex-wrap gap-3">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Clock className="w-4 h-4" />
              {featuredLesson.duration} min
            </div>
            <Badge variant="outline">{featuredLesson.difficulty}</Badge>
            <Badge variant="outline">{featuredLesson.ageGroup} years</Badge>
            <Badge variant="outline">{featuredLesson.topic}</Badge>
          </div>

          <div className="flex gap-2">
            <Link to={`/lessons/${featuredLesson.id}`} className="flex-1">
              <Button className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600">
                <BookOpen className="w-4 h-4 mr-2" />
                View Full Lesson
              </Button>
            </Link>
            <Link to="/assign" className="flex-1">
              <Button variant="outline" className="w-full">
                Assign to Class
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>

      {/* Continue Last Lesson */}
      {lastLesson && (
        <Card className="border-blue-200 bg-blue-50">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-blue-600" />
              Continue Where You Left Off
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{lastLesson.title}</p>
                <p className="text-sm text-gray-600">{lastLesson.description}</p>
              </div>
              <Link to={`/lessons/${lastLesson.id}`}>
                <Button variant="outline" size="sm">
                  <Play className="w-4 h-4 mr-2" />
                  Continue
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          ⚡ Quick Actions
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Link to="/lessons">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-purple-200 hover:border-purple-400">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <h3 className="font-semibold">Browse Lessons</h3>
                  <p className="text-sm text-gray-600">Explore {lessons.length} lessons</p>
                </div>
              </CardContent>
            </Card>
          </Link>

          <Link to="/classes">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-blue-200 hover:border-blue-400">
              <CardContent className="p-6 flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                  <Users className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold">View Classes</h3>
                  <p className="text-sm text-gray-600">{classes.length} active classes</p>
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>
      </div>

      {/* Class Snapshot */}
      <div>
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          📊 Class Snapshot
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Total Students</p>
                  <p className="text-3xl font-bold text-green-700">{totalStudents}</p>
                </div>
                <div className="w-12 h-12 rounded-full bg-green-200 flex items-center justify-center">
                  <Users className="w-6 h-6 text-green-700" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-50 to-amber-50 border-orange-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Active Assignments</p>
                  <p className="text-3xl font-bold text-orange-700">{totalAssignments}</p>
                </div>
                <div className="w-12 h-12 rounded-full bg-orange-200 flex items-center justify-center">
                  <Calendar className="w-6 h-6 text-orange-700" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Avg. Engagement</p>
                  <p className="text-3xl font-bold text-blue-700">{avgEngagement}%</p>
                </div>
                <div className="w-12 h-12 rounded-full bg-blue-200 flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-blue-700" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Recent Classes */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold flex items-center gap-2">
            🎓 Your Classes
          </h2>
          <Link to="/classes">
            <Button variant="ghost" size="sm">View All</Button>
          </Link>
        </div>
        <div className="grid grid-cols-1 gap-4">
          {classes.slice(0, 3).map((classItem) => (
            <Card key={classItem.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">{classItem.name}</h3>
                    <div className="flex gap-4 mt-2 text-sm text-gray-600">
                      <span className="flex items-center gap-1">
                        <Users className="w-4 h-4" />
                        {classItem.studentCount} students
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {classItem.activeAssignments} assignments
                      </span>
                      <span className="flex items-center gap-1">
                        <TrendingUp className="w-4 h-4" />
                        {classItem.engagementRate}% engaged
                      </span>
                    </div>
                  </div>
                  <Link to={`/classes/${classItem.id}`}>
                    <Button variant="outline" size="sm">View Class</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
