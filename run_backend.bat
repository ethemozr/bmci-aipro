@echo off
cd /d %~dp0
py -3.12 -m pip install -r backend\requirements.txt
py -3.12 -m uvicorn backend.main:app --reload
pause
