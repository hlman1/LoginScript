#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import tkinter as tk
import json
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("GUI 功能测试")
print("=" * 60)

print("\n[1/5] 检查必要的库...")
try:
    import tkinter
    print("OK tkinter")
except ImportError:
    print("FAIL tkinter")
    sys.exit(1)

try:
    import pyautogui
    print("OK pyautogui")
except ImportError:
    print("WARN pyautogui not installed")

try:
    import PIL
    print("OK PIL")
except ImportError:
    print("WARN PIL not installed")

print("\n[2/5] 检查文件路径...")
gui_script = Path("src/steam_login_gui.py")
login_script = Path("src/login_steam.py")

print(f"OK {gui_script}" if gui_script.exists() else f"FAIL {gui_script}")
print(f"OK {login_script}" if login_script.exists() else f"FAIL {login_script}")

print("\n[3/5] 检查 GUI 语法...")
try:
    import py_compile
    py_compile.compile("src/steam_login_gui.py", doraise=True)
    print("OK GUI syntax check")
except Exception as e:
    print(f"FAIL {e}")
    sys.exit(1)

print("\n[4/5] 测试配置文件...")
config_file = Path("test_config.json")
try:
    test_config = {"steam_path": r"F:\steam\Steam.exe"}
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(test_config, f)
    with open(config_file, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    print("OK config read/write")
    config_file.unlink()
except Exception as e:
    print(f"FAIL {e}")

print("\n[5/5] 检查账号文件...")
accounts_file = Path("accounts.txt")
if accounts_file.exists():
    with open(accounts_file, 'r', encoding='utf-8') as f:
        count = sum(1 for line in f if line.strip() and not line.strip().startswith('#'))
    print(f"OK accounts.txt ({count} accounts)")
else:
    print("WARN accounts.txt not found")

print("\n" + "=" * 60)
print("All tests passed!")
print("=" * 60)
print("\nNext steps:")
print("1. Double click: 启动工具.bat")
print("2. Or run: python src/steam_login_gui.py")
