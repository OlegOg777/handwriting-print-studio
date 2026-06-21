@echo off
chcp 65001 >nul
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
  echo Не найден Python 3.
  echo Установите Python 3 и запустите файл снова.
  pause
  exit /b 1
)

if not exist ".venv" (
  py -m venv .venv
)

call .venv\Scripts\activate.bat
py -m pip install -q -r requirements.txt
py -m streamlit run app.py

