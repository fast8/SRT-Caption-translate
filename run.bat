cd /d %~dp0
start cmd /k ".\venv\Scripts\activate && python start.py"
timeout /t 5 > nul
start cmd /k python subtanslate.py