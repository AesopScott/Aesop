@echo off
REM Rebase the local commit onto the latest origin/main, then push.
REM Run from the NEW repo location (C:\Users\scott\Code\Aesop).

cd /d C:\Users\scott\Code\Aesop

echo === Pulling latest from origin with rebase ===
git pull --rebase origin main
if errorlevel 1 goto :conflict

echo.
echo === Pushing ===
git push origin main
if errorlevel 1 goto :error

echo.
echo === Done. Phase 2 rename is now on GitHub. ===
pause
exit /b 0

:conflict
echo.
echo *** Rebase hit conflicts. Resolve them, then run:
echo     git rebase --continue
echo     git push origin main
pause
exit /b 1

:error
echo.
echo *** Push failed. ***
pause
exit /b 1
