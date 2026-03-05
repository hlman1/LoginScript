@echo off
chcp 65001 >nul
echo ====================================
echo   诊断工具 - 检查运行环境
echo ====================================
echo.

echo [1] 当前目录
cd
echo.

echo [2] 启动工具位置
echo %~f0
echo.

echo [3] 检查项目文件
if exist "src\steam_login_gui.py" (
    echo [OK] src\steam_login_gui.py
) else (
    echo [FAIL] src\steam_login_gui.py - 文件不存在
    echo.
    echo 请确认你在项目根目录下运行此脚本
)

if exist "src\login_steam.py" (
    echo [OK] src\login_steam.py
) else (
    echo [FAIL] src\login_steam.py - 文件不存在
)

if exist "src\chinese_to_tab.py" (
    echo [OK] src\chinese_to_tab.py
) else (
    echo [FAIL] src\chinese_to_tab.py - 文件不存在
)

if exist "启动工具.bat" (
    echo [OK] 启动工具.bat
) else (
    echo [FAIL] 启动工具.bat - 文件不存在
)

if exist "accounts.txt" (
    echo [OK] accounts.txt
) else (
    echo [WARN] accounts.txt - 文件不存在（首次运行正常）
)

echo.
echo [4] 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python - 未安装或不在PATH中
) else (
    python --version
)

echo.
echo [5] 检查 Python 依赖
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] tkinter - 未安装
) else (
    echo [OK] tkinter
)

python -c "import pyautogui" >nul 2>&1
if errorlevel 1 (
    echo [WARN] pyautogui - 未安装（可以后续安装）
) else (
    echo [OK] pyautogui
)

python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo [WARN] PIL - 未安装（可以后续安装）
) else (
    echo [OK] PIL
)

echo.
echo ====================================
echo   诊断完成
echo ====================================
echo.
echo 如果有 [FAIL] 项，请先解决这些问题
pause
