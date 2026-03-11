import { useState } from 'react';
import { useParams, Link } from 'react-router';
import { ArrowLeft, Award, BookOpen, TrendingUp, Calendar, Edit, Save } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Textarea } from './ui/textarea';
import { getStudentById, updateStudentNotes } from '../lib/teacherStorage';
import { toast } from 'sonner';

export default function StudentProfile() {
  const { studentId } = useParams();
  const student = getStudentById(studentId || '');
  const [isEditingNotes, setIsEditingNotes] = useState(false);
  const [notes, setNotes] = useState(student?.teacherNotes || '');

  if (!student) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold mb-2">Student not found</h2>
        <Link to="/students">
          <Button>Back to Students</Button>
        </Link>
      </div>
    );
  }

  const handleSaveNotes = () => {
    updateStudentNotes(student.id, notes);
    setIsEditingNotes(false);
    toast.success('Notes saved successfully!');
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="space-y-6 pb-20 md:pb-8">
      {/* Back Button */}
      <Link to="/students">
        <Button variant="ghost" size="sm">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Students
        </Button>
      </Link>

      {/* Student Header */}
      <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
        <CardContent className="p-6">
          <div className="flex items-start gap-6">
            <Avatar className="w-24 h-24 text-4xl">
              <AvatarFallback className="bg-gradient-to-br from-purple-400 to-pink-400 text-white">
                {student.avatar}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                {student.name}
              </h1>
              <div className="flex items-center gap-4 mt-2 text-gray-600">
                <span className="flex items-center gap-1">
                  <BookOpen className="w-4 h-4" />
                  {student.lessonsCompleted} lessons
                </span>
                <span className="flex items-center gap-1">
                  <TrendingUp className="w-4 h-4" />
                  {student.challengesCompleted} challenges
                </span>
                <span className="flex items-center gap-1">
                  <Award className="w-4 h-4" />
                  {student.achievements.length} achievements
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Progress Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Learning Progress</CardTitle>
            <CardDescription>Overall completion rate</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600">{student.progressPercentage}%</div>
              <p className="text-sm text-gray-600 mt-1">Complete</p>
            </div>
            <Progress value={student.progressPercentage} className="h-3" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Lessons Completed</CardTitle>
            <CardDescription>Video lessons watched</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600">{student.lessonsCompleted}</div>
              <p className="text-sm text-gray-600 mt-1">Lessons</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Challenges Solved</CardTitle>
            <CardDescription>Coding challenges completed</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600">{student.challengesCompleted}</div>
              <p className="text-sm text-gray-600 mt-1">Challenges</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Achievements */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Award className="w-5 h-5 text-yellow-600" />
            Achievements & Badges
          </CardTitle>
          <CardDescription>Badges earned for completing milestones</CardDescription>
        </CardHeader>
        <CardContent>
          {student.achievements.length > 0 ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              {student.achievements.map((achievement) => (
                <div
                  key={achievement.id}
                  className="bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-200 rounded-lg p-4 text-center hover:shadow-lg transition-shadow"
                >
                  <div className="text-4xl mb-2">{achievement.icon}</div>
                  <h4 className="font-semibold text-sm mb-1">{achievement.name}</h4>
                  <p className="text-xs text-gray-600">
                    {new Date(achievement.earnedDate).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Award className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>No achievements yet</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Activity History */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="w-5 h-5 text-blue-600" />
            Recent Activity
          </CardTitle>
          <CardDescription>Latest lessons and challenges</CardDescription>
        </CardHeader>
        <CardContent>
          {student.activityHistory.length > 0 ? (
            <div className="space-y-3">
              {student.activityHistory.map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-start gap-4 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                    activity.success ? 'bg-green-100' : 'bg-red-100'
                  }`}>
                    {activity.type === 'lesson' && <BookOpen className="w-5 h-5 text-green-600" />}
                    {activity.type === 'challenge' && <TrendingUp className="w-5 h-5 text-green-600" />}
                    {activity.type === 'achievement' && <Award className="w-5 h-5 text-yellow-600" />}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-semibold">{activity.title}</h4>
                        <p className="text-sm text-gray-600">{formatDate(activity.date)}</p>
                      </div>
                      <Badge variant={activity.success ? "default" : "destructive"}>
                        {activity.success ? 'Completed' : 'Failed'}
                      </Badge>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Calendar className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>No activity yet</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Teacher Notes */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Edit className="w-5 h-5 text-purple-600" />
                Teacher Notes
              </CardTitle>
              <CardDescription>Private notes about this student</CardDescription>
            </div>
            {!isEditingNotes ? (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsEditingNotes(true)}
              >
                <Edit className="w-4 h-4 mr-2" />
                Edit
              </Button>
            ) : (
              <Button
                size="sm"
                onClick={handleSaveNotes}
                className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
              >
                <Save className="w-4 h-4 mr-2" />
                Save
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {isEditingNotes ? (
            <Textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Add notes about this student's progress, strengths, areas for improvement, etc."
              className="min-h-[150px]"
            />
          ) : (
            <div className="min-h-[100px] p-4 bg-gray-50 rounded-lg">
              {student.teacherNotes ? (
                <p className="text-gray-700 whitespace-pre-wrap">{student.teacherNotes}</p>
              ) : (
                <p className="text-gray-400 italic">No notes yet. Click Edit to add notes.</p>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
