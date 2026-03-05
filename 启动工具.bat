@echo off
chcp 65001 >nul
echo ====================================
echo   Steam 批量登录工具 v2.1
echo   图形化界面版本
echo ====================================
echo.

cd /d "%~dp0"
python src\steam_login_gui.py

if errorlevel 1 (
    echo.
    echo ❌ 启动失败，请检查：
    echo 1. 是否已安装 Python
    echo 2. 是否已安装依赖（pyautogui pillow）
    echo.
    pause
)
