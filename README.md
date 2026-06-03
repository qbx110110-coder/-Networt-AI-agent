# Network AI Agent 🌐

一个智能网络设备管理系统，可以使用 Telnet 和 SSH 协议连接网络交换机，通过对接大模型（LLM）实现自然语言命令配置。

## 功能特性 ✨

- **多协议支持**: 支持 Telnet 和 SSH 两种连接方式
- **AI 驱动**: 集成大模型（OpenAI/Claude/本地 LLM）
- **智能命令解析**: 将自然语言转换为网络设备命令
- **设备管理**: 支持交换机、路由器等网络设备
- **日志记录**: 完整的操作日志和审计跟踪
- **错误处理**: 智能错误恢复和重试机制
- **安全性**: 命令验证、干运行模式、权限管理

## 架构设计 🏗️

```
┌─────────────┐
│   用户输入   │
└──────┬──────┘
       │
┌──────▼──────────────────┐
│   LLM 大模型处理        │
│  (解析意图和命令)       │
└──────┬──────────────────┘
       │
┌──────▼──────────────────┐
│   命令验证和优化        │
└──────┬──────────────────┘
       │
┌──────▼──────────────────────────┐
│   网络连接模块                   │
│  ├─ SSH 连接                    │
│  └─ Telnet 连接                 │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────┐
│   网络设备执行命令       │
│  (交换机/路由器)        │
└──────────────────────────┘
```

## 快速开始 🚀

### 环境要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

编辑 `config/config.yaml`:

```yaml
llm:
  provider: openai
  openai:
    api_key: your_openai_api_key
    model: gpt-4
    temperature: 0.3

devices:
  switch1:
    host: 192.168.1.1
    port: 22
    username: admin
    password: ${SWITCH1_PASSWORD}
    protocol: ssh
    device_type: cisco_ios
    enabled: true

agent:
  dry_run: true
  allow_config_changes: true
  validate_commands: true
```

### 运行

```bash
# 交互式模式
python src/main.py

# 或者在 Python 代码中使用
from src.agent.network_agent import NetworkAgent

agent = NetworkAgent()
result = agent.execute("配置交换机 VLAN 100")
print(result)
```

## 项目结构 📁

```
.
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
│   └── config.yaml              # 主配置文件
├── src/
│   ├── main.py                  # 主入口
│   ├── llm/
│   │   ├── base.py              # LLM 基类
│   │   └── openai_client.py     # OpenAI 实现
│   ├── network/
│   │   ├── connection.py        # 连接基类
│   │   ├── ssh_handler.py       # SSH 实现
│   │   ├── telnet_handler.py    # Telnet 实现
│   │   └── device_manager.py    # 设备管理器
│   ├── agent/
│   │   ├── network_agent.py     # 主 Agent
│   │   └── command_executor.py  # 命令执行器
│   ├── utils/
│   │   ├── logger.py            # 日志工具
│   │   └── config_loader.py     # 配置加载器
│   └── prompts/
│       └── system_prompts.py    # 系统提示词
├── tests/
│   └── test_connection.py       # 单元测试
└── examples/
    ├── basic_usage.py           # 基础使用示例
    └── advanced_usage.py        # 高级使用示例
```

## 使用示例 💡

### 基础使用

```python
from src.agent.network_agent import NetworkAgent

# 初始化 Agent
agent = NetworkAgent(config_path='config/config.yaml')

# 配置 VLAN
result = agent.execute("配置交换机1的 VLAN 100")
print(f"状态: {result['status']}")
print(f"命令: {result['commands']['commands']}")
print(f"结果: {result['results']}")
```

### 批量配置

```python
commands = [
    "创建 VLAN 100",
    "创建 VLAN 200",
    "配置端口 1-10 为 VLAN 100"
]

results = agent.execute_batch(commands)
for result in results:
    print(f"状态: {result['status']}")
```

### 干运行模式（安全模式）

```python
# 干运行模式 - 不实际执行命令，只生成和验证
result = agent.execute(
    "重启交换机",
    device_name="switch1",
    dry_run=True  # 启用干运行
)
print(result)  # 显示将要执行的命令
```

## 核心功能详解 🔧

### 1. 自然语言处理

Agent 使用 LLM 将自然语言请求转换为网络命令：

```
用户输入: "配置 VLAN 100"
  ↓ (LLM 解析)
生成命令: ["vlan 100", "name VLAN-100", "exit"]
  ↓ (验证)
执行命令: ✓
```

### 2. 多协议支持

- **SSH**: 安全的加密连接（推荐）
- **Telnet**: 明文连接（用于遗留设备）

### 3. 安全机制

- **命令验证**: 验证命令的安全性
- **干运行模式**: 预览命令不执行
- **禁止关键字**: 防止危险操作
- **日志审计**: 记录所有操作

### 4. 设备管理

支持多个设备的管理和批量操作：

```python
# 获取设备状态
status = agent.get_device_status()
print(status)

# 广播命令
results = agent.device_manager.broadcast_command(
    "show version",
    devices=["switch1", "switch2"]
)
```

## 配置说明 📋

### LLM 配置

```yaml
llm:
  provider: openai  # openai, claude, ollama
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4
    temperature: 0.3  # 低温度 = 更确定的输出
    max_tokens: 2000
```

### 设备配置

```yaml
devices:
  switch1:
    host: 192.168.1.1
    port: 22
    protocol: ssh      # ssh 或 telnet
    username: admin
    password: ${SWITCH1_PASSWORD}
    device_type: cisco_ios
    enabled: true
```

### Agent 配置

```yaml
agent:
  dry_run: true              # 干运行模式
  allow_config_changes: true # 允许配置修改
  validate_commands: true    # 验证命令
  forbidden_keywords:
    - "erase"
    - "delete"
    - "reload"
```

## 日志记录 📝

默认日志位置: `logs/network_agent.log`

```
2024-06-03 10:30:45 - NetworkAgent - INFO - Network AI Agent initialized
2024-06-03 10:30:46 - DeviceManager - INFO - Connected to switch1 via SSH
2024-06-03 10:30:47 - CommandExecutor - INFO - Command executed on switch1
```

## 常见问题 ❓

### Q: 如何连接到我的交换机？
A: 编辑 `config/config.yaml`，填入交换机的 IP 地址、用户名和密码。

### Q: 支持哪些网络设备？
A: 支持任何支持 SSH/Telnet 的设备（Cisco、Arista、Juniper 等）。

### Q: 如何启用干运行模式？
A: 设置 `dry_run: true` 或在执行时传递 `dry_run=True`。

### Q: 如何添加新的 LLM 提供商？
A: 在 `src/llm/` 中创建新的类继承 `BaseLLM`。

## 贡献指南 🤝

欢迎提交 Issue 和 Pull Request！

## 许可证 📜

MIT License

## 联系方式 📧

如有问题，请提交 GitHub Issue。
