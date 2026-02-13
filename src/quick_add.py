#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速添加账号工具 v4 - Tab 格式版
功能：支持 tab 分隔，更清晰易读
"""

import os
import sys
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def parse_account_tab_format(text):
    """
    解析 tab 分隔格式账号

    格式：账号	密码	邮箱	邮箱密码	邮箱地址
    """
    text = text.strip()

    # 按 tab 分隔
    parts = text.split('\t')

    # 清理每个部分
    parts = [p.strip() for p in parts if p.strip()]

    # 验证
    if len(parts) >= 2:
        return {
            'username': parts[0] if len(parts) > 0 else '',
            'password': parts[1] if len(parts) > 1 else '',
            'email': parts[2] if len(parts) > 2 else '',
            'email_password': parts[3] if len(parts) > 3 else '',
            'email_url': parts[4] if len(parts) > 4 else ''
        }

    return None


def format_account_tab(account):
    """格式化为 tab 分隔行"""
    return "{username}\t{password}\t{email}\t{email_password}\t{email_url}".format(**account)


def show_account_preview(account, index=None):
    """显示账号预览"""
    print(f"\n✅ 成功识别账号信息:")
    print(f"   Steam账号: {account['username']}")
    print(f"   Steam密码: {'*' * len(account['password'])}")
    if account.get('email'):
        print(f"   邮箱账号: {account['email']}")
    if account.get('email_password'):
        print(f"   邮箱密码: {'*' * len(account['email_password'])}")
    if account.get('email_url'):
        print(f"   邮箱地址: {account['email_url']}")
    if index:
        print(f"   (第 {index} 个)")
    print()


def save_to_accounts_file(accounts):
    """保存账号到 accounts.txt"""
    project_root = Path(__file__).parent.parent
    accounts_file = project_root / "accounts.txt"

    try:
        # 读取现有内容
        existing_lines = []
        if accounts_file.exists():
            with open(accounts_file, 'r', encoding='utf-8') as f:
                existing_lines = f.readlines()

        # 写入文件
        with open(accounts_file, 'w', encoding='utf-8') as f:
            # 保留原有注释和空行
            for line in existing_lines:
                if line.strip().startswith('#') or line.strip() == '':
                    f.write(line)

            # 添加新账号
            f.write('\n# 以下是通过快速添加工具导入的账号\n')
            f.write('# ============================================\n\n')
            for account in accounts:
                f.write(format_account_tab(account) + '\n')

        print(f"\n✅ 成功保存 {len(accounts)} 个账号到: {accounts_file}")
        print(f"📁 文件位置: {accounts_file.absolute()}")
        return True

    except Exception as e:
        print(f"\n❌ 保存失败: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🚀 Steam 账号快速添加工具 v4 - Tab 格式版")
    print("="*70)
    print("\n💡 新格式：tab 分隔（更清晰易读）")
    print("\n💡 格式说明：")
    print("   Steam账号	密码	邮箱	邮箱密码	邮箱地址")
    print("   每个字段用 tab 键分隔\n")

    print("\n💡 示例：")
    print("   rex78532	PeF753606	n7w77v@sdhgz.cn	374777	a.dcmya.com")

    print("\n💡 命令:")
    print("   done/exit - 保存并退出")
    print("   list/show  - 查看已添加的账号")
    print("   clear       - 清空已添加的账号")
    print("   preview    - 显示账号详细信息")
    print("   help/?     - 显示格式帮助\n")

    accounts = []

    while True:
        print("\n" + "-"*70)
        try:
            user_input = input("📝 请粘贴账号信息 (或输入命令): ").strip()

            if not user_input:
                continue

            # 退出命令
            if user_input.lower() in ['done', 'exit', '退出', '完成', 'q']:
                if accounts:
                    print(f"\n📋 准备保存 {len(accounts)} 个账号...")
                    if save_to_accounts_file(accounts):
                        print("\n" + "="*70)
                        print("✅ 完成！")
                        print("="*70)
                        print("\n💾 下一步：运行登录脚本")
                        print("   python src\\login_steam.py")
                        print()
                else:
                    print("\n⚠️  还没有添加任何账号")
                    choice = input("确定退出吗？(y/n): ").strip().lower()
                    if choice == 'y':
                        break
                continue

            # 清空命令
            if user_input.lower() == 'clear':
                accounts = []
                print("✅ 已清空账号列表\n")
                continue

            # 查看已添加
            if user_input.lower() in ['list', '查看', 'show', 'ls']:
                if not accounts:
                    print("\n⚠️  还没有添加任何账号\n")
                else:
                    print(f"\n📋 已添加 {len(accounts)} 个账号:")
                    for i, acc in enumerate(accounts, 1):
                        email = acc.get('email', 'N/A')
                        print(f"   {i}. {acc['username']}\t{email}")
                continue

            # 帮助命令
            if user_input.lower() in ['help', '帮助', 'h', '?']:
                print("\n📖 Tab 格式帮助:\n")
                print("格式：字段用 tab 键分隔")
                print("顺序：Steam账号	密码	邮箱	邮箱密码	邮箱地址")
                print("\n示例：")
                print("   rex78532	PeF753606	n7w77v@sdhgz.cn	374777	a.dcmya.com")
                print("\n💡 命令:")
                print("   done/exit - 保存并退出")
                print("   list/show  - 查看已添加的账号")
                print("   clear       - 清空已添加的账号")
                print("   preview    - 显示账号详细信息")
                continue

            # 预览模式切换
            if user_input.lower() == 'preview':
                preview_mode = True
                print("\n🔍 预览模式已开启（输入信息会显示详细信息）")
                print("   输入 'preview' 再次关闭预览模式\n")
                continue

            # 尝试解析
            account = parse_account_tab_format(user_input)

            if account:
                # 显示结果
                if user_input.lower() != 'preview':
                    print(f"\n✅ 成功识别账号信息:")
                    show_account_preview(account, len(accounts) + 1)
                else:
                    # 预览模式
                    show_account_preview(account, len(accounts) + 1)

                accounts.append(account)
                print(f"\n✅ 已添加到列表，当前共 {len(accounts)} 个")

            else:
                print("\n❌ 无法识别账号信息")
                print("💡 请确保至少包含：")
                print("   • Steam账号")
                print("   • Steam密码")
                print("   • 其他字段可选")
                print("\n💡 输入 'help' 查看格式示例")

        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断")
            break


if __name__ == "__main__":
    main()
