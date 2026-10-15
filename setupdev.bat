@echo off
setlocal

echo Setting up ContentMod environment...

cd backend
if not exist env (
    echo [1/4] Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo Failed to create virtual environment. Ensure Python 3.9+ is installed.
        exit /b 1
    )
)

echo [2/4] Installing backend dependencies...
call env\Scripts\activate
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo Failed to install requirements.
    exit /b 1
)

echo [3/4] Running migrations...
alembic upgrade head
if errorlevel 1 (
    echo Alembic upgrade failed. Deleting existing database and retrying...
    if exist content_mod.db del /f /q content_mod.db
    alembic upgrade head
    if errorlevel 1 (
        echo Migration retry failed.
        exit /b 1
    )
)

if exist seed_data.sql (
    python -c "import sqlite3; con = sqlite3.connect('content_mod.db'); con.executescript(open('seed_data.sql', encoding='utf-8').read()); con.close()"
    echo Seed data loaded.
)

call deactivate
cd ..

echo [4/4] Installing frontend dependencies...
cd frontend
call npm install --silent
if errorlevel 1 (
    echo npm install failed. Ensure Node.js and npm are installed.
    exit /b 1
)
cd ..

echo Setup complete.
exit /b 0
