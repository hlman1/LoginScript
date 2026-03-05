@echo off
chcp 65001 >nul
setlocal

rem 获取批处理文件所在目录
set "SCRIPT_DIR=%~dp0"

echo ====================================
echo   Steam 批量登录工具 v2.1
echo   图形化界面版本
echo ====================================
echo.
echo 工作目录: %SCRIPT_DIR%
echo.

rem 切换到脚本所在目录
cd /d "%SCRIPT_DIR%"

rem 检查核心文件是否存在
if not exist "src\steam_login_gui.py" (
    echo ❌ 错误：找不到 GUI 程序
    echo.
    echo 请确认以下文件存在：
    echo   - src\steam_login_gui.py
    echo   - src\login_steam.py
    echo   - src\chinese_to_tab.py
    echo.
    echo 当前目录: %SCRIPT_DIR%
    echo.
    pause
    exit /b 1
)

rem 运行 GUI 程序
echo 🚀 正在启动图形界面...
echo.
python src\steam_login_gui.py

rem 检查运行结果
if errorlevel 1 (
    echo.
    echo ❌ 启动失败，错误代码: %errorlevel%
    echo.
    echo 可能的原因：
    echo 1. Python 未安装或未加入 PATH
    echo 2. 缺少必要的库（pyautogui, pillow）
    echo 3. 文件损坏
    echo.
    echo 建议运行 诊断工具.bat 查看详情
    echo.
    pause
)

endlocal
