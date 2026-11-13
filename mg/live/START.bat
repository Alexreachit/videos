@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist node_modules (echo Bitte zuerst SETUP.bat ausfuehren. & pause & exit /b)
if not exist config.json copy config.example.json config.json >nul
start "" "http://localhost:8787/live/game.html?q=0.5&fps=30"
node server.js %*
pause
