@echo off
cd /d %~dp0
if not exist node_modules call npm install
if not exist config.json copy config.example.json config.json
start "" http://localhost:8787/live/game.html
node server.js %*
pause
