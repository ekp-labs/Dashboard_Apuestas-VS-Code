@echo off
setlocal
cd /d "%~dp0"
start "Dashboard Apuestas" powershell -NoExit -Command "npm run dev -- --host 127.0.0.1 --port 5178"
timeout /t 4 /nobreak >nul
start "" "http://127.0.0.1:5178"



