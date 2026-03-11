import { Outlet, Link, useLocation } from 'react-router';
import { Home, BookOpen, GraduationCap, Users, Settings } from 'lucide-react';
import { useEffect, useState } from 'react';
import { getTeacherProfile, saveTeacherProfile } from '../lib/teacherStorage';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { Toaster } from './Toaster';

export default function Root() {
  const location = useLocation();
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [school, setSchool] = useState('');

  useEffect(() => {
    const profile = getTeacherProfile();
    if (!profile) {
      setShowOnboarding(true);
    }
  }, []);

  const handleSaveProfile = () => {
    if (name && email && school) {
      saveTeacherProfile({
        name,
        email,
        school,
        avatar: '👨‍🏫'
      });
      
      setShowOnboarding(false);
    }
  };

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/lessons', icon: BookOpen, label: 'Lessons' },
    { path: '/classes', icon: GraduationCap, label: 'Classes' },
    { path: '/students', icon: Users, label: 'Students' },
    { path: '/settings', icon: Settings, label: 'Settings' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50">
      <Toaster />
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-purple-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <span className="text-2xl">👨‍🏫</span>
              </div>
              <span className="font-bold text-xl bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                Teacher Dashboard
              </span>
            </Link>
            
            <nav className="hidden md:flex gap-1">
              {navItems.map(item => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-purple-100 text-purple-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Mobile Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-md border-t border-purple-100">
        <div className="flex justify-around items-center h-16">
          {navItems.map(item => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex flex-col items-center gap-1 px-3 py-2 transition-colors ${
                  isActive ? 'text-purple-600' : 'text-gray-400'
                }`}
              >
                <Icon className="w-6 h-6" />
                <span className="text-xs">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Onboarding Dialog */}
      <Dialog open={showOnboarding} onOpenChange={setShowOnboarding}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-2xl">Welcome, Teacher! 👨‍🏫</DialogTitle>
            <DialogDescription>
              Let's set up your teacher dashboard. Tell us a bit about yourself.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="name">Your Name</Label>
              <Input
                id="name"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                placeholder="teacher@school.nl"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="school">School Name</Label>
              <Input
                id="school"
                placeholder="Your school name"
                value={school}
                onChange={(e) => setSchool(e.target.value)}
              />
            </div>

            <Button 
              onClick={handleSaveProfile} 
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
              disabled={!name || !email || !school}
            >
              Get Started! 🚀
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}