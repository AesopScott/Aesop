@echo off
REM Finish the Aesop repo migration:
REM   1. Rebase pending commit onto latest origin/main
REM   2. Push to GitHub
REM   3. Rename old OneDrive folder to Aesop.OLD
REM Run from anywhere by double-clicking.

setlocal

set "OLD=C:\Users\scott\Documents\Aesop"
set "NEW=C:\Users\scott\Code\Aesop"
set "BACKUP=C:\Users\scott\Documents\Aesop.OLD"

cd /d "%NEW%"
if errorlevel 1 (
    echo *** Cannot cd to %NEW% \^- did the migrate step run?
    pause
    exit /b 1
)

echo === Step 1: Rebase pending commit onto latest origin/main ===
git pull --rebase origin main
if errorlevel 1 goto :conflict

echo.
echo === Step 2: Push to GitHub ===
git push origin main
if errorlevel 1 goto :pusherror

echo.
echo === Step 3: Rename old OneDrive folder ===
if exist "%BACKUP%" (
    echo   %BACKUP% already exists. Skipping rename.
) else if exist "%OLD%" (
    cd /d C:\
    ren "%OLD%" "Aesop.OLD"
    if errorlevel 1 (
        echo   *** Could not rename old folder. It may be in use. Close any windows/editors pointing at it and rename manually.
    ) else (
        echo   Old path renamed to %BACKUP%
    )
) else (
    echo   Old path %OLD% does not exist. Nothing to rename.
)

echo.
echo === Migration complete ===
echo Active repo: %NEW%
echo.
echo Next steps for you:
echo   1. In Cowork, re-mount the Aesop folder from %NEW%
echo   2. Update Claude memory protocol to use %NEW%
echo   3. Re-enable scheduled tasks when ready
echo.
pause
exit /b 0

:conflict
echo.
echo *** Rebase hit conflicts. Resolve them, then run:
echo     git rebase --continue
echo     git push origin main
pause
exit /b 1

:pusherror
echo.
echo *** Push failed. ***
pause
exit /b 1
