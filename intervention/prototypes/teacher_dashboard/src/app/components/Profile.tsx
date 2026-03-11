import { useState } from 'react';
import { Mail, School, User, Edit, Save } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Avatar, AvatarFallback } from './ui/avatar';
import { getTeacherProfile, saveTeacherProfile } from '../lib/teacherStorage';
import { toast } from 'sonner';

export default function Profile() {
  const profile = getTeacherProfile();
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(profile?.name || '');
  const [email, setEmail] = useState(profile?.email || '');
  const [school, setSchool] = useState(profile?.school || '');

  const handleSave = () => {
    if (name && email && school) {
      saveTeacherProfile({
        name,
        email,
        school,
        avatar: profile?.avatar || '👨‍🏫'
      });
      setIsEditing(false);
      toast.success('Profile updated successfully!');
    }
  };

  const handleCancel = () => {
    setName(profile?.name || '');
    setEmail(profile?.email || '');
    setSchool(profile?.school || '');
    setIsEditing(false);
  };

  return (
    <div className="space-y-6 pb-20 md:pb-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
          Settings ⚙️
        </h1>
        <p className="text-gray-600 mt-2">
          Manage your teacher profile and preferences
        </p>
      </div>

      {/* Profile Card */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Teacher Profile</CardTitle>
              <CardDescription>Your personal information</CardDescription>
            </div>
            {!isEditing ? (
              <Button
                variant="outline"
                onClick={() => setIsEditing(true)}
              >
                <Edit className="w-4 h-4 mr-2" />
                Edit
              </Button>
            ) : (
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  onClick={handleCancel}
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleSave}
                  className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                >
                  <Save className="w-4 h-4 mr-2" />
                  Save
                </Button>
              </div>
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Avatar */}
          <div className="flex items-center gap-6">
            <Avatar className="w-24 h-24 text-4xl">
              <AvatarFallback className="bg-gradient-to-br from-purple-400 to-pink-400 text-white">
                {profile?.avatar || '👨‍🏫'}
              </AvatarFallback>
            </Avatar>
            <div>
              <h3 className="text-xl font-semibold">{profile?.name || 'Teacher'}</h3>
              <p className="text-gray-600">{profile?.school || 'School'}</p>
            </div>
          </div>

          {/* Form Fields */}
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name" className="flex items-center gap-2">
                <User className="w-4 h-4" />
                Full Name
              </Label>
              {isEditing ? (
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your name"
                />
              ) : (
                <p className="p-3 bg-gray-50 rounded-lg">{profile?.name || 'Not set'}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="flex items-center gap-2">
                <Mail className="w-4 h-4" />
                Email Address
              </Label>
              {isEditing ? (
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="teacher@school.nl"
                />
              ) : (
                <p className="p-3 bg-gray-50 rounded-lg">{profile?.email || 'Not set'}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="school" className="flex items-center gap-2">
                <School className="w-4 h-4" />
                School Name
              </Label>
              {isEditing ? (
                <Input
                  id="school"
                  value={school}
                  onChange={(e) => setSchool(e.target.value)}
                  placeholder="Your school"
                />
              ) : (
                <p className="p-3 bg-gray-50 rounded-lg">{profile?.school || 'Not set'}</p>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* About Section */}
      <Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
        <CardHeader>
          <CardTitle>About This Dashboard</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-gray-700">
          <p>
            This teacher dashboard is part of the Dream Space digital literacy intervention,
            designed to help integrate computational thinking into everyday classroom practice.
          </p>
          <ul className="space-y-2">
            <li className="flex items-start gap-2">
              <span className="text-purple-600">📚</span>
              <span>Access curriculum-aligned coding lessons with video content</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-purple-600">👥</span>
              <span>Track student progress and engagement in real-time</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-purple-600">🎯</span>
              <span>Assign lessons and monitor completion rates</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-purple-600">📊</span>
              <span>View detailed analytics and learning insights</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}