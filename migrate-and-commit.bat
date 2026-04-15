@echo off
REM Migrate Aesop repo OUT of OneDrive, apply pending Phase 2 rename, commit, and push.
REM Double-click to run. OneDrive should stay off.

setlocal

set "OLD=C:\Users\scott\Documents\Aesop"
set "NEW=C:\Users\scott\Code\Aesop"
set "BACKUP=C:\Users\scott\Documents\Aesop.OLD"

echo.
echo === Step 1: Fresh clone to %NEW% ===
if exist "%NEW%" (
    echo   %NEW% already exists. Skipping clone.
) else (
    if not exist "C:\Users\scott\Code" mkdir "C:\Users\scott\Code"
    git clone https://github.com/AesopScott/Aesop.git "%NEW%"
    if errorlevel 1 goto :error
)

echo.
echo === Step 2: Mirror working-tree changes from OneDrive path (excluding .git) ===
robocopy "%OLD%" "%NEW%" /MIR /XD .git /R:1 /W:1 /NFL /NDL /NJH /NJS
if errorlevel 8 goto :error

echo.
echo === Step 3: Stage, commit, push ===
cd /d "%NEW%"
git add -A
git commit -m "Standardize underscore course dirs/files to hyphens" -m "Renamed 5 underscore course directories + contained module files to hyphens. Also normalized 3 underscore version-string filenames to dot semver. Updated all path references (href, fetch, registry URL fields, sitemap) to match. Kept course 'id' fields with underscores so student localStorage progress is preserved." -m "Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
if errorlevel 1 goto :error
git push origin main
if errorlevel 1 goto :error

echo.
echo === Step 4: Rename old OneDrive folder so nothing uses it by mistake ===
if exist "%BACKUP%" (
    echo   %BACKUP% already exists. Old path NOT renamed.
) else (
    cd /d C:\
    ren "%OLD%" "Aesop.OLD"
    echo   Old path renamed to %BACKUP%
)

echo.
echo === Done ===
echo New repo location: %NEW%
echo.
pause
exit /b 0

:error
echo.
echo *** ERROR encountered. See messages above. ***
pause
exit /b 1
