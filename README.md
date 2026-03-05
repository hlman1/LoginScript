# Steam 账号批量登录 + PUBG 启动脚本 - 使用说明

> 自动化登录多个 Steam 账号并启动 PUBG 游戏

---

## 📌 这个脚本做什么？

**自动登录你的多个 Steam 账号，启动 PUBG 游戏，运行 90 秒后关闭，然后切换下一个账号**

**工作流程**：
1. 读取你准备的账号列表
2. 使用 Steam 客户端登录第一个账号
3. 自动启动 PUBG 游戏
4. 游戏运行 90 秒
5. 关闭游戏和 Steam 客户端
6. 自动登录下一个账号并重复
7. 直到全部账号处理完成

**适合场景**：
- 批量账号签到
- 游戏活动任务
- 日常账号维护

---

## 🎯 核心功能

### ✅ 已实现功能
- **Steam 客户端登录** - 使用 Steam 命令行自动登录
- **PUBG 自动启动** - 通过 Steam 协议启动游戏
- **用户许可协议自动处理** - 自动点击"接受"按钮
- **游戏窗口激活** - 自动激活游戏窗口到前台
- **账号自动切换** - 完成后自动关闭并切换下一个
- **进度显示** - 实时显示当前处理进度

### 📋 技术特性
- 多种协议处理方法（Tab+Space、鼠标点击、Alt+Y、回车键）
- 进程检测和验证
- 完善的错误处理
- Windows 控制台编码支持（Emoji 显示）

---

## 🚀 快速开始

### 第一步：检查 Python 版本

打开命令提示符（按 `Win + R`，输入 `cmd`，回车），输入：

```bash
python --version
```

**需要 Python 3.8 或更高版本**

❌ **没有安装？**
1. 访问 https://www.python.org/downloads/
2. 下载 Windows 安装包
3. **安装时务必勾选** "Add Python to PATH"
4. 安装完成后重启电脑

---

### 第二步：安装依赖

**1. 打开项目文件夹**

```bash
# 根据你的实际安装路径修改下面这行
cd D:\vscode\LoginScript

# 例如，如果你的项目在桌面：
# cd C:\Users\你的用户名\Desktop\LoginScript
```

**2. 安装必要的库**
```bash
pip install pyautogui pillow
```

**等待安装完成**（大概 1-2 分钟）
- 看到很多行文字滚动是正常的
- 看到 `Successfully installed...` 就好了

❌ **如果安装失败？**

方法1：升级 pip 后重试
```bash
python -m pip install --upgrade pip
pip install pyautogui pillow
```

方法2：使用国内镜像源（更快）
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyautogui pillow
```

方法3：使用阿里云镜像
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ pyautogui pillow
```

---

### 第三步：配置 Steam 路径

打开 `src\login_steam.py` 文件，找到这几行（约第 45 行）：

```python
STEAM_EXE_PATH = r"F:\steam\Steam.exe"
PUBG_APP_ID = "578080"
```

**如果你的 Steam 安装路径不同，请修改**：
- `STEAM_EXE_PATH` - 你的 Steam.exe 完整路径
- 例如：`r"C:\Program Files (x86)\Steam\Steam.exe"`

🔍 **如何找到你的 Steam 路径**：

**方法1：通过 Steam 图标**
1. 右键桌面上的 Steam 图标
2. 选择"打开文件所在的位置"
3. 在地址栏复制完整路径
4. 路径格式类似：`C:\Program Files (x86)\Steam\Steam.exe`

**方法2：通过任务管理器**
1. 按 `Ctrl + Shift + Esc` 打开任务管理器
2. 找到"Steam"进程
3. 右键 → "打开文件所在的位置"
4. 复制 Steam.exe 的完整路径

**方法3：常见默认路径**
- `C:\Program Files (x86)\Steam\Steam.exe`
- `C:\Program Files\Steam\Steam.exe`
- `D:\Steam\Steam.exe`
- `E:\Steam\Steam.exe`

---

### 第四步：添加你的账号

**最简单的方法：创建文本文件批量导入（推荐）**

**步骤1：创建一个临时文本文件**

在项目文件夹中创建一个 txt 文件（如 `my_accounts.txt`），每行一个账号，使用中文关键词：

```
steam账号ta3az7wf4vg3密码Av6Ih8Bh8Fd7邮箱账号FCJPT30502@gdh333.cn邮箱密码MLOBV00990邮箱地址x.pubg.fit
账号rex78532密码PeF753606邮箱账号n7w77v@sdhgz.cn邮箱密码374777邮箱登录地址https://a.dcmya.com/
```

**💡 支持的关键词**：
- `steam账号` 或 `账号`
- `密码`
- `邮箱账号` 或 `邮箱`
- `邮箱密码`
- `邮箱地址`、`邮箱登录地址` 或 `邮箱网站`

**步骤2：运行转换脚本**

```bash
python src\chinese_to_tab.py my_accounts.txt
```

**步骤3：查看结果**

你会看到类似的输出：

```
======================================================================
📝 Steam 账号格式转换工具 - 文件批量导入
======================================================================

📂 正在读取文件: my_accounts.txt

✅ 成功解析 2 个账号:
   1. ta3az7wf4vg3	(FCJPT30502@gdh333.cn)
   2. rex78532	(n7w77v@sdhgz.cn)

✅ 成功保存 2 个账号到: d:\vscode\LoginScript\accounts.txt
📁 文件位置: d:\vscode\LoginScript\accounts.txt

🚀 现在可以运行登录脚本:
   python src\login_steam.py
```

**完成！** 账号已自动保存到 `accounts.txt`，可以运行登录脚本了。

---

**其他方法**：

**方法2：直接编辑 accounts.txt**

如果你熟悉 Tab 分隔格式，可以直接编辑 `accounts.txt`：

```
ta3az7wf4vg3	Av6Ih8Bh8Fd7	FCJPT30502@gdh333.cn	MLOBV00990	x.pubg.fit
rex78532	PeF753606	n7w77v@sdhgz.cn	374777	a.dcmya.com
```

**字段顺序**（Tab 分隔）：Steam账号 → Steam密码 → 邮箱账号 → 邮箱密码 → 邮箱地址

**方法3：使用问答式配置工具**

```bash
python src\config_accounts.py
```

按照提示一步步输入账号信息即可。

---

## 🎬 运行脚本

💡 **第一次使用建议**：
> 先在 `accounts.txt` 中只添加**一个账号**进行测试，确认一切正常后再添加更多账号。这样更容易发现问题。

**运行命令**：
```bash
python src\login_steam.py
```

**你会看到什么**：

```
============================================================
🎮 Steam 账号批量登录脚本
============================================================
✅ 成功加载 2 个账号

📋 进度: [1/2]
📋 处理账号: ta3az7wf4vg3

==================================================
🎮 开始 PUBG 游戏流程
==================================================
🧹 清理所有进程...
✅ 所有进程已清理

🔐 使用 Steam 客户端登录: ta3az7wf4vg3
📍 执行: steam.exe -login ta3az7wf4vg3 ********
⏳ 等待 Steam 完全准备就绪...
✅ Steam 已就绪 (耗时 3 秒)
✅ Steam 登录完成

🎮 启动 PUBG 游戏...
📍 使用 Steam -applaunch 启动游戏...
⏳ 等待游戏启动...
✅ 检测到游戏已启动

⏳ 游戏运行中 (90 秒)...
   ⏱️  剩余时间: 90 秒
   ⏱️  剩余时间: 60 秒
   ⏱️  剩余时间: 30 秒
   ✅ 游戏运行时间结束

🎮 关闭 PUBG 游戏...
✅ PUBG 游戏已关闭
🚪 关闭 Steam 客户端...
✅ Steam 已完全关闭

✅ PUBG 流程完成

⏳ 等待 2 秒后处理下一个账号...
```

**整个过程完全自动，你只需要看着！**

---

## ⚙️ 自定义配置

### 修改游戏运行时间

打开 `src\login_steam.py`，找到（约第 851 行）：

```python
game_time = 90  # 90秒
```

修改为你想要的秒数，例如：
```python
game_time = 120  # 改为 120 秒（2分钟）
```

### 修改账号切换间隔

找到（约第 937 行）：

```python
interval = 2  # 账号之间间隔（秒）
```

可以根据需要调整。

---

## ⚠️ 常见问题

### 问题1：提示"找不到 Steam"

**错误信息**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'F:\\steam\\Steam.exe'
```

**解决方法**：
1. 找到你的 Steam 安装位置
2. 右键 Steam 桌面图标 → 打开文件所在位置
3. 复制完整路径
4. 修改 `src\login_steam.py` 中的 `STEAM_EXE_PATH`

### 问题2：游戏没有自动启动

**可能原因**：
- 账号没有购买 PUBG 游戏
- 游戏文件损坏
- Steam 库位置不正确

**解决方法**：
1. 手动登录 Steam 检查游戏库
2. 验证游戏文件完整性

### 问题3：用户许可协议没自动处理

**说明**：
脚本会尝试多种方法处理许可协议：
- Tab + Space
- 鼠标点击左侧（接受按钮）
- Alt+Y 快捷键
- 回车键

**如果仍然失败**：
1. 检查是否有弹窗被其他窗口遮挡
2. 手动点击"接受"按钮
3. 脚本会继续尝试，最多 12 次

### 问题4：Steam 客户端没有完全关闭

**如果遇到账号混淆**：
- 脚本会自动检测并清理残留的 Steam 进程
- 如果仍有问题，手动打开任务管理器结束所有 steam.exe 进程

### 问题5：想停止脚本

按 `Ctrl + C`（同时按 Ctrl 和 C 键）

---

## 💡 实用技巧

### 暂时跳过某个账号

在 `accounts.txt` 中，不想处理的账号行前面加 `#`

例如：
```
# ta3az7wf4vg3	Av6Ih8Bh8Fd7	FCJPT30502@gdh333.cn	MLOBV00990	x.pubg.fit
rex78532	PeF753606	n7w77v@sdhgz.cn	374777	a.dcmya.com
```

### 查看当前进度

命令提示符会显示：
```
📋 进度: [2/5]
```
表示正在处理第 2 个账号，总共 5 个账号

### 调试模式

如果遇到问题，可以查看脚本执行过程：
- 每一步都有详细的日志输出
- 会显示当前的屏幕分辨率
- 会显示尝试的点击位置

---

## 📁 项目结构

```
LoginScript/
├── src/
│   ├── login_steam.py           # 主程序（Steam客户端+PUBG启动）
│   ├── test_login_one.py        # 单账号测试脚本
│   ├── config_accounts.py       # 问答式配置工具
│   ├── quick_add.py             # Tab格式快速添加工具
│   └── chinese_to_tab.py        # 中文格式转换工具
├── accounts.txt                 # 你的账号密码文件
├── requirements.txt             # Python 依赖列表
├── README.md                    # 本说明文件
├── WORKFLOW.md                  # 工作流记录
└── CLAUDE.md                    # 开发对话记录
```

---

## 🔒 安全提醒

⚠️ **重要**：

1. **保管好账号文件**
   - `accounts.txt` 包含你的账号密码
   - 不要分享给任何人
   - 不要上传到网上或 GitHub

2. **使用强密码**
   - 建议使用密码管理器
   - 开启 Steam Guard 双因素认证

3. **注意账号安全**
   - 不要在公共场所使用
   - 使用完成后删除 `accounts.txt`

4. **遵守 Steam 服务条款**
   - 不要用于违规用途
   - 注意登录频率，避免触发风控

---

## ❓ 常见疑问

**Q: 脚本会偷我的账号吗？**

A: 不会。源代码完全公开，你可以查看每一行代码。所有操作都在你本地电脑完成。

**Q: 为什么不用浏览器登录了？**

A: 使用 Steam 客户端更稳定，可以直接启动游戏，不需要打开浏览器。

**Q: 支持其他游戏吗？**

A: 当前只支持 PUBG。修改 `PUBG_APP_ID` 可以支持其他 Steam 游戏。

**Q: 游戏运行时间可以调整吗？**

A: 可以。在 `src\login_steam.py` 中修改 `game_time` 参数。

**Q: 遇到问题怎么办？**

A:
1. 查看本说明的"常见问题"部分
2. 查看 `WORKFLOW.md` 了解详细开发过程
3. 检查错误日志输出

---

## 📊 系统要求

| 要求 | 说明 |
|------|------|
| 操作系统 | Windows 10/11 |
| Python | 3.8 或更高版本 |
| Steam | 已安装并配置好 |
| PUBG | 账号已购买游戏 |
| 网络 | 稳定的互联网连接 |

---

## 📝 更新日志

### v2.0 (2026-02-26)
- ✅ 改用 Steam 客户端登录（替代浏览器）
- ✅ 新增 PUBG 游戏自动启动功能
- ✅ 新增用户许可协议自动处理
- ✅ 新增游戏窗口自动激活
- ✅ 优化 Steam 进程清理机制
- ✅ 修复账号切换时的进程残留问题

### v1.0 (2026-02-13)
- ✅ 初始版本（浏览器登录方式）

---

*最后更新：2026-02-26*
