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

if not exist "fonts" mkdir fonts
if not exist "fonts\licenses" mkdir fonts\licenses

if not exist "fonts\01-BadScript-Regular.ttf" powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/google/fonts/main/ofl/badscript/BadScript-Regular.ttf' -OutFile 'fonts\01-BadScript-Regular.ttf'"
if not exist "fonts\02-Caveat-Regular.ttf" powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/google/fonts/main/ofl/caveat/Caveat%%5Bwght%%5D.ttf' -OutFile 'fonts\02-Caveat-Regular.ttf'"
if not exist "fonts\03-MarckScript-Regular.ttf" powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/google/fonts/main/ofl/marckscript/MarckScript-Regular.ttf' -OutFile 'fonts\03-MarckScript-Regular.ttf'"
if not exist "fonts\04-Neucha-Regular.ttf" powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/google/fonts/main/ofl/neucha/Neucha-Regular.ttf' -OutFile 'fonts\04-Neucha-Regular.ttf'"

if not exist ".venv" (
  py -m venv .venv
)

call .venv\Scripts\activate.bat
py -m pip install -r requirements.txt
py -m streamlit run app.py
