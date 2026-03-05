#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件完整性检查工具
检查运行GUI所需的所有文件是否存在
"""

import sys
import os
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("GUI 运行所需文件检查工具")
print("=" * 60)
print()

# 获取当前目录
current_dir = Path.cwd()
print(f"当前目录: {current_dir}")
print()

# 必需文件列表
required_files = {
    "启动工具.bat": "启动器",
    "src/steam_login_gui.py": "GUI 主程序",
    "src/login_steam.py": "登录核心脚本",
    "src/chinese_to_tab.py": "账号格式转换",
}

# 可选文件
optional_files = {
    "accounts.txt": "账号文件（首次运行可自动创建）",
    "config.json": "配置文件（自动生成）",
    "GUI使用指南.md": "使用说明",
    "README.md": "项目说明",
}

print("【必需文件检查】")
print("-" * 60)
all_ok = True
for file_path, description in required_files.items():
    full_path = current_dir / file_path
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"✓ {file_path}")
        print(f"  {description} ({size:,} 字节)")
    else:
        print(f"✗ {file_path}")
        print(f"  {description} - 【缺失】")
        all_ok = False

print()
print("【可选文件检查】")
print("-" * 60)
for file_path, description in optional_files.items():
    full_path = current_dir / file_path
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"✓ {file_path}")
        print(f"  {description} ({size:,} 字节)")
    else:
        print(f"○ {file_path}")
        print(f"  {description} - （不存在，首次运行正常）")

print()
print("=" * 60)
if all_ok:
    print("✓ 所有必需文件都存在，可以运行 GUI 工具！")
    print()
    print("下一步：")
    print("  双击 '启动工具.bat' 启动图形界面")
else:
    print("✗ 缺少必需文件，请补充完整！")
    print()
    print("解决方法：")
    print("  1. 确保复制了完整的 src/ 文件夹")
    print("  2. 确保启动工具.bat 在项目根目录")
    print("  3. 重新从原项目复制所有文件")

print("=" * 60)
print()

# 检查 Python 环境
print("【Python 环境检查】")
print("-" * 60)
try:
    import tkinter
    print("✓ tkinter (GUI 框架)")
except ImportError:
    print("✗ tkinter - 未安装")
    all_ok = False

try:
    import pyautogui
    print("✓ pyautogui (键盘鼠标控制)")
except ImportError:
    print("○ pyautogui - 未安装（可以后续在 GUI 中安装）")

try:
    import PIL
    print("✓ PIL/pillow (图像处理)")
except ImportError:
    print("○ PIL/pillow - 未安装（可以后续在 GUI 中安装）")

print()
print("=" * 60)
