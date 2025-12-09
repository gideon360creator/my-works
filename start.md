---
description: Start both backend and frontend servers
---

# Start Project Servers

This workflow starts both the backend (FastAPI) and frontend (Vite/React) development servers.

// turbo-all

## Steps

1. Start the backend server in the background:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the frontend development server in the background:
```bash
cd frontend
npm run dev
```

## Expected Result

- Backend API running at: http://localhost:8000
- Frontend app running at: http://localhost:5173 (or next available port)
- Both servers will auto-reload on code changes

## To Stop Servers

You can ask me to stop the servers, or manually terminate them from the terminal.
