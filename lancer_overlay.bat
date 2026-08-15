@echo off
setlocal
cd /d "%~dp0"
python overlay_esprits.py
if errorlevel 1 (
  py overlay_esprits.py
)
endlocal
