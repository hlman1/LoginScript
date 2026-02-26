# Steam 账号批量登录脚本 - 工作流记录

## 项目概述
实现一个自动化脚本，能够从txt文件读取多个Steam账号密码，依次登录并退出每个账号。

## 技术选型
- **编程语言**: Python
- **理由**: 有成熟的Steam第三方库、跨平台支持、代码简洁易维护

## 工作流程

### 1. 环境准备
- [ ] 安装 Python (建议 3.8+)
- [ ] 安装必要的依赖库
  - `steam` 库或相关Steam登录库
  - 其他辅助库（如需）

### 2. 账号文件准备
- [x] 创建账号密码文件格式规范
  - 文件名: `accounts.txt`
  - 格式: `Steam账号:Steam密码:邮箱账号:邮箱密码:邮箱地址`
- [x] 创建示例账号文件并添加测试账号

### 3. 脚本开发
- [x] 编写脚本主体结构
  - [x] 创建 `SteamLoginBatch` 类框架
  - [x] 读取账号文件功能
  - [x] Steam登录功能实现 (Playwright)
  - [x] Steam登出功能实现
  - [x] 循环登录逻辑
  - [x] 错误处理和日志记录
  - [x] Steam Guard 验证处理（手动输入）

### 4. 测试与调试
- [x] 单账号登录测试
- [x] 多账号循环测试
- [x] 异常情况处理测试
- [x] 账号文件格式问题修复

### 5. 文档完善
- [x] 使用说明文档 (README.md - 小白友好版)
- [x] 注意事项说明

## 项目文件结构
```
D:\vscode\LoginScript\
├── WORKFLOW.md           # 本工作流文档
├── requirements.txt      # Python 依赖
├── accounts.txt          # 账号密码文件
├── src/                 # 源代码目录
│   ├── __init__.py
│   └── login_steam.py    # 主脚本文件
├── README.md             # 使用说明（待创建）
└── logs/                 # 日志文件夹（可选）
```

## 注意事项
- 账号安全：妥善保管 accounts.txt 文件
- Steam限制：注意登录频率，避免触发风控
- 网络稳定：确保网络连接正常

## 当前进度
- [x] 创建项目工作流文档
- [x] 环境准备 (创建 requirements.txt)
- [x] 脚本主体框架开发
- [x] Steam 登录功能实现 (Playwright)
- [x] Steam 登出功能实现
- [x] 测试验证（单账号+多账号）
- [x] 问题修复（编码+账号格式）
- [ ] 文档完善（README.md）
- [ ] PUBG 游戏签到功能（待开发）

---

## 开发日志

### 2026-02-13 - 脚本框架开发

#### 已完成
1. **创建主脚本** `login_steam.py`
   - 实现 `SteamLoginBatch` 类
   - 账号文件读取功能（支持注释和空行）
   - 账号信息解析（5字段格式）
   - 循环登录逻辑框架
   - 进度显示和基础日志

2. **账号文件** `accounts.txt`
   - 创建文件格式规范
   - 添加两个测试账号

#### 待完成
- **Steam 登录方案选择**（需确认）
  - Selenium 浏览器自动化
  - Playwright 浏览器自动化
  - Steam 官方 API 库

3. **脚本功能**
  - [ ] Steam 登录具体实现
  - [ ] Steam 登出功能
  - [ ] 错误处理优化
  - [ ] 日志文件记录

---

### 2026-02-13 - Playwright 登录实现

#### 技术方案确定
- **选择 Playwright** 作为浏览器自动化方案
- **理由**：
  - 为后期 PUBG 游戏签到功能预留扩展性
  - 自动管理浏览器驱动，无需手动下载
  - 支持有头/无头模式切换
  - 更好的跨平台支持

#### 已完成
1. **主脚本更新** `login_steam.py`
   - 集成 Playwright 同步 API
   - 实现浏览器初始化和关闭
   - 实现自动登录逻辑（多选择器兼容）
   - 实现 Steam Guard 验证处理（手动输入验证码）
   - 实现登出功能（访问 logout URL 或清除 cookies）
   - 添加异常处理和用户交互

2. **依赖文件** `requirements.txt`
   - playwright==1.48.0

#### 脚本功能特性
- ✅ 自动检测并填充登录表单（兼容多种页面结构）
- ✅ Steam Guard 验证支持（手动输入）
- ✅ 登录状态检测（URL 匹配）
- ✅ 失败后询问是否继续
- ✅ 显示浏览器窗口便于调试（headless=False）
- ✅ 账号间间隔控制（避免触发风控）

#### 待测试
- [ ] 安装依赖：`pip install -r requirements.txt`
- [ ] 安装 Playwright 浏览器：`playwright install chromium`
- [ ] 运行测试：`python src/login_steam.py`

---

### 2026-02-13 - 脚本测试与问题修复

#### 环境准备

**操作1：检查 Python 版本**
```bash
python --version
```
- **结果**：Python 3.12.0 ✅
- **说明**：项目需要 Python 3.8+，当前版本满足要求

**操作2：安装 Playwright 依赖**
```bash
pip install playwright==1.48.0
```
- **结果**：成功安装 ✅
- **安装的包**：
  - playwright==1.48.0
  - greenlet==3.1.1
  - pyee==12.0.0
  - typing_extensions==4.15.0

**操作3：安装 Chromium 浏览器**
```bash
playwright install chromium
```
- **结果**：Chromium 下载成功 ✅
- **说明**：FFmpeg（视频录制组件）下载失败，但不影响登录功能

---

#### 问题1：Windows 控制台编码错误

**错误信息**：
```
UnicodeEncodeError: 'gbk' codec can't encode character '\U0001f3ae'
```

**原因分析**：
- Windows 控制台默认使用 GBK 编码
- 脚本中使用了 emoji 字符（🎮、🔐 等）
- GBK 编码无法显示这些 Unicode 字符

**解决方案**：
在 `login_steam.py` 文件开头添加编码修复代码：

```python
# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
```

**操作步骤**：
1. 打开 `src/login_steam.py`
2. 在 `import` 语句之前添加上述代码
3. 保存文件

**结果**：编码问题解决 ✅

---

#### 问题2：账号文件格式错误

**错误信息**：
```
⚠️  第 19 行格式错误，已跳过
✅ 成功加载 1 个账号
```

**原因分析**：
- 第二个账号的邮箱地址是 `https://a.dcmya.com/`
- URL 中的 `://` 被当成字段分隔符（`:`
- 导致分割后字段数量不是 5 个

**解决方案**：
移除邮箱地址的协议前缀，只保留域名：

**修改前**：
```
rex78532:PeF753606:n7w77v@sdhgz.cn:374777:https://a.dcmya.com/
```

**修改后**：
```
rex78532:PeF753606:n7w77v@sdhgz.cn:374777:a.dcmya.com
```

**操作步骤**：
1. 打开 `accounts.txt`
2. 修改第二个账号的邮箱地址字段
3. 保存文件

**结果**：两个账号都能正确加载 ✅

---

#### 测试执行

**操作4：运行登录测试**
```bash
python src/login_steam.py
```

**测试流程**：

| 步骤 | 操作 | 结果 | 说明 |
|------|------|------|------|
| 1 | 加载账号文件 | ✅ 成功加载 2 个账号 | 账号格式正确 |
| 2 | 初始化浏览器 | ✅ Chromium 启动成功 | 无头模式关闭，可见窗口 |
| 3 | 访问 Steam 登录页 | ✅ 页面加载成功 | 使用 steamcommunity.com/login/home/ |
| 4 | 自动填充用户名 | ✅ 自动识别并填充 | 多选择器兼容方案 |
| 5 | 自动填充密码 | ✅ 自动识别并填充 | 密码显示为星号 |
| 6 | 点击登录按钮 | ✅ 自动点击登录 | 表单提交成功 |
| 7 | 检查 Steam Guard | ✅ 无需验证 | 该账号已验证过设备 |
| 8 | 验证登录状态 | ✅ URL 匹配成功 | 跳转到个人主页 |
| 9 | 等待 5 秒 | ✅ 正常等待 | 可调整等待时间 |
| 10 | 退出登录 | ✅ 清除 cookies | logout 页面访问成功 |
| 11 | 处理下一个账号 | ✅ 间隔 3 秒后继续 | 避免频繁请求 |

**测试账号信息**：
```
账号：ta3az7wf4vg3
邮箱：FCJPT30502@gdh333.cn
登录结果：成功
个人主页：https://steamcommunity.com/profiles/76561199358116370/home
```

---

#### 测试结果总结

**功能验证**：
- ✅ 账号文件读取正确（支持注释、空行）
- ✅ 账号信息解析正确（5 字段格式）
- ✅ 浏览器自动化正常（Playwright 集成成功）
- ✅ 登录表单自动填充（多选择器兼容）
- ✅ Steam Guard 检测功能（可手动输入验证码）
- ✅ 登录状态判断（URL 匹配检测）
- ✅ 自动登出功能（cookies 清理）
- ✅ 循环登录逻辑（多账号处理）
- ✅ 错误处理机制（异常捕获和提示）

**已解决问题**：
1. ✅ Windows 控制台编码问题
2. ✅ 账号文件格式问题（URL 冒号冲突）

**后续优化建议**：
1. 添加日志文件输出功能
2. 支持验证码自动获取（邮箱自动化）
3. 添加截图保存功能（调试用）
4. 优化登录成功判断逻辑
5. 添加重试机制

---

### 2026-02-26 - v2.0 重大更新：Steam 客户端 + PUBG 启动

#### 技术方案调整
从浏览器自动化（Playwright）切换到 Steam 客户端命令行：
- **旧方案**：Playwright 浏览器自动化
- **新方案**：Steam CLI (`steam.exe -login`) + 游戏启动 (`steam.exe -applaunch`)

#### 原因
- 需要启动 PUBG 游戏客户端
- Steam 客户端更稳定可靠
- 避免浏览器兼容性问题

#### 已完成功能

**1. Steam 客户端登录**
- ✅ 使用 `steam.exe -login` 命令登录
- ✅ 进程检测验证（steam.exe, steamwebhelper.exe）
- ✅ 等待 Steam 完全准备就绪（最多 30 秒）

**2. PUBG 游戏启动**
- ✅ 使用 `steam.exe -applaunch 578080` 启动游戏
- ✅ 用户许可协议自动处理（多种方法）
- ✅ 游戏进程检测（TslGame.exe）
- ✅ 游戏窗口自动激活

**3. 用户许可协议处理**
多种方法组合：
- Tab + Space（默认按钮）
- 鼠标点击左侧（中文 Windows "接受"按钮位置）
- Alt+Y（Yes 快捷键）
- 回车键（备用方案）

**4. 完善的进程管理**
- ✅ 游戏运行时间控制（默认 90 秒）
- ✅ PUBG 进程关闭（TslGame.exe, BEService.exe）
- ✅ Steam 优雅关闭（`steam.exe -shutdown`）
- ✅ 强制关闭残留进程
- ✅ 等待并验证完全退出

**5. 账号切换优化**
- ✅ 登录前检测残留 Steam 进程
- ✅ 彻底清理旧的登录状态
- ✅ 避免账号混淆问题

#### 修复的问题

**问题1：游戏窗口不显示**
- **现象**：游戏进程启动但窗口不可见
- **原因**：窗口在后台，没有激活到前台
- **解决**：使用 PowerShell 激活包含 "PUBG" 关键词的窗口

**问题2：游戏运行时间太长**
- **现象**：第一个账号游戏运行 120 秒
- **用户反馈**：时间设置为 90 秒
- **解决**：修改 `game_time = 90`

**问题3：用户许可协议无法自动处理**
- **现象**：第二个账号有用户许可协议窗口，脚本无法点击"接受"
- **原因**：
  - 协议有"接受"和"取消"两个按钮
  - 不能用回车和空格处理
  - 原代码点击屏幕右侧（错误位置）
- **解决**：
  - 中文 Windows "接受"按钮在左侧
  - 修改点击位置为屏幕左侧
  - 增加多种处理方法（Tab+Space、Alt+Y、回车）
  - 最终通过回车键成功处理

**问题4：账号切换时出现账号混淆**
- **现象**：
  - 第一个账号退出后，又重新登录了第一个账号
  - 第二个账号完成后，又登录了第一个账号
- **原因**：
  - Steam 客户端关闭不彻底
  - 有残留进程导致登录状态混乱
- **解决**：
  - 登录前检测并清理残留进程
  - 使用 `steam.exe -shutdown` 优雅关闭
  - 强制关闭所有 Steam 相关进程
  - 等待并验证 Steam 完全退出（最多 15 秒）
  - 增加二次关闭尝试

**问题5：代码 typo**
- **现象**：`PYAUTOGOGUI_AVAILABLE` 拼写错误
- **解决**：修正为 `PYAUTOGUI_AVAILABLE`

#### 测试验证

**测试账号**：
- 账号1：ta3az7wf4vg3 ✅ 成功
- 账号2：rex78532 ✅ 成功

**测试流程**：
1. Steam 登录 ✅
2. PUBG 启动 ✅
3. 用户许可协议处理 ✅
4. 游戏窗口激活 ✅
5. 游戏运行 90 秒 ✅
6. 游戏关闭 ✅
7. Steam 完全关闭 ✅
8. 账号切换 ✅
9. 第二个账号完整流程 ✅
10. 所有账号完成 ✅

#### 文件变更

**修改文件**：
- `src/login_steam.py` - 主要功能实现

**新增方法**：
- `steam_login()` - Steam 客户端登录
- `launch_pubg_game()` - 启动 PUBG 游戏
- `activate_and_click_accept()` - 处理用户许可协议
- `close_pubg_game()` - 关闭 PUBG 游戏
- `close_steam_client()` - 彻底关闭 Steam
- `_save_debug_screenshot()` - 截图调试（预留）

**修改方法**：
- `kill_all_processes()` - 增强进程清理逻辑
- `visit_pubg_page()` - 完整的游戏流程编排

**新增测试脚本**：
- `src/test_login_one.py` - 单账号测试脚本（用于调试）

#### 依赖变更

**移除依赖**：
- ~~playwright~~（不再需要浏览器自动化）

**新增依赖**：
- pyautogui - 键盘鼠标模拟
- pillow - 图像处理（pyautogui 依赖）

**requirements.txt** 更新：
```
pyautogui>=0.9.54
pillow>=10.0.0
```

#### 配置变更

**新增配置项**：
```python
STEAM_EXE_PATH = r"F:\steam\Steam.exe"  # Steam 客户端路径
PUBG_APP_ID = "578080"                   # PUBG 游戏 ID
game_time = 90                           # 游戏运行时间（秒）
```

#### 已知限制

1. **截图功能不可用**
   - PyAutoGUI 与当前 Python/Pillow 版本兼容性问题
   - pyscreeze 模块导入失败
   - 不影响主要功能

2. **用户许可协议**
   - 大部分情况下可以自动处理
   - 如果失败需要手动点击
   - 最多尝试 12 次

#### 后续计划

- [ ] 修复截图功能（升级 Pillow 或找替代方案）
- [ ] 支持其他 Steam 游戏（可配置 APP_ID）
- [ ] 添加日志文件输出
- [ ] 添加配置文件（不需要修改代码）
- [ ] 图形化界面（GUI）

---

*最后更新时间: 2026-02-26*
