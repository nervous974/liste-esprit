@echo off
chcp 65001 >nul
set "ZIPFILE=%~dp0esprits-fortnite-app.zip"
if exist "%ZIPFILE%" del /f /q "%ZIPFILE%"
powershell -NoProfile -Command "Compress-Archive -Path '%~dp0app-mobile\*' -DestinationPath '%ZIPFILE%' -Force"
echo ZIP mis a jour : esprits-fortnite-app.zip
explorer /select,"%ZIPFILE%"
