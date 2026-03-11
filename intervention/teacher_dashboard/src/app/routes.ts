import { createBrowserRouter } from "react-router";
import Root from "./components/Root";
import TeacherHome from "./components/TeacherHome";
import LessonLibrary from "./components/LessonLibrary";
import LessonDetail from "./components/LessonDetail";
import ClassOverview from "./components/ClassOverview";
import StudentList from "./components/StudentList";
import StudentProfile from "./components/StudentProfile";
import Profile from "./components/Profile";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      { index: true, Component: TeacherHome },
      { path: "lessons", Component: LessonLibrary },
      { path: "lessons/:lessonId", Component: LessonDetail },
      { path: "classes", Component: ClassOverview },
      { path: "students", Component: StudentList },
      { path: "students/:studentId", Component: StudentProfile },
      { path: "settings", Component: Profile },
    ],
  },
]);