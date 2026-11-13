@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   Roundhead Island LIVE - Einrichtung
echo ============================================
set NEU=
where node >nul 2>nul
if errorlevel 1 (
  echo [1/2] Node.js fehlt und wird jetzt installiert ...
  winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
  set NEU=1
) else (echo [1/2] Node.js ist da.)
python -c "import sys" >nul 2>nul
if errorlevel 1 (
  echo [2/2] Python fehlt und wird jetzt installiert ...
  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
  set NEU=1
) else (echo [2/2] Python ist da.)
if defined NEU (
  echo.
  echo Installation fertig. Bitte dieses Fenster schliessen und SETUP.bat noch einmal doppelklicken.
  echo Falls winget fehlt: Node.js von https://nodejs.org und Python von https://python.org selbst installieren.
  pause
  exit /b
)
echo.
echo Stimme (edge-tts) installieren ...
python -m pip install --user --upgrade edge-tts
echo.
echo Live-Verbindung (tiktok-live-connector) installieren ...
call npm install
if not exist config.json copy config.example.json config.json >nul
echo.
echo ============================================
echo   Fertig! Jetzt in config.json bei "tiktokUser" deinen TikTok-Namen eintragen.
echo   Test ohne TikTok: TEST.bat   -   Echtes Live: START.bat
echo ============================================
notepad config.json
pause
