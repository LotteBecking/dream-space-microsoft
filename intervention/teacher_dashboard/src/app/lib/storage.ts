export interface UserProfile {
  name: string;
  age: number;
  teamId: string;
  avatar: string;
}

export interface ChallengeResult {
  challengeId: string;
  completed: boolean;
  correct: boolean;
  date: string;
  points: number;
}

export interface TeamMember {
  id: string;
  name: string;
  avatar: string;
  points: number;
}

export interface Team {
  id: string;
  name: string;
  members: TeamMember[];
  totalPoints: number;
}

const STORAGE_KEYS = {
  PROFILE: 'codequest_profile',
  RESULTS: 'codequest_results',
  TEAMS: 'codequest_teams'
};

// User Profile
export function saveProfile(profile: UserProfile): void {
  localStorage.setItem(STORAGE_KEYS.PROFILE, JSON.stringify(profile));
}

export function getProfile(): UserProfile | null {
  const data = localStorage.getItem(STORAGE_KEYS.PROFILE);
  return data ? JSON.parse(data) : null;
}

// Challenge Results
export function saveResult(result: ChallengeResult): void {
  const results = getResults();
  results.push(result);
  localStorage.setItem(STORAGE_KEYS.RESULTS, JSON.stringify(results));
}

export function getResults(): ChallengeResult[] {
  const data = localStorage.getItem(STORAGE_KEYS.RESULTS);
  return data ? JSON.parse(data) : [];
}

export function getTodayResult(): ChallengeResult | null {
  const today = new Date().toDateString();
  const results = getResults();
  return results.find(r => new Date(r.date).toDateString() === today) || null;
}

export function getStreak(): number {
  const results = getResults();
  if (results.length === 0) return 0;
  
  let streak = 0;
  const today = new Date();
  
  for (let i = 0; i < 365; i++) {
    const checkDate = new Date(today);
    checkDate.setDate(checkDate.getDate() - i);
    const dateString = checkDate.toDateString();
    
    const hasResult = results.some(r => 
      new Date(r.date).toDateString() === dateString && r.completed
    );
    
    if (hasResult) {
      streak++;
    } else if (i > 0) {
      break;
    }
  }
  
  return streak;
}

export function getTotalPoints(): number {
  const results = getResults();
  return results.reduce((sum, r) => sum + (r.correct ? r.points : 0), 0);
}

// Teams
export function getTeams(): Team[] {
  const data = localStorage.getItem(STORAGE_KEYS.TEAMS);
  if (data) {
    return JSON.parse(data);
  }
  
  // Default teams with mock data
  const defaultTeams: Team[] = [
    {
      id: 'team-1',
      name: 'Code Warriors',
      totalPoints: 1250,
      members: [
        { id: '1', name: 'Alex', avatar: '👦', points: 450 },
        { id: '2', name: 'Sam', avatar: '👧', points: 380 },
        { id: '3', name: 'Jordan', avatar: '🧒', points: 420 }
      ]
    },
    {
      id: 'team-2',
      name: 'Algorithm Wizards',
      totalPoints: 1180,
      members: [
        { id: '4', name: 'Taylor', avatar: '👦', points: 410 },
        { id: '5', name: 'Morgan', avatar: '👧', points: 390 },
        { id: '6', name: 'Casey', avatar: '🧒', points: 380 }
      ]
    },
    {
      id: 'team-3',
      name: 'Binary Builders',
      totalPoints: 1050,
      members: [
        { id: '7', name: 'Riley', avatar: '👦', points: 360 },
        { id: '8', name: 'Quinn', avatar: '👧', points: 350 },
        { id: '9', name: 'Avery', avatar: '🧒', points: 340 }
      ]
    },
    {
      id: 'team-4',
      name: 'Logic Masters',
      totalPoints: 920,
      members: [
        { id: '10', name: 'Jamie', avatar: '👦', points: 320 },
        { id: '11', name: 'Drew', avatar: '👧', points: 310 },
        { id: '12', name: 'Skyler', avatar: '🧒', points: 290 }
      ]
    }
  ];
  
  localStorage.setItem(STORAGE_KEYS.TEAMS, JSON.stringify(defaultTeams));
  return defaultTeams;
}

export function updateTeamMemberPoints(teamId: string, memberId: string, additionalPoints: number): void {
  const teams = getTeams();
  const team = teams.find(t => t.id === teamId);
  
  if (team) {
    const member = team.members.find(m => m.id === memberId);
    if (member) {
      member.points += additionalPoints;
      team.totalPoints = team.members.reduce((sum, m) => sum + m.points, 0);
      localStorage.setItem(STORAGE_KEYS.TEAMS, JSON.stringify(teams));
    }
  }
}
