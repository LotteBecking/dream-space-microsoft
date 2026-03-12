import { useState } from 'react';
import { useSearchParams, Link } from 'react-router';
import { Search, Filter, Clock, Award, BookOpen, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../shared/ui/card';
import { Input } from '../../shared/ui/input';
import { Badge } from '../../shared/ui/badge';
import { Progress } from '../../shared/ui/progress';
import { Avatar, AvatarFallback } from '../../shared/ui/avatar';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../shared/ui/select';
import { getStudents, getClasses } from '../../shared/data/teacherStorage';

export default function StudentList() {
  const [searchParams] = useSearchParams();
  const classFilter = searchParams.get('class') || 'all';
  
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedClass, setSelectedClass] = useState(classFilter);
  
  const students = getStudents();
  const classes = getClasses();

  const filteredStudents = students.filter((student) => {
    const matchesSearch = searchQuery === '' || 
      student.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesClass = selectedClass === 'all' || student.classId === selectedClass;
    return matchesSearch && matchesClass;
  });

  const getActivityColor = (lastActivity: string) => {
    const hours = (Date.now() - new Date(lastActivity).getTime()) / (1000 * 60 * 60);
    if (hours < 24) return 'text-green-600';
    if (hours < 48) return 'text-yellow-600';
    return 'text-gray-600';
  };

  const formatLastActivity = (lastActivity: string) => {
    const hours = Math.floor((Date.now() - new Date(lastActivity).getTime()) / (1000 * 60 * 60));
    if (hours < 1) return 'Just now';
    if (hours === 1) return '1 hour ago';
    if (hours < 24) return `${hours} hours ago`;
    const days = Math.floor(hours / 24);
    if (days === 1) return '1 day ago';
    return `${days} days ago`;
  };

  return (
    <div className="space-y-6 pb-20 md:pb-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
          Student Progress 📊
        </h1>
        <p className="text-gray-600 mt-2">
          Monitor individual student progress and achievements
        </p>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                placeholder="Search students by name..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Class Filter */}
            <div>
              <Select value={selectedClass} onValueChange={setSelectedClass}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by class" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Classes</SelectItem>
                  {classes.map((classItem) => (
                    <SelectItem key={classItem.id} value={classItem.id}>
                      {classItem.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Filter className="w-4 h-4" />
            Showing {filteredStudents.length} of {students.length} students
          </div>
        </CardContent>
      </Card>

      {/* Student Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredStudents.map((student) => {
          const studentClass = classes.find(c => c.id === student.classId);
          
          return (
            <Link key={student.id} to={`/students/${student.id}`}>
              <Card className="hover:shadow-xl transition-shadow cursor-pointer h-full">
                <CardHeader>
                  <div className="flex items-start gap-4">
                    <Avatar className="w-16 h-16 text-2xl">
                      <AvatarFallback className="bg-gradient-to-br from-purple-400 to-pink-400 text-white">
                        {student.avatar}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <CardTitle className="truncate">{student.name}</CardTitle>
                      <CardDescription className="mt-1">
                        {studentClass?.name || 'No class'}
                      </CardDescription>
                      <div className={`flex items-center gap-1 text-xs mt-2 ${getActivityColor(student.lastActivity)}`}>
                        <Clock className="w-3 h-3" />
                        {formatLastActivity(student.lastActivity)}
                      </div>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  {/* Progress */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Overall Progress</span>
                      <span className="font-semibold text-purple-600">{student.progressPercentage}%</span>
                    </div>
                    <Progress value={student.progressPercentage} className="h-2" />
                  </div>

                  {/* Stats */}
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-blue-50 rounded-lg p-3 text-center">
                      <div className="flex items-center justify-center gap-1 text-blue-600 mb-1">
                        <BookOpen className="w-4 h-4" />
                      </div>
                      <p className="text-xl font-bold text-blue-700">{student.lessonsCompleted}</p>
                      <p className="text-xs text-blue-600">Lessons</p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-3 text-center">
                      <div className="flex items-center justify-center gap-1 text-green-600 mb-1">
                        <TrendingUp className="w-4 h-4" />
                      </div>
                      <p className="text-xl font-bold text-green-700">{student.challengesCompleted}</p>
                      <p className="text-xs text-green-600">Challenges</p>
                    </div>
                  </div>

                  {/* Achievements */}
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Award className="w-4 h-4" />
                      <span>Achievements ({student.achievements.length})</span>
                    </div>
                    <div className="flex gap-1 flex-wrap">
                      {student.achievements.slice(0, 5).map((achievement) => (
                        <div
                          key={achievement.id}
                          className="w-8 h-8 rounded-full bg-gradient-to-br from-yellow-400 to-orange-400 flex items-center justify-center text-sm"
                          title={achievement.name}
                        >
                          {achievement.icon}
                        </div>
                      ))}
                      {student.achievements.length > 5 && (
                        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-600">
                          +{student.achievements.length - 5}
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>

      {/* Empty State */}
      {filteredStudents.length === 0 && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="text-6xl mb-4">👨‍🎓</div>
            <h3 className="text-xl font-semibold mb-2">No students found</h3>
            <p className="text-gray-600">Try adjusting your search or filters</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
