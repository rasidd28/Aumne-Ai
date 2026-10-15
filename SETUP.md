# ContentMod: Setup Instructions

## Prerequisites

| Tool | Version | Needed for |
|---|---|---|
| Python | 3.9+ | Backend and virtualenv |
| Node.js + npm | 16+ | Frontend, and installing the SDK generator |
| Java | 11+ | Generating the Python SDK |

## 1. First-time setup

Run from the project root (`content mod/`):

```bat
setupdev.bat
```

This will:
- create the Python virtualenv in `backend/env/`
- install the backend dependencies from `requirements.txt`
- run the Alembic migrations (creates `backend/content_mod.db`)
- load the sample data (skipped if the table already has rows)
- run `npm install` for the frontend

If Alembic fails with "table posts already exists", you have an old database. Delete it and run setup again:

```bat
del backend\content_mod.db
setupdev.bat
```

## 2. Start the app

```bat
runapplication.bat
```

This opens two terminal windows:

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

## 3. Run the tests

```bat
cd backend
env\Scripts\activate
pytest -v
cd ..
```

All tests should pass.

## 4. Generate the Python SDK

From the project root:

```bat
generate_sdk.bat
```

The script checks for Java and the generator CLI, starts the backend if it isn't already running, generates `moderation_sdk/`, installs it into the backend virtualenv, runs `sdk_usage_example.py` as a smoke test, and stops the backend again if it started it.

To run the demo again later (backend must be running, SDK already generated):

```bat
backend\env\Scripts\python.exe sdk_usage_example.py
```

## Manual setup (if the .bat files don't work)

Backend:

```bat
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python seed.py
python main.py
```

Frontend (in a second terminal):

```bat
cd frontend
npm install
npm start
```

## Quick check that it works

- http://localhost:8000/docs loads and lists 5 endpoints.
- http://localhost:3000 loads, and you can create a post, submit it, and publish it.
- `pytest -v` passes.
- `moderation_sdk/` exists after running `generate_sdk.bat`.
