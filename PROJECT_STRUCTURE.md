# Steam 批量登录工具 - 项目结构

## 📦 必需文件（不能删除）

### 启动文件
- **start.bat** / **启动工具.bat** - 双击启动 GUI（二选一）
- **src/steam_login_gui.py** - GUI 主程序
- **src/login_steam.py** - 核心登录脚本
- **src/chinese_to_tab.py** - 账号格式转换工具

### 数据文件
- **accounts.txt** - 账号信息存储

### 依赖配置
- **requirements.txt** - Python 依赖列表

---

## 📚 文档文件（推荐保留）

- **README.md** - 主使用说明（GUI 方式优先）
- **GUI使用指南.md** - GUI 详细使用指南
- **WORKFLOW.md** - 开发工作流记录
- **CLAUDE.md** - 对话历史记录

---

## 🛠️ 可选工具（根据需要保留）

以下工具已集成到 GUI 中，可选择性保留：

- **src/config_accounts.py** - 问答式配置工具（GUI 已包含）
- **src/quick_add.py** - 快速添加工具（GUI 已包含）
- **src/test_login_one.py** - 单账号测试脚本（调试用）

---

## 📁 分发版文件清单

如果要打包分发给他人，只需包含以下文件：

### 最小分发包
```
LoginScript/
├── start.bat                    # 启动器
├── requirements.txt              # 依赖列表
├── README.md                    # 使用说明
├── src/
│   ├── steam_login_gui.py       # GUI 程序
│   ├── login_steam.py           # 登录脚本
│   └── chinese_to_tab.py        # 转换工具
└── accounts.txt                 # 账号文件（可为空）
```

### 完整分发包（推荐）
```
LoginScript/
├── start.bat                    # 启动器
├── requirements.txt              # 依赖列表
├── README.md                    # 使用说明
├── GUI使用指南.md               # 详细指南
├── src/
│   ├── steam_login_gui.py       # GUI 程序
│   ├── login_steam.py           # 登录脚本
│   ├── chinese_to_tab.py        # 转换工具
│   ├── config_accounts.py       # 配置工具（可选）
│   └── quick_add.py             # 快速添加（可选）
└── accounts.txt                 # 账号文件
```

---

## 🚀 使用方式

### 方式1：GUI 界面（推荐）
1. 双击 `start.bat` 或 `启动工具.bat`
2. 按照界面提示操作

### 方式2：命令行
```bash
python src/steam_login_gui.py
```

---

## ⚠️ 文件说明

| 文件 | 必需 | 说明 |
|------|------|------|
| start.bat | ✅ | 启动器（纯英文） |
| 启动工具.bat | ✅ | 启动器（纯英文） |
| src/steam_login_gui.py | ✅ | GUI 主程序 |
| src/login_steam.py | ✅ | 登录核心脚本 |
| src/chinese_to_tab.py | ✅ | 格式转换 |
| accounts.txt | ✅ | 账号数据 |
| requirements.txt | ✅ | 依赖列表 |
| README.md | ✓ | 使用说明 |
| GUI使用指南.md | ✓ | 详细指南 |
| src/config_accounts.py | ○ | 配置工具 |
| src/quick_add.py | ○ | 快速添加 |
| src/test_login_one.py | ○ | 测试脚本 |
| WORKFLOW.md | ○ | 开发记录 |
| CLAUDE.md | ○ | 对话记录 |

**图例**：
- ✅ 必需
- ✓ 推荐保留
- ○ 可选

---

## 💾 从 GitHub 下载使用

1. 下载并解压压缩包
2. 双击 `start.bat`
3. 如果提示缺少 Python，请先安装 Python 3.8+
4. 如果提示缺少依赖，GUI 会提示一键安装

---

## 🔧 问题排查

### 问题1：bat 文件无法运行
- **原因**：文件编码问题
- **解决**：使用 `start.bat`（纯英文版）

### 问题2：提示找不到文件
- **原因**：文件结构不完整
- **解决**：确认包含 `src/` 文件夹和所有必需文件

### 问题3：Python 依赖错误
- **原因**：未安装 pyautogui 或 pillow
- **解决**：
  ```bash
  pip install pyautogui pillow
  ```

---

*最后更新：2026-03-06*
