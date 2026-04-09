import { createBrowserRouter, RouterProvider } from 'react-router'
import AppShell from '@/components/layout/AppShell'
import LessonLandingScreen from '@/screens/LessonLandingScreen'
import SimulatorScreen from '@/screens/SimulatorScreen'
import Exercise1Screen from '@/screens/Exercise1Screen'
import Exercise2Screen from '@/screens/Exercise2Screen'
import Exercise3Screen from '@/screens/Exercise3Screen'
import ChallengeScreen from '@/screens/ChallengeScreen'
import VocabReviewScreen from '@/screens/VocabReviewScreen'

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppShell />,
    children: [
      { index: true, element: <LessonLandingScreen /> },
      { path: 'simulator', element: <SimulatorScreen /> },
      { path: 'exercise/1', element: <Exercise1Screen /> },
      { path: 'exercise/2', element: <Exercise2Screen /> },
      { path: 'exercise/3', element: <Exercise3Screen /> },
      { path: 'challenge', element: <ChallengeScreen /> },
      { path: 'review', element: <VocabReviewScreen /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
