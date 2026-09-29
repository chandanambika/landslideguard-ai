@echo off
echo ========================================================
echo Starting LandslideGuard AI (Backend + Frontend)
echo ========================================================

REM Add node to PATH if needed
set PATH=C:\Program Files\nodejs;%PATH%

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "LandslideGuard AI - Backend" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting Vite Frontend on http://localhost:5173 ...
cd frontend
start "LandslideGuard AI - Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================================
echo LandslideGuard AI is running!
echo Access the Dashboard at: http://localhost:5173
echo Access the API Docs at:  http://127.0.0.1:8000/docs
echo ========================================================
