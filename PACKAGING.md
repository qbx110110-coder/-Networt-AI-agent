# 网络 AI Agent - Windows 打包指南

## 📦 打包要求

### 系统要求
- Windows 10 或更高版本
- 至少 2GB 可用磁盘空间
- 互联网连接（用于下载依赖）

### 软件要求
1. **Python 3.8+** - https://www.python.org/
   - 安装时勾选 "Add Python to PATH"

2. **NSIS** (可选，用于创建安装程序) - https://nsis.sourceforge.io/
   - 用于生成 Network-AI-Agent-Setup.exe
   - 如果不安装，仍可生成独立可执行文件

## 🚀 快速打包步骤

### 方法 1：使用批处理脚本（推荐）

1. **打开命令提示符**（Win + R，输入 `cmd`）

2. **导航到项目目录**
   ```bash
   cd C:\path\to\-Networt-AI-agent
   ```

3. **运行构建脚本**
   ```bash
   build.bat
   ```

4. **等待构建完成**
   - 脚本会自动安装依赖
   - 生成可执行文件在 `dist` 文件夹中

### 方法 2：手动打包步骤

1. **安装构建依赖**
   ```bash
   pip install -r requirements-build.txt
   pip install -r requirements.txt
   ```

2. **构建可执行文件**
   ```bash
   python build_installer.py
   ```
   或使用 PyInstaller 直接：
   ```bash
   pyinstaller --onefile --windowed --add-data "config:config" --hidden-import=paramiko --hidden-import=openai --name=NetworkAIAgent src/main.py
   ```

3. **创建安装程序**（可选）
   - 安装 NSIS
   - 运行：`makensis.exe network_ai_agent_installer.nsi`

## 📁 打包输出

构建完成后，你会得到：

```
输出文件结构:
├── dist/
│   └── NetworkAIAgent/
│       ├── NetworkAIAgent.exe         # 主程序可执行文件
│       ├── python*.dll                # Python 运行库
│       ├── _internal/                 # 依赖库文件夹
│       ├── config/                    # 配置文件
│       ├── .env.example               # 环境变量示例
│       └── README.md                  # 说明文档
│
└── Network-AI-Agent-Setup.exe         # Windows 安装程序（如果安装了 NSIS）
```

## ⚙️ 配置安装

### 使用独立可执行文件

1. **运行可执行文件**
   ```
   dist/NetworkAIAgent/NetworkAIAgent.exe
   ```

2. **首次运行配置**
   - 复制 `.env.example` 为 `.env`
   - 添加你的 OpenAI API 密钥
   - 编辑 `config/config.yaml` 配置网络设备

### 使用安装程序（如有）

1. **双击运行 Network-AI-Agent-Setup.exe**

2. **按照安装向导操作**
   - 选择安装位置
   - 完成安装

3. **配置应用**
   - 在安装目录找到 `.env.example`
   - 复制为 `.env` 并配置 API 密钥
   - 修改 `config/config.yaml`

4. **运行应用**
   - 从开始菜单选择 "Network AI Agent"
   - 或双击桌面快捷方式

## 🔧 故障排除

### 问题 1："Python 不是内部或外部命令"

**解决方案**：
1. 重新安装 Python
2. 安装时勾选 "Add Python to PATH"
3. 重启命令提示符

### 问题 2："缺少模块" 错误

**解决方案**：
```bash
pip install -r requirements.txt --upgrade
pip install -r requirements-build.txt --upgrade
```

### 问题 3：NSIS 找不到

**解决方案**：
- 从 https://nsis.sourceforge.io 下载并安装 NSIS
- 手动运行：`C:\\Program Files (x86)\\NSIS\\makensis.exe network_ai_agent_installer.nsi`

### 问题 4：可执行文件无法运行

**解决方案**：
1. 确保 .NET Framework 已安装
2. 检查防病毒软件是否阻止
3. 以管理员身份运行

## 📋 分发清单

打包完成后，分发包含：

- ✅ `NetworkAIAgent.exe` - 主程序
- ✅ 所有依赖库
- ✅ 配置示例文件
- ✅ 说明文档
- ✅ 快速启动脚本

## 💾 大小和性能

- **可执行文件大小**：~80-120 MB（包含所有依赖）
- **安装大小**：~200-300 MB（解压后）
- **内存占用**：~200-400 MB（运行时）
- **启动时间**：~2-5 秒

## 🔐 安全建议

1. **保护 API 密钥**
   - 不要在 GitHub 上提交 `.env` 文件
   - 定期轮换 API 密钥

2. **安装更新**
   - 定期更新 Python 依赖
   - 检查安全补丁

3. **配置备份**
   - 备份 `config/config.yaml`
   - 记录设备凭证

## 📚 相关链接

- [Python 下载](https://www.python.org/downloads/)
- [NSIS 项目](https://nsis.sourceforge.io/)
- [PyInstaller 文档](https://pyinstaller.org/)
- [项目 GitHub](https://github.com/qbx110110-coder/-Networt-AI-agent)

## ✅ 验证安装

安装后验证：

1. **检查版本**
   ```bash
   NetworkAIAgent.exe --version
   ```

2. **测试连接**
   - 启动应用
   - 输入测试命令
   - 验证响应

3. **查看日志**
   - 检查 `logs/network_agent.log`
   - 验证没有错误

## 🆘 获取帮助

遇到问题？

1. 查看 [README.md](README.md) 的常见问题部分
2. 检查日志文件 `logs/network_agent.log`
3. 在 [GitHub Issues](https://github.com/qbx110110-coder/-Networt-AI-agent/issues) 提交问题

---

**祝你打包顺利！** 🎉
