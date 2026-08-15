@echo off
chcp 65001 >nul
setlocal

set "APPDIR=%~dp0app-mobile"
set "ZIPFILE=%~dp0esprits-fortnite-app.zip"

echo.
echo  ============================================
echo   TRACKER ESPRITS FORTNITE - Deploiement
echo  ============================================
echo.

:: Supprimer l'ancien zip si present
if exist "%ZIPFILE%" del /f /q "%ZIPFILE%"

:: Creer le ZIP avec PowerShell
echo  Creation du fichier ZIP...
powershell -NoProfile -Command "Compress-Archive -Path '%APPDIR%\*' -DestinationPath '%ZIPFILE%' -Force"

if not exist "%ZIPFILE%" (
  echo  ERREUR: Le ZIP n'a pas pu etre cree.
  pause
  exit /b 1
)

echo  ZIP cree : esprits-fortnite-app.zip
echo.
echo  ============================================
echo.
echo  ETAPES D'INSTALLATION SUR TON TELEPHONE :
echo.
echo  1. La page Netlify va s'ouvrir dans ton navigateur.
echo.
echo  2. Glisse-depose le fichier ZIP cree ici :
echo     %ZIPFILE%
echo     sur la zone "Drag and drop your site folder" de Netlify.
echo.
echo  3. Attends 30 secondes -> tu recois une URL du genre :
echo     https://amazing-name-xyz123.netlify.app
echo.
echo  4. Ouvre cette URL sur ton telephone (5G ou WiFi).
echo.
echo  5. Dans Chrome, appuie sur le menu (3 points) puis
echo     "Ajouter a l'ecran d'accueil".
echo.
echo  6. L'app est installee. Elle fonctionne SANS internet
echo     une fois les images chargees une premiere fois.
echo.
echo  ============================================
echo.

:: Ouvrir Netlify Drop dans le navigateur
start "" "https://app.netlify.com/drop"

:: Ouvrir le dossier pour faciliter le drag-drop
explorer /select,"%ZIPFILE%"

echo  Netlify Drop est ouvert dans ton navigateur.
echo  Glisse le fichier ZIP mis en surbrillance sur la page.
echo.
pause
