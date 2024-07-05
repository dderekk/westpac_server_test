@echo off
REM Navigate to the directory of the script
cd /d %~dp0

REM Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Run the server
python start_server.py

pause
