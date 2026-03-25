# Claude Code 国内使用完整指南【2026 年最新】

> 国内开发者使用 Claude Code 的完整解决方案 — 无需魔法，5 分钟配置，即刻开始 AI 编程

## 📌 你遇到的问题

如果你是国内开发者，想用 Claude Code 但遇到了这些问题：

- ❌ Claude Code 直连超时、403 被拒
- ❌ 注册 Anthropic 需要海外手机号和信用卡
- ❌ 官方 Max 订阅每月 $100-200，门槛太高
- ❌ 不确定中转服务是否稳定可靠

本指南提供一个**经过验证的解决方案**，让你在国内流畅使用 Claude Code。

## 🚀 解决方案：通过 MaxRouter 中转

[MaxRouter](https://www.maxrouter.ai) 提供 Anthropic API 中转服务，兼容 Claude Code 原生协议，国内直连无需代理。

**核心优势：**
- ✅ 国内直连，无需任何代理工具
- ✅ 兼容 Claude Code 原生协议，无缝切换
- ✅ 按量计费，用多少付多少，无月费
- ✅ 注册即送 ¥10 体验金，免费试用
- ✅ 支持所有 Claude 模型（Opus 4、Sonnet 4、Haiku 等）

## 📋 配置步骤

### 第一步：注册 MaxRouter 账号

访问 [www.maxrouter.ai](https://www.maxrouter.ai)，注册账号（注册即送 ¥10 体验金）。

### 第二步：获取 API Key

登录后进入 [控制台 → 令牌管理](https://www.maxrouter.ai/console/tokens)，创建一个新的 API Key（以 `sk-` 开头）。

### 第三步：配置 Claude Code

在终端中设置环境变量：

**macOS / Linux（Zsh）：**

```bash
# 编辑 ~/.zshrc，添加以下两行
export ANTHROPIC_BASE_URL=https://api.maxrouter.ai
export ANTHROPIC_API_KEY=sk-your-key

# 使配置生效
source ~/.zshrc
```

**macOS / Linux（Bash）：**

```bash
# 编辑 ~/.bashrc，添加以下两行
export ANTHROPIC_BASE_URL=https://api.maxrouter.ai
export ANTHROPIC_API_KEY=sk-your-key

# 使配置生效
source ~/.bashrc
```

**Windows（PowerShell）：**

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.maxrouter.ai"
$env:ANTHROPIC_API_KEY = "sk-your-key"
```

**Windows（永久设置）：**

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "https://api.maxrouter.ai", "User")
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-your-key", "User")
```

### 第四步：启动 Claude Code

```bash
claude
```

就这么简单。Claude Code 会自动使用你配置的 MaxRouter 中转地址。

> ⚠️ **注意：** `ANTHROPIC_BASE_URL` 设置为 `https://api.maxrouter.ai`（**不带 `/v1`**），Claude Code 会自动拼接 `/v1/messages` 路径。

## 🤖 支持的 Claude 模型

| 模型 | 说明 | 适用场景 |
|------|------|----------|
| `claude-opus-4` | 最强推理能力 | 复杂架构设计、大型重构 |
| `claude-sonnet-4` | 性能与成本平衡 | 日常编程、代码审查 |
| `claude-sonnet-4-thinking` | 带思维链的 Sonnet | 复杂调试、多步推理 |
| `claude-haiku-4` | 快速响应 | 简单任务、代码补全 |

在 Claude Code 中切换模型：

```
/model claude-opus-4
```

## 🔧 常见开发工具配置

### Cursor

1. 打开设置 → Models
2. 添加自定义模型：
   - Override OpenAI Base URL: `https://api.maxrouter.ai/v1`
   - API Key: `sk-your-key`
   - 模型名: `claude-sonnet-4`

### Cline（VS Code 插件）

1. 安装 Cline 插件
2. 设置 → API Provider → OpenAI Compatible
3. Base URL: `https://api.maxrouter.ai/v1`
4. API Key: `sk-your-key`

### Continue（VS Code / JetBrains）

编辑 `~/.continue/config.json`：

```json
{
  "models": [{
    "title": "Claude via MaxRouter",
    "provider": "openai",
    "model": "claude-sonnet-4",
    "apiKey": "sk-your-key",
    "apiBase": "https://api.maxrouter.ai/v1"
  }]
}
```

### ChatBox

1. 设置 → API Provider → OpenAI API Compatible
2. API Host: `https://api.maxrouter.ai`
3. API Key: `sk-your-key`
4. 模型: `claude-sonnet-4`

### NextChat（ChatGPT Next Web）

1. 设置 → 接口地址: `https://api.maxrouter.ai`
2. API Key: `sk-your-key`
3. 自定义模型名: `claude-sonnet-4`

## 💻 API 直接调用示例

MaxRouter 同时兼容 OpenAI SDK 格式，方便在代码中集成：

**Python：**

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-key",
    base_url="https://api.maxrouter.ai/v1"
)

response = client.chat.completions.create(
    model="claude-sonnet-4",
    messages=[{"role": "user", "content": "用 Python 写一个快速排序"}]
)
print(response.choices[0].message.content)
```

**Node.js：**

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
    apiKey: 'sk-your-key',
    baseURL: 'https://api.maxrouter.ai/v1'
});

const response = await client.chat.completions.create({
    model: 'claude-sonnet-4',
    messages: [{ role: 'user', content: '用 TypeScript 写一个 HTTP 服务器' }]
});
console.log(response.choices[0].message.content);
```

**cURL：**

```bash
curl https://api.maxrouter.ai/v1/chat/completions \
  -H "Authorization: Bearer sk-your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

## ❓ 常见问题

### Q: 跟官方直连有什么区别？
A: 功能完全一致，MaxRouter 只做请求转发，不修改任何内容。区别是你不需要代理工具，国内直连即可。

### Q: 支持流式输出吗？
A: 支持。Claude Code 默认使用流式输出，MaxRouter 完整支持 SSE 流式传输。

### Q: 速度怎么样？
A: MaxRouter 服务器部署在海外，延迟通常在 200-500ms，实际使用中 Claude 模型本身的推理时间远大于网络延迟，体感差异不大。

### Q: 数据安全吗？
A: MaxRouter 不存储任何对话内容，请求直接转发到 Anthropic 官方 API。

### Q: 怎么计费？
A: 按 token 用量计费，与 Anthropic 官方价格一致或略有加成。注册即送 ¥10 体验金，可以先免费试用。

### Q: 支持哪些支付方式？
A: 支持信用卡（Visa / Mastercard）支付，后续将支持更多支付方式。

## 🔗 相关链接

- 🌐 官网：[www.maxrouter.ai](https://www.maxrouter.ai)
- 📖 完整文档：[www.maxrouter.ai/docs](https://www.maxrouter.ai/docs)
- 🤖 模型列表：[www.maxrouter.ai/models](https://www.maxrouter.ai/models)
- 💰 价格查询：[www.maxrouter.ai/pricing](https://www.maxrouter.ai/pricing)
- 🔑 获取 API Key：[www.maxrouter.ai/console/tokens](https://www.maxrouter.ai/console/tokens)

---

**⭐ 如果这个指南对你有帮助，请给个 Star，让更多开发者看到！**
