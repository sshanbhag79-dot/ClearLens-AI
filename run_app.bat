@echo off
echo Starting BioFilter...

:: Start Backend
echo Starting Backend on Port 8000...
start "BioFilter Backend" cmd /k "python -m uvicorn backend.main:app --reload --port 8000"

:: Wait a moment for backend to initialize
timeout /t 5

:: Start Frontend
echo Starting Frontend on Port 8501...
start "BioFilter Frontend" cmd /k "python -m streamlit run frontend/app.py --server.port 8501"

echo App is running!
echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:8501
pause
