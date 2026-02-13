#usr/bin/env python3
# -*- coding: utf-8 -*-
"""
账号格式转换工具 v6 - 文件批量导入版
功能：将中文格式转换为 Tab 分隔格式
新增：支持从文件批量导入
"""

import sys
import re
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def parse_chinese_format(text):
    """
    解析中文格式的账号信息

    支持的关键词：
    - steam账号/账号
    - 密码
    - 邮箱账号/邮箱
    - 邮箱密码
    - 邮箱地址/邮箱登录地址/邮箱网站
    """
    text = text.strip()

    result = {}

    # 定义所有需要查找的关键词
    all_keywords = [
        'steam账号', '账号',
        '密码',
        '邮箱账号', '邮箱',
        '邮箱密码',
        '邮箱登录地址', '邮箱地址', '邮箱网站'
    ]

    # 构建停止词集合（用于提取字段时知道到哪里停止）
    stop_patterns = []
    for kw in all_keywords:
        stop_patterns.append(kw)

    # 1. 提取 steam账号/账号
    for kw in ['steam账号', '账号']:
        pattern = re.compile(re.escape(kw) + r'(\S+?)(?=' + '|'.join([re.escape(k) for k in stop_patterns if k not in [kw, '账号']]) + r'|$)', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            result['username'] = match.group(1).strip()
            break

    # 2. 提取密码
    for kw in ['密码']:
        # 密码后面应该跟着"邮箱"相关的关键词
        pattern = re.compile(re.escape(kw) + r'(\S+?)(?=邮箱账号|邮箱密码|邮箱$)', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            result['password'] = match.group(1).strip()
            break

    # 3. 提取邮箱账号/邮箱
    for kw in ['邮箱账号', '邮箱']:
        # 邮箱后面应该跟着"邮箱密码"
        pattern = re.compile(re.escape(kw) + r'(\S+?)(?=邮箱密码|$)', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            result['email'] = match.group(1).strip()
            break

    # 4. 提取邮箱密码
    for kw in ['邮箱密码']:
        # 邮箱密码后面跟着"邮箱地址"相关
        pattern = re.compile(re.escape(kw) + r'(\S+?)(?=邮箱登录地址|邮箱地址|邮箱网站|$)', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            result['email_password'] = match.group(1).strip()
            break

    # 5. 提取邮箱地址
    for kw in ['邮箱登录地址', '邮箱地址', '邮箱网站']:
        # 邮箱地址是最后一个字段
        pattern = re.compile(re.escape(kw) + r'(\S+)', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            value = match.group(1).strip()
            # 清理邮箱地址（移除协议前缀和末尾斜杠）
            value = value.replace('https://', '').replace('http://', '').strip().strip('/')
            result['email_url'] = value
            break

    # 验证必要字段
    if 'username' in result and 'password' in result:
        # 补充缺失字段
        if 'email' not in result:
            result['email'] = ''
        if 'email_password' not in result:
            result['email_password'] = ''
        if 'email_url' not in result:
            result['email_url'] = ''
        return result

    return None


def parse_file(input_file):
    """
    从文件批量解析账号

    Args:
        input_file: 输入文件路径

    Returns:
        list: 解析成功的账号列表
    """
    accounts = []
    failed_lines = []

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue

                # 尝试解析
                account = parse_chinese_format(line)
                if account:
                    accounts.append(account)
                else:
                    failed_lines.append((line_num, line))

        return accounts, failed_lines

    except FileNotFoundError:
        print(f"❌ 文件不存在: {input_file}")
        return [], []
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return [], []


def format_tab_line(account):
    """格式化为 Tab 分隔行"""
    return "{username}\t{password}\t{email}\t{email_password}\t{email_url}".format(**account)


def save_accounts(accounts, accounts_file):
    """保存账号到文件"""
    if not accounts:
        return False

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
        f.write('\n# 通过格式转换工具添加的账号\n')
        for account in accounts:
            f.write(format_tab_line(account) + '\n')

    return True


def main():
    """主函数"""
    import sys

    # 检查命令行参数
    if len(sys.argv) > 1:
        # 文件批量导入模式
        input_file = sys.argv[1]

        print("\n" + "="*70)
        print("📝 Steam 账号格式转换工具 - 文件批量导入")
        print("="*70)
        print(f"\n📂 正在读取文件: {input_file}")

        project_root = Path(__file__).parent.parent
        accounts_file = project_root / "accounts.txt"

        # 解析文件
        accounts, failed_lines = parse_file(input_file)

        # 显示结果
        if accounts:
            print(f"\n✅ 成功解析 {len(accounts)} 个账号:")
            for i, acc in enumerate(accounts, 1):
                print(f"   {i}. {acc['username']}\t({acc.get('email', 'N/A')})")

        if failed_lines:
            print(f"\n⚠️  {len(failed_lines)} 行无法识别:")
            for line_num, line in failed_lines[:3]:  # 只显示前3个
                print(f"   行{line_num}: {line[:50]}...")
            if len(failed_lines) > 3:
                print(f"   ... 还有 {len(failed_lines) - 3} 行")

        # 保存
        if accounts:
            if save_accounts(accounts, accounts_file):
                print(f"\n✅ 成功保存 {len(accounts)} 个账号到: {accounts_file}")
                print(f"📁 文件位置: {accounts_file.absolute()}")
                print("\n🚀 现在可以运行登录脚本:")
                print("   python src\\login_steam.py")
            else:
                print("\n❌ 保存失败")
        else:
            print("\n⚠️  没有成功解析任何账号")

        print("\n" + "="*70)
        return

    # 交互模式
    print("\n" + "="*70)
    print("📝 Steam 账号格式转换工具 v6 - 中文格式支持")
    print("="*70)
    print("\n💡 使用方法：")
    print("   方式1 (推荐): python src\\chinese_to_tab.py accounts.txt")
    print("   方式2 (交互): 直接运行此命令，手动粘贴")
    print("\n💡 支持的中文格式（关键词顺序）：")
    print("   steam账号xxx密码yyy邮箱账号zzz邮箱密码www邮箱地址bbb")
    print("\n💡 或简写：")
    print("   账号xxx密码yyy邮箱zzz邮箱密码www邮箱地址bbb")
    print("\n💡 示例：")
    print("   steam账号ta3az7wf4vg3密码Av6Ih8Bh8Fd7邮箱账号FCJPT30502@gdh333.cn邮箱密码MLOBV00990邮箱地址x.pubg.fit")
    print("\n💡 输出格式：Tab 分隔（可直接用于 accounts.txt）")
    print("\n💡 命令：")
    print("   输入或粘贴 - 添加账号")
    print("   list/show  - 查看已添加")
    print("   save/done  - 保存到 accounts.txt")
    print("   quit/exit - 退出\n")

    project_root = Path(__file__).parent.parent
    accounts_file = project_root / "accounts.txt"
    accounts = []

    while True:
        print("-"*70)
        try:
            user_input = input("请输入账号信息: ").strip()

            if not user_input:
                continue

            # 退出命令
            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            # 保存命令
            if user_input.lower() in ['save', 'done']:
                if save_accounts(accounts, accounts_file):
                    print(f"\n✅ 成功保存 {len(accounts)} 个账号到: {accounts_file}")
                    print(f"📁 文件位置: {accounts_file.absolute()}")
                    print("\n🚀 现在可以运行登录脚本:")
                    print("   python src\\login_steam.py")
                else:
                    print("\n⚠️  还没有添加任何账号")
                break

            # 查看命令
            if user_input.lower() in ['list', 'show', 'ls']:
                if not accounts:
                    print("\n⚠️  还没有添加任何账号\n")
                else:
                    print(f"\n📋 已添加 {len(accounts)} 个账号:")
                    for i, acc in enumerate(accounts, 1):
                        email = f" ({acc.get('email', 'N/A')})"
                        print(f"   {i}. {acc['username']}\t{email}")
                continue

            # 尝试解析
            account = parse_chinese_format(user_input)

            if account:
                print(f"\n✅ 成功识别账号信息:")
                print(f"   Steam账号: {account['username']}")
                print(f"   Steam密码: {'*' * len(account['password'])}")
                if account.get('email'):
                    print(f"   邮箱账号: {account['email']}")
                if account.get('email_password'):
                    print(f"   邮箱密码: {'*' * len(account['email_password'])}")
                if account.get('email_url'):
                    print(f"   邮箱地址: {account['email_url']}")
                print(f"\n📝 Tab 格式: {format_tab_line(account)}")

                accounts.append(account)
                print(f"\n✅ 已添加到列表，当前共 {len(accounts)} 个")
            else:
                print("\n❌ 无法识别账号信息")
                print("💡 请确保包含以下字段（按顺序）：")
                print("   • steam账号（或账号）")
                print("   • 密码")
                print("   • 邮箱账号（或邮箱）")
                print("   • 邮箱密码")
                print("   • 邮箱地址（或邮箱登录地址/邮箱网站）")
                print("\n💡 输入 'help' 查看完整示例")

        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断")
            break


if __name__ == "__main__":
    main()
