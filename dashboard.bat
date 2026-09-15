@echo off
setlocal
cd /d "%~dp0"
echo Iniciando Dashboard Apuestas...
start npm run dev
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5178"

