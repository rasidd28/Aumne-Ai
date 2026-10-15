@echo off

echo Starting ContentMod services...

echo Starting backend on http://localhost:8000 ...
start "ContentMod Backend" cmd /k "cd backend && call env\Scripts\activate && python main.py"

timeout /t 2 /nobreak > nul

echo Starting frontend on http://localhost:3000 ...
start "ContentMod Frontend" cmd /k "cd frontend && npm start"

echo Services dispatched in separate terminal windows.
echo  Backend:  http://localhost:8000 (Docs: http://localhost:8000/docs)
echo  Frontend: http://localhost:3000
