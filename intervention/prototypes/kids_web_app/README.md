# DreamSpace Kids Web App

A web-based alternative to the iOS kids learning app, built with Flask. Runs on **port 5001** and calls the existing backend on **port 5000** via HTTP — no shared Python imports, no direct database access.

## Quick Start

```bash
cd intervention/prototypes/kids_web_app
pip install -r requirements.txt
python app.py
```

Open http://localhost:5001

## Running with the Backend

```bash
# Terminal 1 — Backend (port 5000)
cd intervention/prototypes/backend
source venv/bin/activate
python app.py

# Terminal 2 — Kids Web App (port 5001)
cd intervention/prototypes/kids_web_app
python app.py
```

## Demo Mode (No Backend)

The app works without the backend using static mock data — ideal for capstone presentations. A banner appears at the top when running in demo mode.

## Features

- **Auth** — Sign up / sign in (proxied to backend)
- **Onboarding** — Name, age, avatar, team selection wizard
- **Dashboard** — Welcome card, tech news carousel, daily challenge, team card, quick actions
- **Challenges** — 12 coding challenges with difficulty filter, multiple choice, instant feedback
- **Progress** — Stats (points, streak, accuracy), weekly chart, category breakdown, achievements
- **Teams** — Team and individual leaderboards
- **Profile** — View and edit name, age, avatar, team
- **Lessons** — All 16 lesson JSONs rendered with exercises and student challenges
- **Dark / Light mode** — Toggle persists in localStorage, no flash on load

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `http://localhost:5000` | Backend URL |
| `SECRET_KEY` | dev key | Flask session secret |
| `NEWSAPI_KEY` | (empty) | Optional NewsAPI.org key for news fallback |

## Architecture

```
kids_web_app/ (port 5001)
  ├── app.py                # Flask entry point, loads lesson JSON at startup
  ├── config.py             # API_BASE_URL, SECRET_KEY, LESSON_DIR
  ├── routes/               # One Blueprint per page
  │   ├── auth.py           # login, signup, logout, @login_required
  │   ├── dashboard.py      # /
  │   ├── onboarding.py     # /onboarding (2-step wizard)
  │   ├── challenges.py     # /challenges, /challenges/<id>
  │   ├── progress.py       # /progress
  │   ├── teams.py          # /teams
  │   ├── profile.py        # /profile
  │   ├── lessons.py        # /lessons, /lessons/<id>
  │   └── news.py           # /api/news (internal, cached)
  ├── services/
  │   ├── api_client.py     # HTTP wrapper → port 5000, with offline fallback
  │   └── news_service.py   # TechCrunch RSS → HN → NewsAPI → static, 15-min TTL
  ├── templates/            # Jinja2 HTML templates
  └── static/
      ├── css/main.css      # Full design system, CSS custom properties
      └── js/
          ├── theme.js      # Dark/light toggle + localStorage
          └── carousel.js   # News carousel (swipe, auto-advance, dots)
```
