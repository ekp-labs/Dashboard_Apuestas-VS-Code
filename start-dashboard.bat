@echo off
setlocal
cd /d "%~dp0"
start "" powershell -NoExit -Command "npm run dev -- --host 127.0.0.1 --port 5178"
timeout /t 2 >nul
start "" "http://127.0.0.1:5178"

