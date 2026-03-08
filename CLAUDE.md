# Claude 对话记录 - Steam 账号批量登录脚本

## 项目背景
用户需要一个自动化脚本，能够实现通过账号密码登录 Steam 账号，依次登录多个账号后退出。

---

### 2026-02-13 对话记录

#### 用户需求
- **功能**: 通过账号密码自动登录 Steam
- **工作方式**:
  1. 从 txt 文件读取账号密码
  2. 登录第一个账号
  3. 退出登录
  4. 登录下一个账号
  5. 循环执行
- **最终目标**: 登录 Steam → 进入 PUBG 游戏签到 → 退出 → 切换账号
- **工作方式**:
  1. 从 txt 文件读取账号密码
  2. 登录第一个账号
  3. 退出登录
  4. 登录下一个账号
  5. 循环执行

#### 技术方案
- **语言**: Python
- **理由**: 成熟的 Steam 第三方库、跨平台支持、代码简洁
- **登录方式**: 仅需账号密码，无需 Steam Guard 验证

#### 项目位置
- **路径**: `D:\vscode\LoginScript\`

#### 已完成工作
1. ✅ 创建工作流文档 `WORKFLOW.md`
2. ✅ 创建对话记录文档 `CLAUDE.md`

#### 项目文件结构规划
```
D:\vscode\LoginScript\
├── WORKFLOW.md           # 工作流记录
├── CLAUDE.md             # 对话记录（本文件）
├── login_steam.py        # 主脚本文件（待开发）
├── accounts.txt          # 账号密码文件（待创建）
└── README.md             # 使用说明（待创建）
```

---

## 下一步计划
- [ ] 开发 Python 脚本
- [ ] 创建账号密码文件
- [ ] 测试登录功能

---

### 2026-02-13 开发进度

#### 项目初始化
- ✅ 创建项目文件夹 `D:\vscode\LoginScript\`
- ✅ 创建工作流文档 `WORKFLOW.md`
- ✅ 创建对话记录文档 `CLAUDE.md`

#### 技术选型确定
- **技术**: Python + Playwright（浏览器自动化）
- **理由**:
  - 为后期 PUBG 游戏签到功能预留扩展性
  - Playwright 自动管理浏览器驱动，无需手动下载
  - 支持有头/无头模式切换
  - 更好的跨平台支持

#### 账号文件设计
- ✅ 创建 `accounts.txt`
- ✅ 格式：Tab 分隔（更清晰易读）
- **字段顺序**：Steam账号	Steam密码	邮箱账号	邮箱密码	邮箱地址
- ✅ 支持注释行（# 开头）
- ✅ 已添加 2 个测试账号

#### 配置工具开发
- ✅ 创建 `src/quick_add.py` - Tab 格式快速添加工具
- ✅ 创建 `src/config_accounts.py` - 问答式配置工具
- ⏳️ `src/chinese_to_tab.py` - 中文格式解析工具（调试中）

#### 主脚本开发
- ✅ 创建 `src/login_steam.py` - 完整登录脚本
- ✅ 浏览器自动化（Playwright）
- ✅ 账号文件读取（支持 Tab/冒号格式）
- ✅ 自动登录表单填充（多选择器兼容）
- ✅ Steam Guard 验证（手动输入验证码）
- ✅ 登录状态检测（URL 匹配）
- ✅ 自动登出功能
- ✅ 循环登录逻辑
- ✅ 错误处理（失败自动跳过）
- ✅ 账号间间隔控制
- ✅ Windows 控制台编码修复（emoji 显示）
- ✅ 第二个账号登录失败问题已修复（完全清除浏览器状态）

#### 测试验证
- ✅ 第一个账号登录成功（ta3az7wf4vg3）
- ✅ 第二个账号登录失败问题已定位（rex78532）- 原因：页面状态未完全清除
- ✅ 修复方案：完全清除浏览器状态（cookies + localStorage + sessionStorage）
- ✅ 修复 `logout_steam()` 函数重复定义问题
- ✅ 更新后功能：完整清除所有登录信息

#### 文档完善
- ✅ 更新 `WORKFLOW.md` - 开发过程记录
- ✅ 更新 `CLAUDE.md` - 对话记录
- ✅ 创建 `requirements.txt` - 依赖管理
- ✅ 创建 `README.md` - 小白使用说明
- ✅ 创建 `src/chinese_to_tab.py` - 中文格式转换工具 v6（支持文件批量导入）
- ✅ 创建 `src/quick_add.py` - Tab 格式快速添加工具
- ✅ 创建 `src/config_accounts.py` - 问答式配置工具
- ✅ 创建 `test_import.txt` - 文件导入测试

---

#### 待完成功能
- [x] 修复第二个账号登录问题（完全清除浏览器状态）- ✅ 已完成
- [x] 多账号登录流程完整测试 - ✅ 已完成
- [x] 中文格式文件批量导入 - ✅ 已完成
- [ ] PUBG 游戏签到功能
- [ ] 邮箱验证码自动获取
- [ ] 日志文件输出
- [ ] 截图保存功能（调试用）

---

## 2026-02-13 更新记录

### 中文格式文件批量导入功能

#### 用户需求
用户希望创建一个 txt 文件，直接粘贴中文格式的账号信息：
```
steam账号ta3az7wf4vg3密码Av6Ih8Bh8Fd7邮箱账号FCJPT30502@gdh333.cn邮箱密码MLOBV00990邮箱地址x.pubg.fit
账号rex78532密码PeF753606邮箱账号n7w77v@sdhgz.cn邮箱密码374777邮箱登录地址https://a.dcmya.com/
```

然后运行脚本就能自动解析并保存到 accounts.txt。

#### 实现方案
- **工具**: `src/chinese_to_tab.py`
- **新增功能**:
  - 支持命令行参数：`python src\chinese_to_tab.py <输入文件>`
  - 自动批量解析文件中的每一行
  - 显示解析结果和失败列表
  - 直接保存到 accounts.txt

#### 使用方法

**步骤1**: 创建输入文件（如 `test_import.txt`）
```text
steam账号ta3az7wf4vg3密码Av6Ih8Bh8Fd7邮箱账号FCJPT30502@gdh333.cn邮箱密码MLOBV00990邮箱地址x.pubg.fit
账号rex78532密码PeF753606邮箱账号n7w77v@sdhgz.cn邮箱密码374777邮箱登录地址https://a.dcmya.com/
```

**步骤2**: 运行转换工具
```bash
python src\chinese_to_tab.py test_import.txt
```

**步骤3**: 工具自动解析并保存到 accounts.txt
```bash
✅ 成功解析 2 个账号
✅ 成功保存到 accounts.txt
```

**步骤4**: 运行登录脚本
```bash
python src\login_steam.py
```

#### 技术细节
- 使用正则表达式前瞻断言精确匹配各字段
- 自动清理邮箱地址的协议前缀（https://, http://）和末尾斜杠
- 支持的关键词变体：
  - 用户名：steam账号、账号
  - 邮箱：邮箱账号、邮箱
  - 邮箱密码：邮箱密码
  - 邮箱地址：邮箱地址、邮箱登录地址、邮箱网站

#### 测试验证
- ✅ 成功解析 2 个测试账号
- ✅ 正确转换到 Tab 格式
- ✅ 登录脚本成功读取并使用

---

## 2026-02-26 对话记录 - v2.0 重大更新

### 用户需求更新
用户希望实现更完整的功能：
- 登录 Steam 后启动 PUBG 游戏
- 游戏运行一段时间后退出
- 切换到下一个账号

### 开发过程

#### 阶段1：从浏览器登录切换到 Steam 客户端登录

**问题**：原有的 Playwright 浏览器登录方式无法启动游戏客户端

**解决方案**：
- 改用 Steam 命令行登录：`steam.exe -login <username> <password>`
- 使用 Steam 协议启动游戏：`steam.exe -applaunch <APP_ID>`

**技术要点**：
- 使用 `subprocess.Popen()` 启动 Steam
- 进程检测验证（`tasklist` 命令）
- 等待 Steam 完全准备就绪

#### 阶段2：PUBG 游戏启动实现

**实现方法**：
```python
cmd = [self.STEAM_EXE_PATH, "-applaunch", self.PUBG_APP_ID]
subprocess.Popen(cmd, shell=False)
```

**验证方式**：
- 检测 `TslGame.exe` 进程
- 激活游戏窗口到前台

#### 阶段3：用户许可协议处理（最大挑战）

**问题1**：第二个账号有用户许可协议窗口，脚本无法处理

**用户反馈**：
- "这个用户许可协议只有两个选项，一个是接受，一个是取消，点击一下接收就行"
- "脚本一直无法实现，我猜测这个是不能通过回车和空格来接收的，考虑一下其他方法"

**解决过程**：

1. **尝试 Tab + Space** - 失败
2. **鼠标点击屏幕右侧** - 失败，点击了错误的位置
3. **用户反馈**："账号2还是没有实现，最后是停留在别的页面了，可能点击的位置错误了"

**关键发现**：
- 中文 Windows 对话框中，"接受/确定"按钮在**左侧**
- "取消"按钮在**右侧**
- 原代码点击右侧，实际点击了"取消"

**最终解决方案**：
- 修改点击位置为屏幕左侧
- 多种方法组合：Tab+Space → 左侧鼠标点击 → Alt+Y → 回车键
- 回车键最终成功处理协议

#### 阶段4：账号切换问题（关键修复）

**问题**：
- 第一个账号退出后，又重新登录了第一个账号
- 第二个账号完成后，又启动了第一个账号的游戏

**用户反馈**：
"第一个账户退出游戏界面，再退出steam客户端，又重新登录了这个账户的steam客户端；然后再重新登录为另一个账号的steam的客户端，登录游戏；但是退出有限界面后，又重新登录了这个账户的steam客户端，还启动了游戏"

**原因分析**：
- Steam 客户端关闭不彻底
- 有残留进程保留了登录状态
- 下次启动时使用了旧的登录信息

**解决方案**：

1. **登录前清理**：
```python
def steam_login(self, username, password):
    # 检查并清理残留的 Steam 进程
    if self.check_process_running("steam.exe"):
        self.kill_all_processes()
        time.sleep(3)
```

2. **彻底关闭 Steam**：
```python
def close_steam_client(self):
    # 方法1：优雅关闭
    subprocess.run([self.STEAM_EXE_PATH, "-shutdown"], ...)

    # 方法2：强制关闭所有进程
    for proc in steam_processes:
        subprocess.run(f"taskkill /F /IM {proc} ...")

    # 方法3：等待并验证
    for i in range(15):
        if not self.check_process_running("steam.exe"):
            return True
```

3. **增强进程清理**：
- 两次关闭尝试
- 验证关键进程是否已关闭
- 针对顽固进程的额外处理

#### 阶段5：完善和测试

**用户需求**：
- "第一个账号成功启动了，但是我感觉在游戏页面停留得有点久，时间设置为90s吧"

**实现**：
```python
game_time = 90  # 90秒
```

**最终测试结果**：
- 账号1 (ta3az7wf4vg3)：✅ 完全成功
- 账号2 (rex78532)：✅ 完全成功

### 技术总结

**核心改动**：
1. 从 Playwright 浏览器自动化 → Steam CLI
2. 新增 PUBG 游戏启动功能
3. 新增用户许可协议处理
4. 新增游戏窗口激活
5. 完善进程管理和清理

**依赖变更**：
- 移除：playwright
- 新增：pyautogui, pillow

**新增文件**：
- `src/test_login_one.py` - 单账号测试脚本

**修改文件**：
- `src/login_steam.py` - 主要功能实现

### 遇到的问题和解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 游戏窗口不显示 | 窗口在后台 | PowerShell 激活窗口 |
| 游戏运行时间长 | 默认120秒 | 改为90秒 |
| 许可协议无法处理 | 点击位置错误 | 改为点击左侧 + 多种方法 |
| 账号混淆 | Steam关闭不彻底 | 登录前清理 + 优雅关闭 + 验证 |
| 代码typo | `PYAUTOGOGUI_AVAILABLE` | 修正为 `PYAUTOGUI_AVAILABLE` |

---

*最后更新: 2026-02-26*


---

## 2026-03-06 对话记录 - OpenCV 图像识别集成

### 用户需求更新

1. **协议窗口智能检测**：
   - "还有一点我要和你明确一下。当代码启动pubg的时候，要检查一下当前是否有"最终用户协议"的页面，如果有这个页面的话，就点击"接受"按钮。因为这个页面不一定会出现的"

2. **高置信度点击**：
   - "然后点击"接受"按钮的动作，我感觉必须是图像识别"接受"按钮置信度大于比如说95这样"

3. **位置无关识别**：
   - "这些位置中按钮的位置确实不同，但是你必须得具备识别不同位置按钮的功能"

4. **项目文件整理**：
   - "你修改吧。同时这个项目文件中，有太多文件里。你整理一下。"

### 开发过程

#### 阶段1: pyautogui 测试失败

**测试结果**：
- 使用 `pyautogui.locateOnScreen()` 测试 3 张图片
- 成功率：0% (0/3)
- 问题：pyautogui 算法精度不够

#### 阶段2: OpenCV 高精度识别

**实现**：
- 创建 `test_enhanced_recognition.py` 测试脚本
- 使用 `cv2.matchTemplate()` with `TM_CCORR_NORMED`
- 测试结果：100% 成功率 (3/3)
- 相似度：99.09%, 99.05%, 99.10%

#### 阶段3: 集成到主脚本

**修改的文件**：
1. **`src/login_steam.py`**:
   - 替换 `activate_and_click_accept()` 方法，使用 OpenCV
   - 替换 `check_for_agreement_window()` 方法，使用 OpenCV
   - 添加 `self.project_root` 属性
   - 修复 `main()` 函数，使用 `visit_pubg_page()` 而不是旧的 `run()`
   - 修复 `self.PYAUTOGUI_AVAILABLE` → `PYAUTOGUI_AVAILABLE`
   - 简化 `wait_for_steam_ready()` 检测逻辑

2. **`src/steam_login_gui.py`**:
   - 更新到 v2.2
   - 添加 opencv-python 环境检查
   - 添加 accept_button.png 模板检查

3. **创建 `config.json`**:
   - Steam 路径配置
   - 游戏时间配置 (90秒)

#### 阶段4: 项目文件清理

**删除的文件** (12+ 个冗余文件):
- check_agreement.py
- fix_click_confidence.py
- new_activate_and_click_accept.txt
- test_enhanced_recognition.py
- test_images_recognition.py
- 停止按钮修复说明.md
- 协议窗口检测优化说明.md
- 启动文件检查报告.md
- 实时日志优化说明.md
- 带标记的图像识别说明.md
- 环境检查界面更新说明.md
- 高置信度点击优化说明.md
- 图像识别优化方案.md
- 项目文件总览.md

**创建的文档**:
- `项目说明.md` - 统一的项目文档
- `项目检查报告.md` - 运行前检查清单
- `OPENCV_INTEGRATION_COMPLETE.md` - OpenCV 集成完成报告

#### 阶段5: 关键 Bug 修复

**问题1**: main() 函数使用旧方法
- **原因**: `main()` 调用的是 `bot.run()` (Playwright 浏览器方法)
- **修复**: 改为循环调用 `bot.visit_pubg_page()` (Steam 客户端方法)

**问题2**: self.PYAUTOGUI_AVAILABLE 不存在
- **原因**: `PYAUTOGUI_AVAILABLE` 是全局变量，不是类属性
- **修复**: `self.PYAUTOGUI_AVAILABLE` → `PYAUTOGUI_AVAILABLE`

**问题3**: wait_for_steam_ready() 检测失败
- **原因**: 等待 `steamwebhelper.exe` 但检测不到
- **修复**: 简化为只检测 `steam.exe` 进程存在即可

**问题4**: Steam 启动后立即失败
- **原因**: 各种检测逻辑问题
- **修复**: 完善错误处理和超时机制

### 技术细节

#### OpenCV 图像识别

**方法**：
```python
# 模板匹配
result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCORR_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

similarity = max_val  # 0-1 范围
location = max_loc    # (x, y) 坐标
```

**阈值设置**：
- **协议窗口检测**: 50% (similarity >= 0.50)
- **点击按钮**: 95% (similarity >= 0.95)

**激活窗口**：
```python
keywords = ["许可", "协议", "License", "Agreement", "User", "EULA", 
            "Terms", "PUBG", "BATTLEGROUNDS", "Steam", "Subscriber", "Accept", "同意"]
```

#### 完整工作流程

```
1. 加载账号 ✅
   ↓
2. 清理残留进程 ✅
   ↓
3. Steam 客户端登录 ✅
   - steam.exe -login <user> <pass>
   - 等待 steam.exe 进程启动
   ↓
4. 启动 PUBG 游戏 ✅
   - steam.exe -applaunch 578080
   ↓
5. 检测协议窗口 ✅
   - OpenCV 全屏搜索
   - 相似度 >= 50% 认为存在
   ↓
6. 点击"接受"按钮 ✅
   - OpenCV 精确定位
   - 相似度 >= 95% 才点击
   ↓
7. 游戏运行 90 秒 ✅
   ↓
8. 关闭游戏和 Steam ✅
   ↓
9. 切换下一个账号 ✅
```

### 文件变更总结

**核心文件**:
- `src/login_steam.py` - 主脚本 (已更新)
- `src/steam_login_gui.py` - GUI (已更新)
- `src/accept_button.png` - 模板图片 (82x17 像素)

**配置文件**:
- `accounts.txt` - 账号列表
- `config.json` - GUI 配置
- `requirements.txt` - Python 依赖

**文档**:
- `项目说明.md` - 项目总览
- `项目检查报告.md` - 运行前检查
- `CLAUDE.md` - 本文件

### 当前状态

**版本**: v2.2 (图像识别版)

**已实现功能**:
- ✅ Steam 客户端登录
- ✅ PUBG 游戏启动
- ✅ OpenCV 智能协议窗口检测
- ✅ 高精度图像识别点击 (95% 置信度)
- ✅ 全屏任意位置按钮识别
- ✅ 游戏运行 90 秒
- ✅ 完整的进程管理

**待改进功能**:
- ⏳ Steam 加载完成的精确检测 (当前只检测进程存在)
  - 用户建议：等待 Steam 商店页面加载完成后再启动 PUBG
  - 可能方案：检测 Steam 窗口标题或使用 pywin32

### 依赖项

**必需**:
- Python 3.8+
- pyautogui
- pillow
- opencv-python
- numpy

**可选** (GUI 需要但命令行不需要):
- playwright (已不用，可以移除)

### 测试账号

```
账号: 89599811
密码: 35935445
邮箱: YSdqSVVK@744368.ljjmail.com
邮箱密码: 742001
邮箱地址: https://mail.pubgs.team
```

### 遇到的问题和解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| pyautogui 识别失败 | 算法精度不够 | 改用 OpenCV TM_CCORR_NORMED |
| 协议窗口误点击 | 置信度太低 | 设置 95% 阈值 |
| 脚本立即结束 | main() 用错方法 | 改用 visit_pubg_page() |
| self.PYAUTOGUI_AVAILABLE | 不是类属性 | 改用全局变量 |
| Steam 检测失败 | 等待 steamwebhelper.exe | 只检测 steam.exe |
| 项目文件混乱 | 太多测试文件 | 删除 12+ 冗余文件 |

---

*最后更新: 2026-03-06*
*版本: v2.2 (图像识别版)*
*OpenCV 成功率: 100% (3/3 测试图片)*
