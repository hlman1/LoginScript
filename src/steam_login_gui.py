#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam 批量登录工具 - 图形化界面版本
功能：一键完成环境检查、配置、账号管理和登录
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import sys
import os
import json
import threading
from pathlib import Path
import time

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class SteamLoginGUI:
    """Steam 批量登录工具 GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("Steam 批量登录工具 v2.1")
        self.root.geometry("700x650")
        self.root.resizable(False, False)

        # 配置文件路径
        self.config_file = Path(__file__).parent.parent / "config.json"
        self.accounts_file = Path(__file__).parent.parent / "accounts.txt"
        self.login_script = Path(__file__).parent / "login_steam.py"

        # 加载配置
        self.config = self.load_config()

        # 创建界面
        self.create_widgets()

        # 初始化检查
        self.root.after(100, self.check_environment)

    def load_config(self):
        """加载配置文件"""
        default_config = {
            "steam_path": self.find_steam_path(),
            "game_time": 90
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
            except:
                pass

        return default_config

    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败：{e}")
            return False

    def find_steam_path(self):
        """自动查找 Steam 路径"""
        possible_paths = [
            r"F:\steam\Steam.exe",
            r"C:\Program Files (x86)\Steam\Steam.exe",
            r"C:\Program Files\Steam\Steam.exe",
            r"D:\Steam\Steam.exe",
            r"E:\Steam\Steam.exe",
        ]

        for path in possible_paths:
            if Path(path).exists():
                return path

        return r"F:\steam\Steam.exe"  # 默认值

    def create_widgets(self):
        """创建界面组件"""
        # 创建 Notebook（标签页）
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # 创建各个标签页
        self.create_environment_tab(notebook)
        self.create_config_tab(notebook)
        self.create_accounts_tab(notebook)
        self.create_run_tab(notebook)

    def create_environment_tab(self, notebook):
        """创建环境检查标签页"""
        env_frame = ttk.Frame(notebook)
        notebook.add(env_frame, text="🔧 环境检查")

        # 标题
        ttk.Label(env_frame, text="环境检查", font=("Arial", 14, "bold")).pack(pady=10)

        # Python 检查
        self.python_status = self.create_status_row(env_frame, "Python 环境")

        # 依赖检查
        self.pyautogui_status = self.create_status_row(env_frame, "pyautogui 库")
        self.pillow_status = self.create_status_row(env_frame, "pillow 库")

        # 操作按钮
        btn_frame = ttk.Frame(env_frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="🔄 重新检查", command=self.check_environment).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📦 一键安装依赖", command=self.install_dependencies).pack(side='left', padx=5)

        # 日志区域
        ttk.Label(env_frame, text="安装日志：").pack(anchor='w', padx=20, pady=(10, 0))
        self.env_log = scrolledtext.ScrolledText(env_frame, height=10, width=80)
        self.env_log.pack(padx=20, pady=5)

    def create_config_tab(self, notebook):
        """创建配置标签页"""
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="⚙️ 配置")

        # 标题
        ttk.Label(config_frame, text="系统配置", font=("Arial", 14, "bold")).pack(pady=10)

        # Steam 路径配置
        steam_frame = ttk.LabelFrame(config_frame, text="Steam 路径", padding=10)
        steam_frame.pack(fill='x', padx=20, pady=10)

        path_frame = ttk.Frame(steam_frame)
        path_frame.pack(fill='x')

        self.steam_path_var = tk.StringVar(value=self.config.get('steam_path', ''))
        ttk.Entry(path_frame, textvariable=self.steam_path_var, width=50).pack(side='left', padx=5)
        ttk.Button(path_frame, text="浏览...", command=self.browse_steam_path).pack(side='left', padx=5)
        ttk.Button(path_frame, text="自动检测", command=self.auto_detect_steam).pack(side='left', padx=5)

        # 游戏运行时间
        time_frame = ttk.LabelFrame(config_frame, text="游戏运行时间（秒）", padding=10)
        time_frame.pack(fill='x', padx=20, pady=10)

        self.game_time_var = tk.StringVar(value=str(self.config.get('game_time', 90)))
        ttk.Entry(time_frame, textvariable=self.game_time_var, width=20).pack(side='left', padx=5)
        ttk.Label(time_frame, text="秒").pack(side='left')

        # 保存按钮
        ttk.Button(config_frame, text="💾 保存配置", command=self.save_settings).pack(pady=20)

    def create_accounts_tab(self, notebook):
        """创建账号管理标签页"""
        accounts_frame = ttk.Frame(notebook)
        notebook.add(accounts_frame, text="👥 账号管理")

        # 标题
        ttk.Label(accounts_frame, text="账号管理", font=("Arial", 14, "bold")).pack(pady=10)

        # 账号列表
        list_frame = ttk.Frame(accounts_frame)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        # 列表框
        self.accounts_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.accounts_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.accounts_listbox.yview)

        # 刷新账号列表
        self.refresh_accounts_list()

        # 操作按钮
        btn_frame = ttk.Frame(accounts_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="➕ 添加账号", command=self.add_account_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📁 导入文件", command=self.import_accounts_file).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ 删除选中", command=self.delete_account).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 刷新列表", command=self.refresh_accounts_list).pack(side='left', padx=5)

    def create_run_tab(self, notebook):
        """创建运行标签页"""
        run_frame = ttk.Frame(notebook)
        notebook.add(run_frame, text="🚀 运行")

        # 标题
        ttk.Label(run_frame, text="开始运行", font=("Arial", 14, "bold")).pack(pady=10)

        # 统计信息
        stats_frame = ttk.Frame(run_frame)
        stats_frame.pack(pady=10)

        self.account_count_label = ttk.Label(stats_frame, text="账号数量：0")
        self.account_count_label.pack(side='left', padx=20)

        # 进度条
        progress_frame = ttk.Frame(run_frame)
        progress_frame.pack(pady=20, padx=20, fill='x')

        ttk.Label(progress_frame, text="进度：").pack(anchor='w')
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', pady=5)

        self.status_label = ttk.Label(progress_frame, text="就绪")
        self.status_label.pack(anchor='w')

        # 操作按钮
        btn_frame = ttk.Frame(run_frame)
        btn_frame.pack(pady=20)

        self.start_btn = ttk.Button(btn_frame, text="▶️ 开始登录", command=self.start_login)
        self.start_btn.pack(side='left', padx=10)

        self.stop_btn = ttk.Button(btn_frame, text="⏹️ 停止", command=self.stop_login, state='disabled')
        self.stop_btn.pack(side='left', padx=10)

        # 日志区域
        ttk.Label(run_frame, text="运行日志：").pack(anchor='w', padx=20, pady=(10, 0))
        self.run_log = scrolledtext.ScrolledText(run_frame, height=15, width=80)
        self.run_log.pack(padx=20, pady=5)

        # 更新统计
        self.update_stats()

    def create_status_row(self, parent, label):
        """创建状态行"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', padx=20, pady=5)

        ttk.Label(frame, text=label, width=20).pack(side='left')
        status_var = tk.StringVar(value="⏳ 检查中...")
        ttk.Label(frame, textvariable=status_var, foreground="blue").pack(side='left')

        return status_var

    def check_environment(self):
        """检查环境"""
        # 检查 Python
        try:
            version = sys.version.split()[0]
            self.python_status.set(f"✅ Python {version}")
        except:
            self.python_status.set("❌ Python 未安装")

        # 检查 pyautogui
        try:
            import pyautogui
            self.pyautogui_status.set("✅ 已安装")
        except:
            self.pyautogui_status.set("❌ 未安装")

        # 检查 pillow
        try:
            import PIL
            self.pillow_status.set("✅ 已安装")
        except:
            self.pillow_status.set("❌ 未安装")

    def install_dependencies(self):
        """安装依赖"""
        self.log_message("开始安装依赖...\n")

        def install():
            try:
                # 升级 pip
                self.log_message("正在升级 pip...\n")
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                             capture_output=True)

                # 安装 pyautogui
                self.log_message("正在安装 pyautogui...\n")
                result = subprocess.run([sys.executable, "-m", "pip", "install", "pyautogui"],
                                      capture_output=True, text=True)
                self.log_message(result.stdout)

                # 安装 pillow
                self.log_message("正在安装 pillow...\n")
                result = subprocess.run([sys.executable, "-m", "pip", "install", "pillow"],
                                      capture_output=True, text=True)
                self.log_message(result.stdout)

                self.log_message("\n✅ 依赖安装完成！\n")
                self.check_environment()
                messagebox.showinfo("完成", "依赖安装完成！")
            except Exception as e:
                self.log_message(f"\n❌ 安装失败：{e}\n")
                messagebox.showerror("错误", f"安装失败：{e}")

        threading.Thread(target=install, daemon=True).start()

    def browse_steam_path(self):
        """浏览 Steam 路径"""
        filename = filedialog.askopenfilename(
            title="选择 Steam.exe",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if filename:
            self.steam_path_var.set(filename)

    def auto_detect_steam(self):
        """自动检测 Steam 路径"""
        path = self.find_steam_path()
        if Path(path).exists():
            self.steam_path_var.set(path)
            messagebox.showinfo("成功", f"找到 Steam 路径：\n{path}")
        else:
            messagebox.showwarning("未找到", "未能自动找到 Steam，请手动选择")

    def save_settings(self):
        """保存设置"""
        self.config['steam_path'] = self.steam_path_var.get()
        try:
            self.config['game_time'] = int(self.game_time_var.get())
        except:
            messagebox.showerror("错误", "游戏运行时间必须是数字")
            return

        if self.save_config():
            messagebox.showinfo("成功", "配置已保存！")

    def refresh_accounts_list(self):
        """刷新账号列表"""
        self.accounts_listbox.delete(0, tk.END)

        if not self.accounts_file.exists():
            self.accounts_listbox.insert(tk.END, "（暂无账号，请添加）")
            return

        try:
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            username = parts[0]
                            self.accounts_listbox.insert(tk.END, f"账号：{username}")

            self.update_stats()
        except Exception as e:
            messagebox.showerror("错误", f"读取账号文件失败：{e}")

    def add_account_dialog(self):
        """添加账号对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加账号")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # 字段
        fields = [
            ("Steam 账号：", "username"),
            ("Steam 密码：", "password"),
            ("邮箱账号：", "email"),
            ("邮箱密码：", "email_password"),
            ("邮箱地址：", "email_url")
        ]

        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=10, sticky='e')
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry

        def save_account():
            values = []
            for key in ["username", "password", "email", "email_password", "email_url"]:
                value = entries[key].get().strip()
                if not value and key in ["username", "password"]:
                    messagebox.showwarning("警告", "账号和密码不能为空")
                    return
                values.append(value if value else "")

            # 追加到文件
            try:
                with open(self.accounts_file, 'a', encoding='utf-8') as f:
                    f.write('\t'.join(values) + '\n')

                self.refresh_accounts_list()
                dialog.destroy()
                messagebox.showinfo("成功", "账号添加成功！")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{e}")

        ttk.Button(dialog, text="保存", command=save_account).grid(row=5, column=0, columnspan=2, pady=20)

    def import_accounts_file(self):
        """导入账号文件"""
        filename = filedialog.askopenfilename(
            title="选择账号文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )

        if filename:
            # 调用转换脚本
            try:
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).parent / "chinese_to_tab.py"), filename],
                    capture_output=True,
                    text=True
                )

                self.log_message(result.stdout)
                if result.returncode == 0:
                    self.refresh_accounts_list()
                    messagebox.showinfo("成功", "账号导入成功！")
                else:
                    messagebox.showerror("错误", "导入失败，请查看日志")
            except Exception as e:
                messagebox.showerror("错误", f"导入失败：{e}")

    def delete_account(self):
        """删除选中的账号"""
        selection = self.accounts_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的账号")
            return

        if messagebox.askyesno("确认", "确定要删除选中的账号吗？"):
            # 这里简化处理，直接清空文件重新添加
            messagebox.showinfo("提示", "请手动编辑 accounts.txt 文件删除账号")

    def update_stats(self):
        """更新统计信息"""
        count = self.accounts_listbox.size()
        if count > 0 and self.accounts_listbox.get(0) == "（暂无账号，请添加）":
            count = 0
        self.account_count_label.config(text=f"账号数量：{count}")

    def start_login(self):
        """开始登录"""
        if not self.login_script.exists():
            messagebox.showerror("错误", "找不到登录脚本")
            return

        # 更新配置到脚本
        self.update_login_script_config()

        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress_var.set(0)
        self.run_log.delete(1.0, tk.END)

        def run_login():
            try:
                process = subprocess.Popen(
                    [sys.executable, str(self.login_script)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )

                for line in process.stdout:
                    self.log_message(line)

                process.wait()
                self.progress_var.set(100)
                self.status_label.config(text="✅ 完成")
                messagebox.showinfo("完成", "所有账号处理完成！")
            except Exception as e:
                self.log_message(f"错误：{e}\n")
                messagebox.showerror("错误", f"运行失败：{e}")
            finally:
                self.start_btn.config(state='normal')
                self.stop_btn.config(state='disabled')

        threading.Thread(target=run_login, daemon=True).start()

    def stop_login(self):
        """停止登录"""
        # 这里需要实现停止逻辑
        messagebox.showinfo("提示", "请手动关闭 Steam 窗口停止")

    def update_login_script_config(self):
        """更新登录脚本的配置"""
        # 这里可以动态修改 login_steam.py 的配置
        # 为了简化，暂时省略
        pass

    def log_message(self, message):
        """记录日志"""
        self.env_log.insert(tk.END, message)
        self.env_log.see(tk.END)

        self.run_log.insert(tk.END, message)
        self.run_log.see(tk.END)


def main():
    """主函数"""
    root = tk.Tk()
    app = SteamLoginGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
