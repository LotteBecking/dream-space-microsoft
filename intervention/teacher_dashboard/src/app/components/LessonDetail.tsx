import { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router';
import { ArrowLeft, Clock, Users, BookOpen, CheckCircle, Play, FileText } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { lessons } from '../lib/lessons';
import { saveLastLesson } from '../lib/teacherStorage';
import { toast } from 'sonner';

export default function LessonDetail() {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const lesson = lessons.find(l => l.id === lessonId);

  if (!lesson) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold mb-2">Lesson not found</h2>
        <Link to="/lessons">
          <Button>Back to Library</Button>
        </Link>
      </div>
    );
  }

  // Save as last viewed lesson
  useState(() => {
    saveLastLesson(lesson.id);
  });

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-700';
      case 'intermediate': return 'bg-yellow-100 text-yellow-700';
      case 'advanced': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const handleAssign = () => {
    toast.success('Lesson assigned to class!', {
      description: 'Students can now access this lesson in their dashboard'
    });
  };

  return (
    <div className="space-y-6 pb-20 md:pb-8">
      {/* Back Button */}
      <Link to="/lessons">
        <Button variant="ghost" size="sm">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Library
        </Button>
      </Link>

      {/* Lesson Header */}
      <div className="space-y-4">
        <div className="flex flex-wrap gap-2">
          <Badge className={getDifficultyColor(lesson.difficulty)}>
            {lesson.difficulty}
          </Badge>
          <Badge variant="outline">{lesson.ageGroup} years</Badge>
          <Badge variant="outline" className="capitalize">{lesson.topic}</Badge>
          <Badge variant="outline">
            <Clock className="w-3 h-3 mr-1" />
            {lesson.duration} min
          </Badge>
        </div>

        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
          {lesson.title}
        </h1>
        <p className="text-xl text-gray-600">{lesson.description}</p>

        <div className="flex gap-3">
          <Button 
            onClick={handleAssign}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
          >
            <Users className="w-4 h-4 mr-2" />
            Assign to Class
          </Button>
          <Button variant="outline">
            <FileText className="w-4 h-4 mr-2" />
            Download Materials
          </Button>
        </div>
      </div>

      {/* Video Player */}
      <Card className="overflow-hidden">
        <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50">
          <CardTitle className="flex items-center gap-2">
            <Play className="w-5 h-5 text-purple-600" />
            Lesson Video
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="relative aspect-video bg-gray-900">
            <iframe
              className="w-full h-full"
              src={lesson.videoUrl}
              title={lesson.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        </CardContent>
      </Card>

      {/* Lesson Content Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="instructions">Teacher Guide</TabsTrigger>
          <TabsTrigger value="exercises">Student Exercises</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          {/* Learning Objectives */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-600" />
                Learning Objectives
              </CardTitle>
              <CardDescription>What students will learn in this lesson</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {lesson.learningObjectives.map((objective, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-purple-600 text-sm font-semibold">{index + 1}</span>
                    </div>
                    <span className="text-gray-700">{objective}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Curriculum Alignment */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-600" />
                Curriculum Alignment
              </CardTitle>
              <CardDescription>Netherlands digital literacy standards</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {lesson.curriculumAlignment.map((standard, index) => (
                  <Badge key={index} variant="outline" className="text-sm">
                    {standard}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="instructions" className="space-y-6">
          {/* Setup Instructions */}
          <Card>
            <CardHeader>
              <CardTitle>Classroom Setup</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700">{lesson.teacherInstructions.setup}</p>
            </CardContent>
          </Card>

          {/* Step-by-Step Guide */}
          <Card>
            <CardHeader>
              <CardTitle>Step-by-Step Teaching Guide</CardTitle>
              <CardDescription>Follow these steps for a successful lesson</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {lesson.teacherInstructions.steps.map((step, index) => (
                  <div key={index} className="flex gap-4">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center flex-shrink-0">
                      <span className="text-white font-semibold">{index + 1}</span>
                    </div>
                    <div className="flex-1 pt-1">
                      <p className="text-gray-700">{step}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Discussion Prompts */}
          <Card className="bg-blue-50 border-blue-200">
            <CardHeader>
              <CardTitle className="text-blue-900">Discussion Prompts</CardTitle>
              <CardDescription className="text-blue-700">Questions to engage students</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {lesson.teacherInstructions.discussionPrompts.map((prompt, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="text-blue-600 font-semibold">💬</span>
                    <span className="text-gray-700">{prompt}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Teaching Tips */}
          <Card className="bg-green-50 border-green-200">
            <CardHeader>
              <CardTitle className="text-green-900">Teaching Tips</CardTitle>
              <CardDescription className="text-green-700">Best practices for this lesson</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {lesson.teacherInstructions.tips.map((tip, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="text-green-600">💡</span>
                    <span className="text-gray-700">{tip}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="exercises" className="space-y-4">
          {lesson.studentExercises.map((exercise, index) => (
            <Card key={index}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="flex items-center gap-2">
                      {exercise.title}
                      <Badge variant="outline" className="text-xs capitalize">{exercise.type}</Badge>
                    </CardTitle>
                    <CardDescription className="mt-2">{exercise.description}</CardDescription>
                  </div>
                  <Badge className={getDifficultyColor(exercise.difficulty)}>
                    {exercise.difficulty}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <Button variant="outline" size="sm">
                  Preview Exercise
                </Button>
              </CardContent>
            </Card>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  );
}
