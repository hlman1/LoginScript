#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam 账号配置工具
功能：通过简单问答的方式添加账号到 accounts.txt
"""

import os
import sys
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class AccountConfig:
    """账号配置工具类"""

    def __init__(self, accounts_file="accounts.txt"):
        """
        初始化

        Args:
            accounts_file: 账号文件路径
        """
        # 获取项目根目录
        self.project_root = Path(__file__).parent.parent
        self.accounts_file = self.project_root / accounts_file
        self.accounts = []

    def load_existing_accounts(self):
        """加载已存在的账号（排除注释行）"""
        if not self.accounts_file.exists():
            return

        with open(self.accounts_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                self.accounts.append(line)

    def input_account(self):
        """
        交互式输入一个账号

        Returns:
            str: 格式化后的账号字符串
        """
        print("\n" + "="*50)
        print("📝 添加新账号")
        print("="*50)

        # 输入 Steam 账号
        while True:
            username = input("\n1️⃣ 请输入 Steam 账号名: ").strip()
            if username:
                break
            print("❌ 账号名不能为空，请重新输入！")

        # 输入 Steam 密码
        while True:
            password = input("2️⃣ 请输入 Steam 密码: ").strip()
            if password:
                break
            print("❌ 密码不能为空，请重新输入！")

        # 确认密码
        password_confirm = input("   确认密码（直接回车跳过）: ").strip()
        if password_confirm and password_confirm != password:
            print("❌ 两次密码不一致，请重新输入！")
            return self.input_account()

        # 输入邮箱
        while True:
            email = input("3️⃣ 请输入邮箱地址: ").strip()
            if email:
                break
            print("❌ 邮箱不能为空，请重新输入！")

        # 输入邮箱密码
        while True:
            email_password = input("4️⃣ 请输入邮箱密码: ").strip()
            if email_password:
                break
            print("❌ 邮箱密码不能为空，请重新输入！")

        # 输入邮箱网站/地址
        while True:
            email_url = input("5️⃣ 请输入邮箱网站（如: mail.qq.com）: ").strip()
            if email_url:
                # 移除可能的协议前缀
                email_url = email_url.replace("https://", "").replace("http://", "").strip()
                break
            print("❌ 邮箱网站不能为空，请重新输入！")

        # 组合格式
        account_str = f"{username}:{password}:{email}:{email_password}:{email_url}"

        # 显示确认信息
        print("\n" + "-"*50)
        print("📋 账号信息确认：")
        print("-"*50)
        print(f"Steam 账号: {username}")
        print(f"Steam 密码: {'*' * len(password)}")
        print(f"邮箱地址: {email}")
        print(f"邮箱网站: {email_url}")
        print("-"*50)

        # 确认保存
        confirm = input("\n✅ 确认保存这个账号？(y/n): ").strip().lower()

        if confirm == 'y':
            return account_str
        else:
            print("❌ 已取消保存")
            return None

    def save_accounts(self):
        """保存账号到文件"""
        try:
            # 读取原文件内容（保留注释行）
            original_lines = []
            if self.accounts_file.exists():
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    original_lines = f.readlines()

            # 写入文件
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                # 先写入原文件的注释和空行
                for line in original_lines:
                    if line.strip().startswith('#') or line.strip() == '':
                        f.write(line)

                # 添加分隔注释
                f.write("\n# ============================================\n")
                f.write("# 下方是自动添加的账号\n")
                f.write("# ============================================\n\n")

                # 写入账号
                for account in self.accounts:
                    f.write(account + '\n')

            print(f"\n✅ 成功保存 {len(self.accounts)} 个账号到: {self.accounts_file}")
            return True

        except Exception as e:
            print(f"\n❌ 保存失败: {e}")
            return False

    def run(self):
        """运行配置工具"""
        print("\n" + "="*60)
        print("🛠️  Steam 账号配置工具")
        print("="*60)
        print("\n这个工具会帮助你轻松添加账号到 accounts.txt 文件")
        print("所有信息都保存在本地，不会上传到任何地方\n")

        # 加载已存在的账号
        self.load_existing_accounts()
        if self.accounts:
            print(f"📋 当前已有 {len(self.accounts)} 个账号\n")

        # 循环添加账号
        while True:
            print("\n" + "="*60)
            print("请选择操作：")
            print("  1. 添加新账号")
            print("  2. 查看已有账号")
            print("  0. 保存并退出")
            print("="*60)

            choice = input("\n请输入选项 (0/1/2): ").strip()

            if choice == '1':
                account = self.input_account()
                if account:
                    self.accounts.append(account)
                    print("\n✅ 账号已添加到待保存列表\n")

            elif choice == '2':
                if not self.accounts:
                    print("\n⚠️  还没有添加任何账号\n")
                else:
                    print("\n📋 已添加的账号列表：")
                    print("-"*60)
                    for i, account in enumerate(self.accounts, 1):
                        parts = account.split(':')
                        if len(parts) >= 2:
                            print(f"{i}. 账号: {parts[0]} | 邮箱: {parts[2] if len(parts) > 2 else 'N/A'}")
                    print("-"*60 + "\n")

            elif choice == '0':
                if self.accounts:
                    # 保存账号
                    if self.save_accounts():
                        print("\n" + "="*60)
                        print("✅ 配置完成！")
                        print("="*60)
                        print(f"\n📁 账号已保存到: {self.accounts_file}")
                        print(f"📝 共保存了 {len(self.accounts)} 个账号")
                        print("\n💡 现在可以运行登录脚本了:")
                        print(f"   python src{os.sep}login_steam.py")
                        print()
                else:
                    print("\n⚠️  你还没有添加任何账号")
                    re_input = input("是否真的要退出？(y/n): ").strip().lower()
                    if re_input == 'y':
                        break
                break

            else:
                print("\n❌ 无效选项，请重新输入！")


def main():
    """主函数"""
    config = AccountConfig()
    config.run()


if __name__ == "__main__":
    main()
