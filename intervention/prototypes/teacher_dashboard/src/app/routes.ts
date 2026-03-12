import { createBrowserRouter } from "react-router";
import Root from "./layout/Root";
import TeacherHome from "../features/home/TeacherHome";
import LessonLibrary from "../features/lessons/LessonLibrary";
import LessonDetail from "../features/lessons/LessonDetail";
import ClassOverview from "../features/classes/ClassOverview";
import StudentList from "../features/students/StudentList";
import StudentProfile from "../features/students/StudentProfile";
import Profile from "../features/profile/Profile";

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