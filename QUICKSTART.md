# 快速开始

## Windows 用户 - 快速安装

### 方法 A：使用安装程序（推荐）

1. **下载** `Network-AI-Agent-Setup.exe`

2. **双击运行**安装程序

3. **按照向导完成安装**

4. **配置应用**
   - 在安装目录找到 `.env.example`
   - 复制为 `.env`
   - 添加你的 OpenAI API 密钥：
     ```
     OPENAI_API_KEY=sk-...
     ```

5. **编辑配置文件** `config/config.yaml`
   ```yaml
   devices:
     switch1:
       host: 192.168.1.1
       username: admin
       password: your_password
   ```

6. **运行应用**
   - 从开始菜单找到 "Network AI Agent"
   - 或双击桌面快捷方式

### 方法 B：直接运行可执行文件

1. **提取文件夹**包含 `NetworkAIAgent.exe`

2. **双击** `NetworkAIAgent.exe` 运行

3. **配置**同上

## 从源代码构建（开发者）

### 前置要求

- Python 3.8+ - https://www.python.org/
- NSIS (可选) - https://nsis.sourceforge.io/

### 构建步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/qbx110110-coder/-Networt-AI-agent.git
   cd -Networt-AI-agent
   ```

2. **运行构建脚本**
   ```bash
   build.bat
   ```

3. **找到输出**
   - `dist/NetworkAIAgent/NetworkAIAgent.exe` - 可执行文件
   - `Network-AI-Agent-Setup.exe` - 安装程序（如果有 NSIS）

## 使用示例

### 交互式模式

```
$ NetworkAIAgent.exe

============================================================
Network AI Agent - Interactive Configuration
============================================================

Enter your request (or 'quit' to exit): configure VLAN 100
Processing request...

Status: success
Commands Generated:
  > vlan 100
  > name VLAN-100
  > exit

Execution Results:
  [success] vlan 100
  [success] name VLAN-100
```

### Python 代码集成

```python
from src.agent.network_agent import NetworkAgent

agent = NetworkAgent()
result = agent.execute("Configure VLAN 100", device_name="switch1")
print(f"状态: {result['status']}")
```

## 常见问题

### Q: 如何修改配置？

A: 编辑安装目录中的 `config/config.yaml`：
```yaml
llm:
  provider: openai
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4

devices:
  my_switch:
    host: 192.168.1.1
    username: admin
```

### Q: 安装后找不到应用？

A: 
1. 检查开始菜单中的 "Network AI Agent"
2. 或在安装目录直接运行 `NetworkAIAgent.exe`
3. 查看桌面快捷方式

### Q: 如何卸载？

A: 
1. 控制面板 → 程序 → 程序和功能
2. 找到 "Network AI Agent"
3. 点击卸载

## 获取支持

- 📖 查看 [README.md](README.md)
- 📋 查看 [PACKAGING.md](PACKAGING.md)
- 🐛 提交 Issue: https://github.com/qbx110110-coder/-Networt-AI-agent/issues
- 💬 讨论: https://github.com/qbx110110-coder/-Networt-AI-agent/discussions

---

**祝你使用愉快！** 🚀
