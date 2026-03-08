@echo off
setlocal

rem Get script directory
set "SCRIPT_DIR=%~dp0"

echo ====================================
echo   Steam Batch Login Tool v2.1
echo   Graphical Interface
echo ====================================
echo.
echo Working Directory: %SCRIPT_DIR%
echo.

rem Change to script directory
cd /d "%SCRIPT_DIR%"

rem Check core files
if not exist "src\steam_login_gui.py" (
    echo Error: GUI program not found
    echo.
    echo Please confirm these files exist:
    echo   - src\steam_login_gui.py
    echo   - src\login_steam.py
    echo   - src\chinese_to_tab.py
    echo.
    echo Current directory: %SCRIPT_DIR%
    echo.
    pause
    exit /b 1
)

rem Run GUI
echo Starting GUI...
echo.
python src\steam_login_gui.py

rem Check result
if errorlevel 1 (
    echo.
    echo Startup failed, error code: %errorlevel%
    echo.
    echo Possible reasons:
    echo 1. Python not installed or not in PATH
    echo 2. Missing libraries (pyautogui, pillow)
    echo 3. File corrupted
    echo.
    echo Run check_files.py for details
    echo.
    pause
)

endlocal
