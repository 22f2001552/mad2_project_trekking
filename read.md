# Trekking App

This repository contains a Vue frontend and a Flask backend for a trekking booking application.

## Structure

- `frontend/` - Vue 3 application using Vite.
- `backend/` - Flask API, Celery tasks, Redis cache, SQLite database.

## Backend setup

1. Create and activate a Python virtual environment in `backend/`:
   - Windows: `python -m venv backend\venv`
   - Activate: `backend\venv\Scripts\activate`
2. Install backend dependencies:
   - `python -m pip install -r backend/requirements.txt`
3. Start the backend API:
   - `cd backend`
   - `python app.py`

## Frontend setup

1. Install frontend dependencies:
   - `cd frontend`
   - `npm install`
2. Run the frontend development server:
   - `npm run dev`

## Notes

- The backend stores data in `backend/instance/trekking.sqlite3`.
- Celery is configured to use Redis at `redis://localhost:6379/0`.
- Cached API responses use Flask-Caching and Redis.
- Ignore files and runtime artifacts are handled by `.gitignore`.
