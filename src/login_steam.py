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
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class SteamLoginBatch:
    """Steam 批量登录类"""

    # Steam 页面 URL
    STEAM_LOGIN_URL = "https://steamcommunity.com/login/home/"

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
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

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

                # 登录
                if self.login_steam(account):
                    print(f"✅ 账号 {account['username']} 登录成功")

                    # 立即退出，无需等待
                    self.logout_steam()
                else:
                    interval = 1
                    print(f"⏳ 等待 {interval} 秒后处理下一个账号...")
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

    # 创建登录实例并执行
    # headless=False 表示显示浏览器窗口，便于调试
    bot = SteamLoginBatch(str(accounts_file), headless=False)
    bot.run()


if __name__ == "__main__":
    main()
