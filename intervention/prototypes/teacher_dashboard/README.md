
  # Teacher Dashboard

  This folder contains the teacher dashboard prototype. The current app is a Vite + React project styled with Tailwind CSS.

  ## Keep Vs Generate

  You do not need to keep `node_modules` or `dist` in the project folder.

  - Keep: source files, config files, `package.json`, and `package-lock.json`
  - Generate when needed: `node_modules`, `dist`

  With the local `.gitignore`, the project can stay focused on the main source files while dependencies are reinstalled when needed.

  ## Install And Run

  Run `npm install` to install dependencies.

  Run `npm run dev` to start the development server.

  Run `npm run build` to create a production build.

  ## Project Map

  Use this as a quick text guide when browsing the files.

  - `index.html`: Vite HTML entry
  - `package.json`: project scripts and dependency list
  - `vite.config.ts`: Vite configuration
  - `guidelines/Guidelines.md`: design or content notes
  - `src/main.tsx`: app bootstrap entry
  - `src/app/App.tsx`: app root that mounts the router
  - `src/app/routes.ts`: route definitions for the dashboard screens
  - `src/app/layout/Root.tsx`: shared app shell, navigation, and onboarding dialog
  - `src/features/home/TeacherHome.tsx`: dashboard landing page
  - `src/features/lessons/LessonLibrary.tsx`: searchable lesson list
  - `src/features/lessons/LessonDetail.tsx`: single lesson detail view
  - `src/features/lessons/lessons.ts`: lesson data and lesson search helpers
  - `src/features/classes/ClassOverview.tsx`: class management overview
  - `src/features/students/StudentList.tsx`: student list and filters
  - `src/features/students/StudentProfile.tsx`: detailed student progress page
  - `src/features/profile/Profile.tsx`: teacher profile settings
  - `src/shared/ui/`: shared UI building blocks used by the pages
  - `src/shared/ui/Toaster.tsx`: toast notification wrapper
  - `src/shared/data/teacherStorage.ts`: local data storage helpers for classes, students, and profile state
  - `src/styles/index.css`: main style entry point
  - `src/styles/tailwind.css`: Tailwind import and source scanning setup
  - `src/styles/theme.css`: theme variables and shared visual styling
  - `src/styles/fonts.css`: font imports and font rules
  - `src/imports/pasted_text/teacher-dashboard.md`: imported planning/reference text, not core runtime logic

  The source is now organized by responsibility:

  - `app`: app entry, router, and top-level layout
  - `features`: user-facing screens grouped by feature area
  - `shared/ui`: reusable presentational building blocks
  - `shared/data`: local storage and shared data helpers

  ## Styling Choice

  The current project already uses Tailwind CSS.

  - Current approach: Tailwind utility classes plus small shared UI wrappers in `src/shared/ui/`
  - Recommended for this project: keep Tailwind, because the existing screens are already built around it
  - Bootstrap option: possible, but it would be a separate styling approach rather than something to mix casually into the current codebase

  ## Tailwind Vs Bootstrap

  Choose Tailwind if you want:

  - fast visual tweaks directly in components
  - consistent reuse of the existing UI files
  - the smallest amount of refactoring from the current state

  Choose Bootstrap if you want:

  - prebuilt layout and component conventions
  - less custom utility-class styling in JSX
  - a future refactor away from the current Tailwind-based component styling

  Using both at once is possible, but usually not a good cleanup move because it adds two styling systems to the same prototype.

  ## Suggested Cleanup Path

  If you want the folder to feel smaller and easier to navigate, the practical approach is:

  1. Keep the source files and config files.
  2. Ignore and remove `node_modules` and `dist` when not needed.
  3. Remove `.DS_Store` files if you want a cleaner file count.
  4. Review whether `src/imports/pasted_text/teacher-dashboard.md` is still needed.
  