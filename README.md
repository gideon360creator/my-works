# AI Student Performance Chatbot

A complete AI chatbot system for student performance grading and academic tracking.

## Features

- **AI Chatbot**: Ask questions like "What is my grade in Math?" or "How am I performing?".
- **Dashboard**: Visual analytics of your academic performance.
- **Grade Management**: Lecturers can manage subjects, assessments, and grades.
- **Authentication**: Secure login for Students and Lecturers.

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Vite, Tailwind CSS, Recharts

## Setup & Run

### Prerequisites

- Python 3.8+
- Node.js 16+

### Quick Start

1. Install dependencies for both backend and frontend (first time only):
   ```bash
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   cd ..
   ```

2. Run the entire system (Backend + Frontend):
   ```bash
   python run.py
   ```
   This will start both servers and open the application in your browser.

### Backend (Manual)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be running at `http://localhost:8000`.

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The application will be running at `http://localhost:5173`.

## Default Login

You can register a new account on the login page. Select "Lecturer" or "Student" as your role.
