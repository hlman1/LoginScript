#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 只登录第一个账号并保持游戏运行
包含窗口激活功能
"""

import time
import sys
import subprocess

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Windows 键盘模拟支持
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    pyautogui.PAUSE = 0.5
except ImportError:
    PYAUTOGUI_AVAILABLE = False

print("="*60)
print("TEST MODE - Login First Account")
print("="*60)

# 配置
STEAM_EXE_PATH = r"F:\steam\Steam.exe"
PUBG_APP_ID = "578080"
USERNAME = "ta3az7wf4vg3"
PASSWORD = "Av6Ih8Bh8Fd7"

def check_process_running(process_name):
    """检查进程是否正在运行"""
    try:
        result = subprocess.run(
            ['tasklist', '/FI', f'IMAGENAME eq {process_name}'],
            capture_output=True,
            text=True,
            shell=True
        )
        return process_name in result.stdout
    except:
        return False

def activate_window_by_title(title_keyword):
    """通过窗口标题激活窗口"""
    try:
        # 使用 PowerShell 激活窗口
        ps_script = f'''
        $process = Get-Process | Where-Object {{$_.MainWindowTitle -like "*{title_keyword}*"}}
        if ($process) {{
            (New-Object -ComObject WScript.Shell).AppActivate($process.MainWindowTitle)
            Write-Host "Activated: $($process.MainWindowTitle)"
        }}
        '''
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "Activated:" in result.stdout
    except:
        return False

def kill_all_processes():
    """关闭所有 Steam 和 PUBG 相关进程"""
    print("🧹 清理所有进程...")
    processes_to_kill = [
        "steam.exe",
        "steamwebhelper.exe",
        "gameoverlayui.exe",
        "steamservice.exe",
        "TslGame.exe",
        "BEService.exe"
    ]
    for proc in processes_to_kill:
        try:
            subprocess.run(f"taskkill /F /IM {proc} >nul 2>&1", shell=True)
        except:
            pass
    time.sleep(1)
    print("✅ 所有进程已清理")

def steam_login(username, password):
    """使用 Steam 命令行登录"""
    print(f"\n🔐 使用 Steam 客户端登录: {username}")
    try:
        cmd = [STEAM_EXE_PATH, "-login", username, password]
        print(f"📍 执行: steam.exe -login {username} ********")
        subprocess.Popen(cmd, shell=False)

        # 等待 Steam 启动和登录
        print("⏳ 等待 Steam 启动和登录...")
        for i in range(30):
            time.sleep(1)
            if check_process_running("steam.exe") and check_process_running("steamwebhelper.exe"):
                print(f"✅ Steam 已就绪 (耗时 {i+1} 秒)")
                return True

        print("⚠️  Steam 可能未完全就绪，但继续...")
        return True
    except Exception as e:
        print(f"⚠️  Steam 登录失败: {e}")
        return False

def send_enter_key():
    """发送回车键（用于同意用户许可协议）"""
    if PYAUTOGUI_AVAILABLE:
        try:
            print("   💻 使用 pyautogui 发送回车键...")
            pyautogui.press('enter')
            return True
        except Exception as e:
            print(f"   ⚠️  pyautogui 失败: {e}")

    # 备用方法：使用 PowerShell
    try:
        print("   💻 使用 PowerShell 发送回车键...")
        ps_command = "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')"
        subprocess.run(["powershell", "-Command", ps_command], capture_output=True, timeout=5)
        return True
    except:
        return False

def activate_and_send_enter():
    """激活窗口并发送回车键"""
    # 尝试激活包含"许可"、"协议"、"License"、"Agreement"等关键词的窗口
    keywords = ["许可", "协议", "License", "Agreement", "PUBG", "BATTLEGROUNDS"]

    for keyword in keywords:
        if activate_window_by_title(keyword):
            print(f"   ✅ 激活了包含 '{keyword}' 的窗口")
            time.sleep(0.5)
            send_enter_key()
            return True

    # 如果没有找到特定窗口，直接发送回车键
    print("   ⚠️  未找到特定窗口，直接发送回车键...")
    return send_enter_key()

def launch_pubg_game():
    """启动 PUBG 游戏"""
    print("\n🎮 启动 PUBG 游戏...")
    try:
        time.sleep(2)

        print("📍 使用 Steam -applaunch 启动游戏...")
        cmd = [STEAM_EXE_PATH, "-applaunch", PUBG_APP_ID]
        subprocess.Popen(cmd, shell=False)
        print(f"   执行: steam.exe -applaunch {PUBG_APP_ID}")

        print("⏳ 等待游戏启动...")

        # 阶段1：等待用户许可协议窗口
        print("💡 阶段1: 等待用户许可协议窗口...")
        time.sleep(5)

        # 尝试多次发送回车键来同意协议
        max_agree_attempts = 6
        for i in range(max_agree_attempts):
            print(f"   尝试点击同意 ({i+1}/{max_agree_attempts})...")
            activate_and_send_enter()
            time.sleep(2)

            if check_process_running("TslGame.exe"):
                print(f"✅ 检测到游戏已启动（协议可能已同意）")

                # 尝试激活游戏窗口
                print("💡 尝试激活游戏窗口...")
                time.sleep(2)
                for keyword in ["PUBG", "BATTLEGROUNDS", "TslGame"]:
                    if activate_window_by_title(keyword):
                        print(f"   ✅ 已激活 PUBG 游戏窗口")
                        break
                return True

        # 阶段2：继续等待
        print("💡 阶段2: 继续等待游戏进程启动...")
        max_wait = 50
        for i in range(max_wait):
            if check_process_running("TslGame.exe"):
                print(f"✅ PUBG 游戏已启动 (TslGame.exe 检测到，总耗时 {i+1} 秒)")

                # 尝试激活游戏窗口
                print("💡 尝试激活游戏窗口...")
                for keyword in ["PUBG", "BATTLEGROUNDS", "TslGame"]:
                    if activate_window_by_title(keyword):
                        print(f"   ✅ 已激活 PUBG 游戏窗口")
                        break

                return True
            time.sleep(1)
            if (i + 1) % 5 == 0:
                print(f"   等待中... ({i+1}/{max_wait}秒)")

        print("⚠️  未检测到 TslGame.exe 进程")
        return False

    except Exception as e:
        print(f"⚠️  启动 PUBG 失败: {e}")
        return False

# 主流程
try:
    print("\n步骤 1/3: 清理环境")
    kill_all_processes()

    print("\n步骤 2/3: 登录 Steam")
    if not steam_login(USERNAME, PASSWORD):
        print("❌ Steam 登录失败")
        exit(1)

    print("\n步骤 3/3: 启动 PUBG")
    if not launch_pubg_game():
        print("❌ PUBG 启动失败")
        print("\n💡 请手动检查：")
        print("   - 是否看到用户许可协议窗口？")
        print("   - Steam 是否已登录？")
        input("\n按回车键退出...")
        exit(1)

    # ✅ 游戏已启动，保持运行状态
    print("\n" + "="*50)
    print("🧪 测试模式：游戏保持运行")
    print("="*50)
    print("💡 请检查以下内容：")
    print("   1. 任务管理器中是否有 TslGame.exe 进程")
    print("   2. 屏幕上是否有 PUBG 游戏窗口")
    print("   3. 游戏窗口是否在前台显示")
    print("\n💡 如果游戏窗口没有显示，尝试：")
    print("   - 点击任务栏上的 PUBG 图标")
    print("   - 按 Alt+Tab 切换窗口")
    print("\n💡 脚本将保持运行，每 10 秒显示一次状态")
    print("💡 按 Ctrl+C 可以退出")
    print("="*50 + "\n")

    # 保持运行，定期显示状态
    try:
        while True:
            time.sleep(10)

            steam_running = check_process_running("steam.exe")
            game_running = check_process_running("TslGame.exe")

            status = f"📊 状态: Steam={'✅运行' if steam_running else '❌未运行'} | PUBG={'✅运行' if game_running else '❌未运行'}"
            print(status)

    except KeyboardInterrupt:
        print("\n\n⚠️  用户退出")
        print("💡 游戏和 Steam 继续保持运行")
        print("💡 如需关闭，请手动结束任务或在任务管理器中关闭")

except Exception as e:
    print(f"\n⚠️  发生错误: {e}")
    import traceback
    traceback.print_exc()
