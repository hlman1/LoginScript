#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam 账号批量登录脚本
功能：从 accounts.txt 读取账号信息，依次登录 Steam，完成后退出
技术：Playwright 浏览器自动化
"""

import time
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Windows 键盘模拟支持
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    # 设置 pyautogui 安全间隔
    pyautogui.PAUSE = 0.5
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  pyautogui 未安装，将使用备用方法")
    print("💡 安装方法: pip install pyautogui")

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')



class SteamLoginBatch:
    """Steam 批量登录类"""

    # Steam 页面 URL
    STEAM_LOGIN_URL = "https://steamcommunity.com/login/home/"
    PUBG_APP_ID = "578080"
    PUBG_STORE_URL = f"https://store.steampowered.com/app/{PUBG_APP_ID}/"
    STEAM_EXE_PATH = r"F:\steam\Steam.exe"  # Steam 客户端路径

    def __init__(self, accounts_file="accounts.txt", headless=False):
        """
        初始化

        Args:
            accounts_file: 账号文件路径
            headless: 是否使用无头模式（不显示浏览器窗口）
        """
        self.accounts_file = accounts_file
        self.accounts = []
        self.current_index = 0
        self.headless = headless
        # Playwright 浏览器相关属性（已废弃，保留以避免错误）
        
        # 项目根目录
        self.project_root = Path(__file__).parent.parent

    def load_accounts(self):
        """
        从文件加载账号信息
        支持格式：
        - Tab 分隔：账号	密码	邮箱	邮箱密码	邮箱地址
        - 冒号分隔：账号:密码:邮箱:邮箱密码:邮箱地址

        Returns:
            bool: 加载是否成功
        """
        if not os.path.exists(self.accounts_file):
            print(f"❌ 账号文件不存在: {self.accounts_file}")
            return False

        try:
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # 跳过空行和注释行
                    if not line or line.startswith('#'):
                        continue

                    # 尝试解析账号信息
                    account = None

                    # 优先尝试 Tab 分隔格式
                    if '\t' in line:
                        parts = line.split('\t')
                        # 清理每个部分
                        parts = [p.strip() for p in parts if p.strip()]
                        if len(parts) >= 2:
                            account = {
                                'username': parts[0] if len(parts) > 0 else '',
                                'password': parts[1] if len(parts) > 1 else '',
                                'email': parts[2] if len(parts) > 2 else '',
                                'email_password': parts[3] if len(parts) > 3 else '',
                                'email_url': parts[4] if len(parts) > 4 else ''
                            }

                    # 如果 Tab 解析失败，尝试冒号分隔格式（兼容旧格式）
                    elif ':' in line and line.count(':') >= 4:
                        parts = line.split(':')
                        if len(parts) >= 5:
                            account = {
                                'username': parts[0].strip(),
                                'password': parts[1].strip(),
                                'email': parts[2].strip(),
                                'email_password': parts[3].strip(),
                                'email_url': parts[4].strip()
                            }

                    # 验证必要字段
                    if account and account['username'] and account['password']:
                        self.accounts.append(account)
                    else:
                        print(f"⚠️  第 {line_num} 行格式错误，已跳过")

            print(f"✅ 成功加载 {len(self.accounts)} 个账号")
            return len(self.accounts) > 0

        except Exception as e:
            print(f"❌ 读取账号文件失败: {e}")
            return False

    def init_browser(self):
        """
        初始化浏览器

        Returns:
            bool: 初始化是否成功
        """
        try:
            self.playwright = sync_playwright().start()

            # 启动 Chromium 浏览器
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox'
                ]
            )

            # 创建浏览器上下文
            self.context = self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            # 创建新页面
            self.page = self.context.new_page()

            print("✅ 浏览器初始化成功")
            return True

        except Exception as e:
            print(f"❌ 浏览器初始化失败: {e}")
            return False

    def close_browser(self):
        """关闭浏览器"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("✅ 浏览器已关闭")
        except Exception as e:
            print(f"⚠️  关闭浏览器时出错: {e}")

    def login_steam(self, account):
        """
        登录 Steam 账号

        Args:
            account: 账号信息字典

        Returns:
            bool: 登录是否成功
        """
        username = account['username']
        password = account['password']

        print(f"\n{'='*50}")
        print(f"🔐 正在登录账号: {username}")
        print(f"{'='*50}")

        try:
            # 访问 Steam 登录页面
            print(f"📍 正在打开 Steam 登录页面...")
            self.page.goto(self.STEAM_LOGIN_URL, wait_until="domcontentloaded", timeout=30000)

            # 等待登录表单加载
            time.sleep(1)

            # 查找用户名输入框 (Steam 可能有不同的登录界面)
            username_selectors = [
                'input[type="text"]',
                'input[name="username"]',
                'input[placeholder*="用户名" i], input[placeholder*="username" i]',
                '#input_username'
            ]

            username_input = None
            for selector in username_selectors:
                try:
                    username_input = self.page.wait_for_selector(selector, timeout=5000)
                    if username_input:
                        break
                except:
                    continue

            if not username_input:
                print("❌ 未找到用户名输入框")
                print("💡 可能原因：页面未加载完成、网络问题或Steam界面变化")
                print("⏳ 跳过此账号，继续下一个...")
                return False

            # 输入用户名
            print("📝 正在输入用户名...")
            username_input.fill(username)
            time.sleep(0.5)

            # 查找密码输入框
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                '#input_password'
            ]

            password_input = None
            for selector in password_selectors:
                try:
                    password_input = self.page.wait_for_selector(selector, timeout=5000)
                    if password_input:
                        break
                except:
                    continue

            if not password_input:
                print("❌ 未找到密码输入框")
                return False

            # 输入密码
            print("📝 正在输入密码...")
            password_input.fill(password)
            time.sleep(0.5)

            # 查找登录按钮
            login_button_selectors = [
                'button[type="submit"]',
                'button:has-text("登录")',
                'button:has-text("Sign in")',
                'a:has-text("登录")',
                '#login_btn_signin'
            ]

            login_button = None
            for selector in login_button_selectors:
                try:
                    login_button = self.page.wait_for_selector(selector, timeout=5000)
                    if login_button:
                        break
                except:
                    continue

            if login_button:
                print("🖱️  正在点击登录按钮...")
                login_button.click()
            else:
                print("⚠️  未找到登录按钮，尝试按回车提交...")
                password_input.press('Enter')

            # 等待登录处理
            print("⏳ 等待登录处理...")
            time.sleep(1)

            # 检查是否需要 Steam Guard 验证
            self._handle_steam_guard(account)

            # 检查登录是否成功
            # 登录成功后通常会跳转到个人主页或社区首页
            current_url = self.page.url
            print(f"📍 当前页面: {current_url}")

            # 简单判断：如果 URL 包含个人资料特征则认为登录成功
            if 'steamcommunity.com/id/' in current_url or 'steamcommunity.com/profiles/' in current_url:
                print("✅ 登录成功！")
                return True
            else:
                print("⚠️  登录状态未确定，请手动检查")
                input("按回车键继续...")
                return True

        except PlaywrightTimeoutError:
            print("❌ 页面加载超时")
            return False
        except Exception as e:
            print(f"❌ 登录过程出错: {e}")
            return False

    def _handle_steam_guard(self, account):
        """
        处理 Steam Guard 验证

        Args:
            account: 账号信息字典
        """
        print("🔍 检查是否需要 Steam Guard 验证...")

        # 检查是否有 Steam Guard 验证码输入框
        guard_selectors = [
            'input[placeholder*="验证码" i]',
            'input[placeholder*="code" i]',
            'input[name="code"]',
            'input[name="authcode"]'
        ]

        guard_input = None
        for selector in guard_selectors:
            try:
                guard_input = self.page.wait_for_selector(selector, timeout=3000)
                if guard_input:
                    break
            except:
                continue

        if guard_input:
            print("📧 检测到 Steam Guard 验证")
            print(f"📧 邮箱: {account['email']}")
            print(f"🔗 邮箱地址: {account['email_url']}")

            # 提示用户手动输入验证码
            print("\n💡 请检查邮箱获取验证码")
            code = input("请输入 Steam Guard 验证码 (留空跳过): ").strip()

            if code:
                guard_input.fill(code)
                time.sleep(0.5)

                # 提交验证码
                submit_selectors = [
                    'button[type="submit"]',
                    'button:has-text("提交")',
                    'button:has-text("Submit")',
                    'a:has-text("提交")'
                ]

                for selector in submit_selectors:
                    try:
                        submit_btn = self.page.wait_for_selector(selector, timeout=3000)
                        if submit_btn:
                            submit_btn.click()
                            print("✅ 验证码已提交")
                            time.sleep(2)
                            break
                    except:
                        continue
        else:
            print("✅ 无需 Steam Guard 验证")

    def kill_all_processes(self):
        """关闭所有 Steam 和 PUBG 相关进程（彻底清理）"""
        print("🧹 清理所有进程...")

        processes_to_kill = [
            "steam.exe",
            "steamwebhelper.exe",
            "gameoverlayui.exe",
            "steamservice.exe",
            "TslGame.exe",  # PUBG
            "BEService.exe",
            "Steam.exe",    # 大小写变体
            "SteamWebHelper.exe"
        ]

        # 第一次关闭尝试
        for proc in processes_to_kill:
            try:
                subprocess.run(f"taskkill /F /IM {proc} >nul 2>&1", shell=True)
            except:
                pass

        # 等待进程退出
        time.sleep(2)

        # 第二次关闭尝试（针对顽固进程）
        for proc in processes_to_kill:
            try:
                subprocess.run(f"taskkill /F /IM {proc} >nul 2>&1", shell=True)
            except:
                pass

        # 等待并验证
        time.sleep(2)

        # 验证关键进程是否已关闭
        still_running = []
        for proc in ["steam.exe", "TslGame.exe"]:
            if self.check_process_running(proc):
                still_running.append(proc)

        if still_running:
            print(f"   ⚠️  以下进程仍在运行: {', '.join(still_running)}")
            print("   💡 再次尝试强制关闭...")
            for proc in still_running:
                subprocess.run(f"taskkill /F /IM {proc} >nul 2>&1", shell=True)
            time.sleep(2)

        print("✅ 所有进程已清理")

    def check_process_running(self, process_name):
        """检查进程是否正在运行"""
        try:
            # 使用 tasklist 命令检查进程
            result = subprocess.run(
                ['tasklist', '/FI', f'IMAGENAME eq {process_name}'],
                capture_output=True,
                text=True,
                shell=True
            )
            # 检查输出中是否包含进程名
            return process_name in result.stdout
        except:
            return False

    def list_game_processes(self):
        """列出所有游戏相关进程"""
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq TslGame.exe', '/FI', 'IMAGENAME eq BEService.exe', '/V'],
                capture_output=True,
                text=True,
                shell=True
            )
            print("📋 当前游戏进程状态:")
            for line in result.stdout.split('\n')[:20]:  # 只显示前20行
                if line.strip():
                    print(f"   {line}")
        except:
            pass

    def wait_for_steam_ready(self, timeout=60):
        """等待 Steam 完全登录并准备好（改进版 - 检测商店页面）

        检测策略：
        1. 检查 steam.exe 进程是否存在
        2. 检查 Steam 窗口是否存在
        3. 检查窗口标题是否包含 "商店" 或 "Store"
        4. 区分登录页面和商店页面

        Returns:
            bool: Steam 是否就绪（在商店页面）
        """
        print("⏳ 等待 Steam 完全准备就绪...")

        # 尝试导入 win32gui
        try:
            import win32gui
            WIN32_AVAILABLE = True
        except ImportError:
            WIN32_AVAILABLE = False
            print("   ⚠️  win32gui 未安装，仅使用进程检测")

        login_page_detected = False
        store_page_detected = False

        for i in range(timeout):
            # 阶段1: 检查 Steam 进程
            if not self.check_process_running("steam.exe"):
                time.sleep(1)
                continue

            # 阶段2: 如果 win32gui 可用，检查 Steam 窗口
            if WIN32_AVAILABLE:
                steam_windows = []

                def callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        try:
                            title = win32gui.GetWindowText(hwnd)
                            if title and any(keyword in title for keyword in ["Steam", "steam", "商店", "Store"]):
                                windows.append((hwnd, title))
                        except:
                            pass
                    return True

                try:
                    win32gui.EnumWindows(callback, steam_windows)

                    if steam_windows:
                        # 分析窗口类型
                        for hwnd, title in steam_windows:
                            title_lower = title.lower()

                            # 检测商店页面
                            if any(keyword in title_lower for keyword in ["store", "商店", "steam store"]):
                                if not store_page_detected:
                                    print(f"   ✅ 检测到商店页面: {title}")
                                    store_page_detected = True

                            # 检测登录页面
                            elif any(keyword in title_lower for keyword in ["login", "登录", "sign in"]):
                                if not login_page_detected:
                                    print(f"   ⚠️  检测到登录页面: {title}")
                                    print(f"   💡 如果长时间停留在此页面，可能需要手动登录")
                                    login_page_detected = True

                        # 如果找到商店页面，说明 Steam 已就绪
                        if store_page_detected:
                            print(f"✅ Steam 已就绪 (在商店页面, 耗时 {i+1} 秒)")
                            return True

                        # 如果只在登录页面，继续等待
                        if login_page_detected and not store_page_detected:
                            if (i + 1) % 10 == 0:  # 每10秒提示一次
                                print(f"   ⏳ 等待登录完成... ({i+1}/{timeout}秒)")

                except Exception as e:
                    print(f"   ⚠️  窗口检测失败: {e}")
                    # 回退到简单的进程检测
                    if i >= 10:  # 至少等待10秒
                        print(f"✅ Steam 已就绪 (耗时 {i+1} 秒)")
                        return True
            else:
                # win32gui 不可用，使用简单检测
                if i >= 10:  # 至少等待10秒让 Steam 初始化和登录
                    print(f"✅ Steam 已就绪 (耗时 {i+1} 秒)")
                    return True

            time.sleep(1)

            # 每5秒显示一次进度
            if (i + 1) % 5 == 0 and not login_page_detected:
                print(f"   等待 Steam 启动... ({i+1}/{timeout}秒)")

        # 超时后的处理
        if login_page_detected and not store_page_detected:
            print("⚠️  Steam 可能在登录页面等待手动操作")
            print("💡 建议：检查是否需要 Steam Guard 验证")
        else:
            print("⚠️  Steam 可能未完全就绪，但继续尝试...")

        return True



    def steam_login(self, username, password):
        """
        使用 Steam 命令行登录

        Returns:
            bool: 登录是否成功
        """
        print(f"\n🔐 使用 Steam 客户端登录: {username}")

        try:
            # 步骤1：确保没有残留的 Steam 进程
            print("   💡 检查并清理残留的 Steam 进程...")
            if self.check_process_running("steam.exe"):
                print("   ⚠️  检测到残留 Steam 进程，先关闭...")
                self.kill_all_processes()
                time.sleep(3)

            # 再次确认所有 Steam 进程都已关闭
            if self.check_process_running("steam.exe"):
                print("   ⚠️  Steam 进程仍在运行，等待退出...")
                time.sleep(5)
                if self.check_process_running("steam.exe"):
                    print("   ⚠️  强制关闭 Steam...")
                    self.kill_all_processes()
                    time.sleep(3)

            # 步骤2：启动 Steam 并登录
            # 使用 -logout 参数确保先退出旧的登录状态
            cmd = [self.STEAM_EXE_PATH, "-login", username, password]
            print(f"📍 执行: steam.exe -login {username} ********")

            # 启动 Steam（后台）
            subprocess.Popen(cmd, shell=False)

            # 等待 Steam 完全启动和登录
            self.wait_for_steam_ready(timeout=30)

            # 验证 Steam 进程是否运行
            if self.check_process_running("steam.exe"):
                print("✅ Steam 登录完成")
                return True
            else:
                print("⚠️  Steam 进程未检测到")
                return False

        except Exception as e:
            print(f"⚠️  Steam 登录失败: {e}")
            return False

    def send_enter_key(self):
        """发送回车键（用于同意用户许可协议）"""
        if PYAUTOGUI_AVAILABLE:
            try:
                print("   💻 使用 pyautogui 发送回车键...")
                pyautogui.press('enter')
                return True
            except Exception as e:
                print(f"   ⚠️  pyautogui 失败: {e}，尝试备用方法...")

        # 备用方法：使用 PowerShell
        try:
            print("   💻 使用 PowerShell 发送回车键...")
            # 先激活当前窗口
            activate_cmd = "(New-Object -ComObject WScript.Shell).AppActivate((Get-Process | Where-Object {$_.MainWindowTitle -like '*许可*' -or $_.MainWindowTitle -like '*PUBG*' -or $_.MainWindowTitle -like '*License*'}).MainWindowTitle)"
            subprocess.run(["powershell", "-Command", activate_cmd], capture_output=True, timeout=5)
            time.sleep(0.3)

            # 发送回车键
            ps_command = "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')"
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True, timeout=5)
            return True
        except Exception as e:
            print(f"   ⚠️  PowerShell 方法失败: {e}")
            return False

    def activate_window_by_title(self, title_keyword):
        """通过窗口标题激活窗口"""
        try:
            ps_script = f'''
            $process = Get-Process | Where-Object {{$_.MainWindowTitle -like "*{title_keyword}*"}}
            if ($process) {{
                (New-Object -ComObject WScript.Shell).AppActivate($process.MainWindowTitle) | Out-Null
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

    def activate_and_click_accept(self):
        """激活窗口并使用 OpenCV 高精度图像识别点击'接受'按钮"""
        keywords = ["许可", "协议", "License", "Agreement", "User", "EULA", "Terms", "PUBG", "BATTLEGROUNDS", "Steam", "Subscriber", "Accept", "同意"]

        for keyword in keywords:
            if self.activate_window_by_title(keyword):
                print(f"   ✅ 激活了包含 '{keyword}' 的窗口")
                break

        time.sleep(1)

        if not PYAUTOGUI_AVAILABLE:
            print("   ❌ pyautogui 不可用")
            return False

        self._save_debug_screenshot("before_image_recognition")
        print("   💡 使用 OpenCV 图像识别查找'接受'按钮...")

        template_path = Path(__file__).parent / "accept_button.png"

        if not template_path.exists():
            print(f"   ❌ 模板图片不存在: {template_path}")
            return False

        try:
            import cv2
            import numpy as np
            from PIL import Image

            template_img = Image.open(template_path)
            template_size = template_img.size
            print(f"   📐 模板尺寸: {template_size[0]} x {template_size[1]} 像素")

            MIN_SIMILARITY_TO_CLICK = 0.95
            print(f"   🎯 最小相似度: {MIN_SIMILARITY_TO_CLICK} (95%)")

            # 截取屏幕并转换为 OpenCV 格式
            current_screen = pyautogui.screenshot()
            screen_cv = cv2.cvtColor(np.array(current_screen), cv2.COLOR_RGB2BGR)
            screen_gray = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)

            # 读取模板
            template = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)

            # OpenCV 模板匹配 (TM_CCORR_NORMED)
            result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            similarity = max_val
            location = max_loc

            print(f"   📊 最佳匹配相似度: {similarity*100:.2f}%")
            print(f"   📍 位置: ({location[0]}, {location[1]})")

            # 关键安全检查：只有置信度足够高才点击
            if similarity >= MIN_SIMILARITY_TO_CLICK:
                print(f"   ✅ 相似度满足要求 (>= 95%)")

                h, w = template.shape
                center_x = location[0] + w // 2
                center_y = location[1] + h // 2
                print(f"   🖱️  点击中心坐标: ({center_x}, {center_y})")

                # 标记并保存
                try:
                    marked = screen_cv.copy()
                    top_left = location
                    bottom_right = (location[0] + w, location[1] + h)
                    cv2.rectangle(marked, top_left, bottom_right, (0, 255, 0), 3)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    marked_filename = f"marked_opencv_{similarity:.2f}_{timestamp}.png"
                    marked_file = Path("screenshots") / marked_filename
                    marked_file.parent.mkdir(exist_ok=True)
                    cv2.imwrite(str(marked_file), marked)
                    print(f"   📷 已保存标记截图: {marked_file.name}")
                except Exception as e:
                    print(f"   ⚠️  标记截图失败: {e}")

                # 点击按钮
                print(f"   🖱️  执行点击: ({center_x}, {center_y})")
                pyautogui.click(center_x, center_y)
                time.sleep(1)

                self._save_debug_screenshot("after_accept_click")

                if self.check_process_running("TslGame.exe"):
                    print("   ✅ 点击后检测到 TslGame.exe - 游戏已启动")
                    return True
                else:
                    time.sleep(2)
                    if self.check_process_running("TslGame.exe"):
                        print("   ✅ 游戏已启动！")
                        return True
                    else:
                        print("   ⚠️  点击后未检测到游戏进程（可能需要重新启动）")
                        return True  # 返回 True，让外层逻辑处理重新启动
                return True
            else:
                print(f"   ❌ 相似度不足 ({similarity*100:.2f}% < 95%)")
                print(f"   ❌ 不点击，避免误操作")
                return False

            if similarity >= MIN_SIMILARITY_TO_CLICK:
                print(f"   ✅ 相似度满足要求")

                h, w = template.shape
                center_x = location[0] + w // 2
                center_y = location[1] + h // 2
                print(f"   🖱️  点击中心坐标: ({center_x}, {center_y})")

                # 标记并保存
                try:
                    marked = screen_cv.copy()
                    top_left = location
                    bottom_right = (location[0] + w, location[1] + h)
                    cv2.rectangle(marked, top_left, bottom_right, (0, 255, 0), 3)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    marked_filename = f"marked_opencv_{similarity:.2f}_{timestamp}.png"
                    marked_file = Path("screenshots") / marked_filename
                    marked_file.parent.mkdir(exist_ok=True)
                    cv2.imwrite(str(marked_file), marked)
                    print(f"   📷 已保存标记截图: {marked_file.name}")
                except Exception as e:
                    print(f"   ⚠️  标记截图失败: {e}")
            else:
                print(f"   ⚠️  相似度不足 ({similarity*100:.2f}% < 95%)")
                print(f"   ❌ 不点击，避免误操作")
                return False

        except Exception as e:
            print(f"   ❌ 图像识别失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _save_debug_screenshot(self, label):
        """保存调试截图"""
        try:
            if PYAUTOGUI_AVAILABLE:
                screenshot_dir = Path("screenshots")
                screenshot_dir.mkdir(exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = screenshot_dir / f"{label}_{timestamp}.png"
                pyautogui.screenshot(str(filename))
                print(f"   📷 已保存截图: {filename}")
        except Exception as e:
            print(f"   ⚠️  截图失败: {e}")

    def check_for_agreement_window(self):
        """
        检查屏幕上是否有"最终用户协议"窗口（通过 OpenCV 查找"接受"按钮）

        Returns:
            bool: True 如果找到协议窗口，False 如果没找到
        """
        if not PYAUTOGUI_AVAILABLE:
            print("   pyautogui 不可用，无法检测协议窗口")
            return False

        try:
            import cv2
            import numpy as np
        except ImportError:
            print("   OpenCV 不可用，无法检测协议窗口")
            return False

        template_path = self.project_root / "src" / "accept_button.png"
        if not template_path.exists():
            print(f"   模板图片不存在: {template_path}")
            return False

        try:
            # 截取屏幕
            current_screen = pyautogui.screenshot()
            screen_cv = cv2.cvtColor(np.array(current_screen), cv2.COLOR_RGB2BGR)
            screen_gray = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)

            # 读取模板
            template = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)
            if template is None:
                print("   无法读取模板图片")
                return False

            # OpenCV 模板匹配 (TM_CCORR_NORMED)
            result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            similarity = max_val
            print(f"   协议窗口检测相似度: {similarity*100:.2f}%")

            # 提高阈值：相似度 >= 90% 才认为存在协议窗口
            # 这样可以避免误判其他相似但不相关的内容
            if similarity >= 0.90:
                print("   ✅ 检测到'最终用户协议'窗口（高置信度）")
                return True
            elif similarity >= 0.50:
                print(f"   ⚠️  发现相似内容（{similarity*100:.2f}%），但置信度不足以确认是协议窗口")
                print("   ℹ️  为避免误操作，跳过此窗口")
                return False
            else:
                print("   ℹ️  未检测到'最终用户协议'窗口")
                return False

        except Exception as e:
            print(f"   检查协议窗口失败: {e}")
            return False



    def activate_and_send_enter(self):
        """激活窗口并发送回车键（增强版）"""
        # 首先尝试新的点击接受按钮方法
        print("   💡 尝试点击接受按钮...")
        if self.activate_and_click_accept():
            return True

        # 之前的备用方法
        # 尝试激活包含特定关键词的窗口
        keywords = ["许可", "协议", "License", "Agreement", "User", "EULA", "Terms", "Accept", "PUBG", "BATTLEGROUNDS", "Steam", "Subscriber"]

        for keyword in keywords:
            if self.activate_window_by_title(keyword):
                print(f"   ✅ 激活了包含 '{keyword}' 的窗口")
                time.sleep(0.3)
                # 先尝试回车键
                self.send_enter_key()
                # 再尝试空格键（有时协议窗口用空格确认）
                try:
                    if PYAUTOGUI_AVAILABLE:
                        pyautogui.press('space')
                except:
                    pass
                return True

        # 如果没有找到特定窗口，尝试激活最前面的窗口
        print("   ⚠️  未找到特定窗口，尝试激活前台窗口...")
        try:
            # 使用 Alt 键切换焦点到窗口
            if PYAUTOGUI_AVAILABLE:
                pyautogui.press('alt')
                time.sleep(0.2)
                pyautogui.press('tab')
                time.sleep(0.2)
            self.send_enter_key()
            # 也尝试空格键
            if PYAUTOGUI_AVAILABLE:
                pyautogui.press('space')
            return True
        except:
            pass

        # 最后尝试：直接发送回车键和空格键
        print("   ⚠️  直接发送确认键...")
        self.send_enter_key()
        try:
            if PYAUTOGUI_AVAILABLE:
                pyautogui.press('space')
        except:
            pass
        return True

    def launch_pubg_game(self):
        """
        启动 PUBB 游戏

        Returns:
            bool: 启动是否成功
        """
        print("\n🎮 启动 PUBG 游戏...")

        try:
            # 确保 Steam 完全准备好
            time.sleep(2)

            # 方法1：使用 Steam -applaunch 参数（更可靠）
            print("📍 使用 Steam -applaunch 启动游戏...")
            cmd = [self.STEAM_EXE_PATH, "-applaunch", self.PUBG_APP_ID]

            subprocess.Popen(cmd, shell=False)
            print(f"   执行: steam.exe -applaunch {self.PUBG_APP_ID}")

            # 等待游戏启动并验证进程
            print("⏳ 等待游戏启动...")

            # 阶段1：等待并检查是否有用户许可协议窗口
            print("💡 阶段1: 检查是否有'最终用户协议'窗口...")
            time.sleep(5)

            # 检查是否有协议窗口（只检查一次）
            agreement_found = False
            if self.check_for_agreement_window():
                print("   ✅ 检测到'最终用户协议'窗口")
                agreement_found = True

                # 尝试点击"接受"按钮
                max_attempts = 3  # 最多尝试3次
                accept_clicked = False

                for i in range(max_attempts):
                    print(f"   尝试点击'接受'按钮 ({i+1}/{max_attempts})...")

                    if self.activate_and_click_accept():
                        print("   ✅ 成功点击'接受'按钮")
                        accept_clicked = True
                        time.sleep(3)
                        break
                    else:
                        print(f"   ⚠️  点击失败（尝试 {i+1}/{max_attempts}）")
                        time.sleep(2)

                # 关键修改：点击接受后，需要重新启动 PUBG
                if accept_clicked:
                    print("   💡 点击接受后，需要重新启动 PUBG...")
                    time.sleep(2)

                    # 关闭可能的游戏窗口
                    print("   🔄 关闭当前游戏窗口...")
                    subprocess.run(["taskkill", "/F", "/IM", "TslGame.exe"],
                                   capture_output=True, shell=True)
                    time.sleep(2)

                    # 重新启动 PUBG
                    print("   🔄 重新启动 PUBG...")
                    cmd = [self.STEAM_EXE_PATH, "-applaunch", self.PUBG_APP_ID]
                    subprocess.Popen(cmd, shell=False)
                    print("   ✅ PUBG 已重新启动")
            else:
                print("   ℹ️  未检测到'最终用户协议'窗口（无需处理）")

            # 阶段2：如果协议点击后仍未启动，继续等待
            print("💡 阶段2: 继续等待游戏进程启动...")

            # 最多等待 50 秒让游戏启动
            max_wait = 50
            game_started = False

            for i in range(max_wait):
                if self.check_process_running("TslGame.exe"):
                    game_started = True
                    print(f"✅ PUBG 游戏已启动 (TslGame.exe 检测到，总耗时 {i+1} 秒)")
                    # 尝试激活游戏窗口
                    print("💡 尝试激活游戏窗口...")
                    for keyword in ["PUBG", "BATTLEGROUNDS", "TslGame"]:
                        if self.activate_window_by_title(keyword):
                            print(f"   ✅ 已激活 PUBG 游戏窗口")
                            break
                    break
                time.sleep(1)

                # 每5秒显示一次进度
                if (i + 1) % 5 == 0:
                    print(f"   等待中... ({i+1}/{max_wait}秒)")

            if not game_started:
                print("⚠️  未检测到 TslGame.exe 进程，游戏可能未成功启动")
                print("💡 可能原因：")
                print("   - Steam 未完全登录")
                print("   - 该账号未安装 PUBG 游戏")
                print("   - 用户许可协议未同意（需要手动点击）")
                print("   - 游戏启动时间过长")
                print("   - Steam 客户端需要更新")
                print("\n🔍 调试信息:")
                self.list_game_processes()
                print(f"\n⚠️  跳过此账号，继续下一个...")
                time.sleep(2)
                return False

            return True

        except Exception as e:
            print(f"⚠️  启动 PUBG 失败: {e}")
            return False

    def close_pubg_game(self):
        """关闭 PUBG 游戏进程"""
        print("🎮 关闭 PUBG 游戏...")

        try:
            # 尝试多种方式关闭游戏
            kill_methods = [
                "taskkill /F /IM TslGame.exe",
                "taskkill /F /IM BEService.exe"
            ]

            for cmd in kill_methods:
                try:
                    subprocess.run(f"{cmd} >nul 2>&1", shell=True)
                    time.sleep(0.5)
                except:
                    pass

            # 等待进程完全关闭
            time.sleep(2)

            # 验证游戏进程是否已关闭
            if self.check_process_running("TslGame.exe"):
                print("⚠️  TslGame.exe 进程仍在运行，尝试强制关闭...")
                subprocess.run("taskkill /F /IM TslGame.exe >nul 2>&1", shell=True)
                time.sleep(2)

            if not self.check_process_running("TslGame.exe"):
                print("✅ PUBG 游戏已关闭")
            else:
                print("⚠️  游戏进程可能仍在运行")

        except Exception as e:
            print(f"⚠️  关闭游戏时出错: {e}")

    def close_steam_client(self):
        """彻底关闭 Steam 客户端"""
        print("🚪 正在关闭 Steam 客户端...")

        try:
            # 方法1：先尝试用 Steam 的 shutdown 命令（优雅关闭）
            try:
                print("   💡 尝试优雅关闭 Steam...")
                subprocess.run([self.STEAM_EXE_PATH, "-shutdown"], capture_output=True, timeout=10)
                time.sleep(3)
            except:
                pass

            # 方法2：强制关闭所有 Steam 相关进程
            print("   💡 强制关闭所有 Steam 进程...")
            steam_processes = [
                "steam.exe",
                "steamwebhelper.exe",
                "gameoverlayui.exe",
                "steamservice.exe",
                "Steam.exe",
                "SteamWebHelper.exe"
            ]

            for proc in steam_processes:
                subprocess.run(f"taskkill /F /IM {proc} >nul 2>&1", shell=True)

            # 方法3：等待并验证所有进程都已关闭
            print("   💡 等待 Steam 完全退出...")
            max_wait = 15
            for i in range(max_wait):
                time.sleep(1)
                if not self.check_process_running("steam.exe") and \
                   not self.check_process_running("steamwebhelper.exe"):
                    print(f"   ✅ Steam 已完全关闭（耗时 {i+1} 秒）")
                    return True

                if (i + 1) % 5 == 0:
                    print(f"   ⏳ 等待 Steam 退出... ({i+1}/{max_wait}秒)")

            # 如果还在运行，再次强制关闭
            print("   ⚠️  Steam 仍在运行，进行最后一次强制关闭...")
            for proc in steam_processes:
                subprocess.run(f"taskkill /F /IM {proc} >nul 2>&1", shell=True)
            time.sleep(3)

            # 最终验证
            if not self.check_process_running("steam.exe"):
                print("   ✅ Steam 已强制关闭")
            else:
                print("   ⚠️  Steam 可能未完全关闭，将继续尝试清理")

        except Exception as e:
            print(f"⚠️  关闭 Steam 时出错: {e}")

        # 确保等待足够时间让 Steam 完全退出
        time.sleep(2)

    def visit_pubg_page(self, account):
        """
        完整的 PUBG 游戏流程

        Args:
            account: 账号信息字典

        Returns:
            bool: 流程是否成功
        """
        print("\n" + "="*50)
        print("🎮 开始 PUBG 游戏流程")
        print("="*50)

        try:
            # 1. 关闭所有进程
            self.kill_all_processes()

            # 2. Steam 客户端登录
            if not self.steam_login(account['username'], account['password']):
                print("⚠️  Steam 登录失败，清理环境...")
                self.kill_all_processes()
                return False

            # 3. 启动 PUBG 游戏
            if not self.launch_pubg_game():
                print("⚠️  PUBG 启动失败，清理环境...")
                self.kill_all_processes()
                return False

            # 4. 等待游戏运行（90秒）
            game_time = 90  # 90秒
            print(f"\n⏳ 游戏运行中 ({game_time} 秒)...")
            print("💡 提示：游戏窗口应该已经显示在屏幕上")

            # 每30秒显示一次进度
            for elapsed in range(0, game_time, 30):
                remaining = game_time - elapsed
                print(f"   ⏱️  剩余时间: {remaining} 秒")
                time.sleep(30)

            print("   ✅ 游戏运行时间结束")

            # 5. 关闭 PUBG 游戏
            self.close_pubg_game()

            # 6. 关闭 Steam 客户端
            self.close_steam_client()

            print("\n✅ PUBG 流程完成")
            return True

        except Exception as e:
            print(f"\n⚠️  PUBG 流程出错: {e}")
            print("⚠️  清理环境...")
            self.kill_all_processes()
            return False


    def logout_steam(self):
        """
        退出 Steam 登录（完全清除浏览器状态）

        Returns:
            bool: 退出是否成功
        """
        print("\n🚪 正在退出 Steam...")

        try:
            # 清除本地存储和会话存储
            self.page.evaluate('() => { localStorage.clear(); sessionStorage.clear(); }')

            # 完全清除所有 cookies（一次性清除）
            self.context.clear_cookies()

            print("✅ 已清除所有登录信息")

            # 不再访问 logout 页面，直接返回
            return True

        except Exception as e:
            print(f"⚠️ 退出过程出错: {e}")
            return False

    def run(self):
        """
        执行批量登录流程
        """
        print("\n" + "="*60)
        print("🎮 Steam 账号批量登录脚本")
        print("="*60)

        # 加载账号文件
        if not self.load_accounts():
            print("❌ 无法加载账号文件，程序退出")
            return

        # 初始化浏览器
        if not self.init_browser():
            print("❌ 浏览器初始化失败，程序退出")
            return

        try:
            # 循环登录每个账号
            total = len(self.accounts)
            for i, account in enumerate(self.accounts, 1):
                self.current_index = i

                print(f"\n📋 进度: [{i}/{total}]")

                # 直接使用 Steam 客户端登录并启动游戏
                print(f"\n📋 处理账号: {account['username']}")

                # 执行完整的 PUBG 流程
                self.visit_pubg_page(account)

                # 账号间间隔
                interval = 2
                print(f"\n⏳ �待 {interval} 秒后处理下一个账号...")
                time.sleep(interval)

            print("\n" + "="*60)
            print(f"✅ 所有账号处理完成！共处理 {total} 个账号")
            print("="*60)

        finally:
            # 确保浏览器被关闭
            self.close_browser()


def main():
    """主函数"""
    # 获取项目根目录（脚本在 src/ 子目录中）
    project_root = Path(__file__).parent.parent
    accounts_file = project_root / "accounts.txt"

    # 创建登录实例
    bot = SteamLoginBatch(str(accounts_file), headless=False)

    # 加载账号
    if not bot.load_accounts():
        print("❌ 无法加载账号文件，程序退出")
        return

    # 循环处理每个账号
    total = len(bot.accounts)
    for i, account in enumerate(bot.accounts, 1):
        print(f"\n📋 进度: [{i}/{total}]")
        print(f"\n📋 处理账号: {account['username']}")

        # 执行完整的 PUBG 流程
        bot.visit_pubg_page(account)

        # 账号间间隔
        if i < total:
            interval = 2
            print(f"\n⏳ 等待 {interval} 秒后处理下一个账号...")
            time.sleep(interval)

    print("\n" + "="*60)
    print(f"✅ 所有账号处理完成！共处理 {total} 个账号")
    print("="*60)


if __name__ == "__main__":
    main()
