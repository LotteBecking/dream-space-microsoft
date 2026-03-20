# Teacher Dashboard (Python)

This folder contains the teacher dashboard implemented as a Python Flask web application with HTML and Tailwind CSS.

This is a port of the React/Vite dashboard to a Python backend with Jinja2 templates.

## Features

- Teacher dashboard landing page
- Lesson library with search
- Lesson detail view
- Class overview and management
- Student list with filtering
- Student progress profiles
- Teacher settings

## Install and Run

### Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running

Start the development server:
```bash
python app.py
```

The app will be available at `http://localhost:5000`

## Project Structure

- `app.py`: Main Flask application and routes
- `data/`: Data storage and management modules
  - `teacher_storage.py`: Teacher profile, classes, students, and assignments storage
  - `lessons.py`: Lesson data
- `templates/`: Jinja2 HTML templates
  - `base.html`: Base layout with navigation
  - `home.html`: Dashboard home
  - `lessons/`: Lesson-related pages
  - `classes/`: Class management pages
  - `students/`: Student-related pages
  - `profile.html`: Teacher settings
- `static/`: Static assets (currently using Tailwind via CDN)

## Data Storage

Currently uses JSON files for persistence:
- `data/profiles/teacher.json`: Teacher profile
- `data/classes.json`: Classes data
- `data/students.json`: Students data
- `data/assignments.json`: Assignments data

## Styling

Uses Tailwind CSS via CDN in templates. All UI components are built with Tailwind utility classes for consistency with the original figma design.
