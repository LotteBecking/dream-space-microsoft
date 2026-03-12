import { useState } from 'react';
import { Link } from 'react-router';
import { Users, Calendar, TrendingUp, Plus, GraduationCap } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../shared/ui/card';
import { Button } from '../../shared/ui/button';
import { Progress } from '../../shared/ui/progress';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '../../shared/ui/dialog';
import { Input } from '../../shared/ui/input';
import { Label } from '../../shared/ui/label';
import { getClasses, addClass, type Class } from '../../shared/data/teacherStorage';
import { toast } from 'sonner';

export default function ClassOverview() {
  const [classes, setClasses] = useState(getClasses());
  const [showDialog, setShowDialog] = useState(false);
  const [newClassName, setNewClassName] = useState('');

  const handleCreateClass = () => {
    if (!newClassName.trim()) {
      toast.error('Please enter a class name');
      return;
    }

    const newClass: Class = {
      id: `class-${Date.now()}`,
      name: newClassName,
      studentCount: 0,
      activeAssignments: 0,
      engagementRate: 0,
      students: []
    };

    addClass(newClass);
    setClasses(getClasses());
    setNewClassName('');
    setShowDialog(false);
    toast.success('Class created successfully! 🎉');
  };

  const totalStudents = classes.reduce((sum, c) => sum + c.studentCount, 0);
  const avgEngagement = classes.length > 0
    ? Math.round(classes.reduce((sum, c) => sum + c.engagementRate, 0) / classes.length)
    : 0;

  return (
    <div className="space-y-6 pb-20 md:pb-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            My Classes 🎓
          </h1>
          <p className="text-gray-600 mt-2">
            Manage your classes and track student progress
          </p>
        </div>
        <Dialog open={showDialog} onOpenChange={setShowDialog}>
          <DialogTrigger asChild>
            <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600">
              <Plus className="w-4 h-4 mr-2" />
              New Class
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Class</DialogTitle>
              <DialogDescription>
                Add a new class to organize your students
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="className">Class Name</Label>
                <Input
                  id="className"
                  placeholder="e.g., Class 4A"
                  value={newClassName}
                  onChange={(e) => setNewClassName(e.target.value)}
                />
              </div>
              <Button 
                onClick={handleCreateClass}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
              >
                Create Class
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Classes</p>
                <p className="text-3xl font-bold text-purple-700">{classes.length}</p>
              </div>
              <div className="w-12 h-12 rounded-full bg-purple-200 flex items-center justify-center">
                <GraduationCap className="w-6 h-6 text-purple-700" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Students</p>
                <p className="text-3xl font-bold text-blue-700">{totalStudents}</p>
              </div>
              <div className="w-12 h-12 rounded-full bg-blue-200 flex items-center justify-center">
                <Users className="w-6 h-6 text-blue-700" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Avg. Engagement</p>
                <p className="text-3xl font-bold text-green-700">{avgEngagement}%</p>
              </div>
              <div className="w-12 h-12 rounded-full bg-green-200 flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-green-700" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Class List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {classes.map((classItem) => (
          <Card key={classItem.id} className="hover:shadow-xl transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-2xl">{classItem.name}</CardTitle>
                  <CardDescription className="mt-2">
                    Active class with ongoing assignments
                  </CardDescription>
                </div>
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center text-2xl">
                  🎒
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Class Stats */}
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-center gap-1 text-gray-600 mb-1">
                    <Users className="w-4 h-4" />
                  </div>
                  <p className="text-2xl font-bold text-gray-800">{classItem.studentCount}</p>
                  <p className="text-xs text-gray-600">Students</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-center gap-1 text-gray-600 mb-1">
                    <Calendar className="w-4 h-4" />
                  </div>
                  <p className="text-2xl font-bold text-gray-800">{classItem.activeAssignments}</p>
                  <p className="text-xs text-gray-600">Assignments</p>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-center gap-1 text-gray-600 mb-1">
                    <TrendingUp className="w-4 h-4" />
                  </div>
                  <p className="text-2xl font-bold text-gray-800">{classItem.engagementRate}%</p>
                  <p className="text-xs text-gray-600">Engaged</p>
                </div>
              </div>

              {/* Engagement Progress */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Class Engagement</span>
                  <span className="font-semibold text-purple-600">{classItem.engagementRate}%</span>
                </div>
                <Progress value={classItem.engagementRate} className="h-2" />
              </div>

              {/* Action Button */}
              <Link to={`/students?class=${classItem.id}`}>
                <Button className="w-full" variant="outline">
                  View Students
                </Button>
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {classes.length === 0 && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="text-6xl mb-4">🎓</div>
            <h3 className="text-xl font-semibold mb-2">No classes yet</h3>
            <p className="text-gray-600 mb-6">Create your first class to get started</p>
            <Button 
              onClick={() => setShowDialog(true)}
              className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
            >
              <Plus className="w-4 h-4 mr-2" />
              Create Your First Class
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
