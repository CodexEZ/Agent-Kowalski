@echo off
set VENV_PATH=D:\Projects\MCP\venv\Scripts\activate.bat

call %VENV_PATH%

REM Start servers and save their process IDs
start /b python servers\search_server.py
set PID1=%!
start /b python servers\mongoose_database_server.py
set PID2=%!
echo %PID2%
start /b python api.py
set PID3=%!

echo Servers running. Press any key to stop...
pause >nul

REM Kill servers by PID
start /b taskkill /PID %PID1% /F
start /b taskkill /PID %PID2% /F
start /b taskkill /PID %PID3% /F

echo All servers stopped.
