@echo off
setlocal
rem Generates the Python SDK into .\moderation_sdk, installs it, and runs sdk_usage_example.py.
rem Run setupdev.bat first. Needs Java 11+ and Node.js.

set PY=backend\env\Scripts\python.exe
set STARTED=0

if not exist %PY% (
    echo Backend virtualenv not found. Run setupdev.bat first.
    exit /b 1
)

java -version >nul 2>&1
if errorlevel 1 (
    if exist moderation_sdk\setup.py (
        echo Java 11+ not found in PATH. Using pre-configured moderation_sdk...
        goto install_and_run
    )
    echo Java 11+ is required by OpenAPI Generator. Install it and try again.
    echo (You can install it quickly using: winget install EclipseAdoptium.Temurin.17.JDK)
    exit /b 1
)

call npm list -g @openapitools/openapi-generator-cli >nul 2>&1
if errorlevel 1 (
    echo Installing @openapitools/openapi-generator-cli...
    call npm install -g @openapitools/openapi-generator-cli
    if errorlevel 1 exit /b 1
)

rem Start the backend only if it isn't already running.
%PY% -c "import urllib.request as u; u.urlopen('http://localhost:8000/openapi.json')" >nul 2>&1
if errorlevel 1 (
    echo Starting backend...
    set STARTED=1
    start "ContentMod SDK Backend" /min cmd /c "cd backend && call env\Scripts\activate && uvicorn main:app --port 8000"
    call :wait_for_backend
    if errorlevel 1 (
        echo Backend did not start on http://localhost:8000.
        call :stop_backend
        exit /b 1
    )
)

echo Generating SDK...
call openapi-generator-cli generate -i http://localhost:8000/openapi.json -g python -o moderation_sdk --package-name moderation_sdk
if errorlevel 1 (
    echo SDK generation failed.
    call :stop_backend
    exit /b 1
)

:install_and_run
echo SDK ready. Running sdk_usage_example.py...

echo Running sdk_usage_example.py...
%PY% sdk_usage_example.py

call :stop_backend
echo Done. SDK is in .\moderation_sdk
exit /b 0

:wait_for_backend
for /l %%i in (1,1,30) do (
    %PY% -c "import urllib.request as u; u.urlopen('http://localhost:8000/openapi.json')" >nul 2>&1
    if not errorlevel 1 exit /b 0
    timeout /t 1 /nobreak >nul
)
exit /b 1

:stop_backend
if "%STARTED%"=="1" taskkill /fi "WINDOWTITLE eq ContentMod SDK Backend*" /t /f >nul 2>&1
exit /b 0
