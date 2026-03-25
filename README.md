# Claude Code 完整教程：从安装到实战（国内开发者指南）

> Claude Code 是 Anthropic 推出的终端 AI 编程助手，可以直接在命令行中理解你的代码库、编写代码、执行命令、管理 Git。本文从零开始，带你完成安装、配置和实际使用。

## 目录

- [什么是 Claude Code](#什么是-claude-code)
- [Claude Code 能做什么](#claude-code-能做什么)
- [安装 Claude Code](#安装-claude-code)
- [官方订阅方案](#官方订阅方案)
- [国内开发者面临的问题](#国内开发者面临的问题)
- [替代方案：通过 API 中转使用](#替代方案通过-api-中转使用)
- [配置 MaxRouter 中转](#配置-maxrouter-中转)
- [Claude Code 常用命令](#claude-code-常用命令)
- [实战：用 Claude Code 开发一个项目](#实战用-claude-code-开发一个项目)
- [进阶技巧](#进阶技巧)
- [常见问题](#常见问题)

---

## 什么是 Claude Code

Claude Code 是 Anthropic 在 2025 年推出的命令行 AI 编程工具。跟 GitHub Copilot 这类 IDE 插件不同，Claude Code 直接运行在你的终端里，它可以：

- 阅读和理解你的整个代码库
- 编写、修改、删除文件
- 执行终端命令（编译、测试、部署等）
- 管理 Git（提交、分支、合并）
- 搜索代码、分析 bug、重构项目

简单来说，它就像一个坐在你旁边的高级程序员，你用自然语言告诉它要做什么，它直接帮你干。

<!-- TODO: 插入 Claude Code 终端界面截图 -->

## Claude Code 能做什么

一些真实的使用场景：

```
> 帮我把这个 Express 项目从 JavaScript 迁移到 TypeScript

> 这个函数有 bug，用户反馈传入空数组时会崩溃，帮我修复并加上单元测试

> 阅读整个项目，给我画一个架构图，用 Mermaid 格式

> 帮我写一个 GitHub Actions CI/CD 配置，要求跑测试、构建 Docker 镜像、推送到 ECR
```

Claude Code 会自动分析你的项目结构，理解上下文，然后一步步执行。它不是简单的代码补全，而是一个能独立完成复杂任务的 AI Agent。

## 安装 Claude Code

### 系统要求

- macOS 10.15+、Ubuntu 20.04+ / Debian 10+、或 Windows（通过 WSL2）
- Node.js 18+（推荐使用原生安装器，无需手动安装 Node）

### 安装命令

**macOS / Linux：**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell：**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD：**

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

安装完成后，在终端输入 `claude` 即可启动。

> ⚠️ 如果你在国内，安装时可能会遇到网络超时。这是因为 `claude.ai` 域名在国内被限制访问。解决方法：使用代理工具，或者通过 npm 安装 `npm install -g @anthropic-ai/claude-code`。

<!-- TODO: 插入安装成功的终端截图 -->

### 验证安装

```bash
claude --version
```

看到版本号就说明安装成功了。

## 官方订阅方案

Claude Code 需要 Anthropic 账号才能使用。官方提供几种方案：

| 方案 | 价格 | 说明 |
|------|------|------|
| Claude Pro | $20/月 | 包含一定量的 Claude Code 使用额度 |
| Claude Max 5x | $100/月 | 5 倍用量 |
| Claude Max 20x | $200/月 | 20 倍用量 |
| API 按量付费 | 按 token 计费 | 通过 `ANTHROPIC_API_KEY` 使用，无月费上限 |

如果你能正常访问 Anthropic 官网、有海外信用卡，直接订阅 Pro 或 Max 是最简单的方式。

## 国内开发者面临的问题

但现实是，大部分国内开发者会遇到这些障碍：

### 1. 网络问题
- `claude.ai` 在国内无法直接访问
- 即使安装成功，运行时也会因为 API 请求被拦截而报错 403
- 使用代理工具不稳定，经常断连

### 2. 注册问题
- Anthropic 注册需要海外手机号接收验证码
- 需要绑定海外信用卡（Visa/Mastercard）
- 部分地区的 IP 直接被 Anthropic 封禁

### 3. 虚拟卡风险
很多人会想到用虚拟信用卡（如 WildCard、Depay 等）来注册。但需要注意：

- ⚠️ Anthropic 对虚拟卡的检测越来越严格
- ⚠️ 使用虚拟卡注册的账号有较高的封号风险（社区反馈约 90% 的封号率）
- ⚠️ 一旦封号，充值的余额无法退回
- ⚠️ 频繁更换 IP 也会触发风控

### 4. 成本问题
- Pro 订阅 $20/月，对于偶尔使用的开发者来说不划算
- Max 订阅 $100-200/月，成本较高
- 按量付费（API）更灵活，但需要解决网络和支付问题

## 替代方案：通过 API 中转使用

对于国内开发者，最稳定、最经济的方式是通过 **API 中转服务** 使用 Claude Code。

原理很简单：Claude Code 支持通过环境变量 `ANTHROPIC_BASE_URL` 自定义 API 地址。你只需要把请求指向一个国内可访问的中转服务，中转服务再转发到 Anthropic 官方 API。

```
你的终端 → 中转服务（国内可达） → Anthropic API（海外）
```

这种方式的优势：
- ✅ 不需要代理工具，国内网络直连
- ✅ 不需要 Anthropic 账号，不用担心封号
- ✅ 按量计费，用多少付多少
- ✅ 中转服务通常对接多个上游供应商，稳定性更好

## 配置 MaxRouter 中转

[MaxRouter](https://www.maxrouter.ai) 是一个 LLM API 聚合平台，对接了 10+ 家上游供应商，支持 80+ 个模型（包括 Claude 全系列、GPT、Gemini、DeepSeek 等）。

选择 MaxRouter 的理由：
- 多供应商冗余，单个供应商出问题会自动切换，不影响使用
- 国内直连，延迟低
- 按量计费，没有月费
- 注册即送 ¥10 体验金，可以先试用
- 支持 Claude Code 原生协议，配置简单

### 第一步：注册账号

访问 [www.maxrouter.ai](https://www.maxrouter.ai) 注册账号。

<!-- TODO: 插入 MaxRouter 注册页面截图 -->

### 第二步：获取 API Key

登录后进入 [控制台 → 令牌管理](https://www.maxrouter.ai/console/tokens)，点击「创建令牌」，复制生成的 API Key（以 `sk-` 开头）。

<!-- TODO: 插入 MaxRouter 令牌管理页面截图 -->

### 第三步：配置环境变量

**macOS / Linux（Zsh）：**

```bash
# 编辑 ~/.zshrc
nano ~/.zshrc

# 在文件末尾添加这两行
export ANTHROPIC_BASE_URL=https://api.maxrouter.ai
export ANTHROPIC_API_KEY=sk-your-key  # 替换为你的实际 Key

# 保存后使配置生效
source ~/.zshrc
```

**macOS / Linux（Bash）：**

```bash
# 编辑 ~/.bashrc
nano ~/.bashrc

# 在文件末尾添加这两行
export ANTHROPIC_BASE_URL=https://api.maxrouter.ai
export ANTHROPIC_API_KEY=sk-your-key

# 保存后使配置生效
source ~/.bashrc
```

**Windows PowerShell（临时）：**

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.maxrouter.ai"
$env:ANTHROPIC_API_KEY = "sk-your-key"
```

**Windows（永久设置）：**

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "https://api.maxrouter.ai", "User")
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-your-key", "User")
# 重启终端后生效
```

> ⚠️ **重要：** `ANTHROPIC_BASE_URL` 设置为 `https://api.maxrouter.ai`，**不要加 `/v1`**。Claude Code 会自动拼接 `/v1/messages` 路径。

### 第四步：启动 Claude Code

```bash
claude
```

如果一切配置正确，你会看到 Claude Code 的欢迎界面，可以开始使用了。

<!-- TODO: 插入 Claude Code 启动成功截图 -->

### 切换模型

MaxRouter 支持所有 Claude 模型，你可以在 Claude Code 中随时切换：

```
/model claude-opus-4          # 最强推理能力，适合复杂任务
/model claude-sonnet-4        # 日常编程首选，性价比高
/model claude-sonnet-4-thinking  # 带思维链，适合复杂调试
/model claude-haiku-4         # 快速响应，适合简单任务
```

## Claude Code 常用命令

启动 Claude Code 后，以下是一些常用的交互方式：

### 基本操作

| 命令 | 说明 |
|------|------|
| `/help` | 查看帮助信息 |
| `/model` | 切换模型 |
| `/compact` | 压缩上下文，节省 token |
| `/clear` | 清除对话历史 |
| `/cost` | 查看当前会话的 token 消耗 |
| `Ctrl+C` | 中断当前操作 |
| `/exit` | 退出 Claude Code |

### 文件操作

直接用自然语言告诉 Claude Code 你要做什么：

```
> 读一下 src/index.ts，告诉我这个文件的作用

> 在 src/utils/ 下创建一个 logger.ts，实现一个简单的日志工具

> 把 src/api/user.ts 里的 fetch 调用改成 axios
```

### Git 操作

```
> 帮我提交当前的修改，commit message 写清楚改了什么

> 创建一个新分支 feature/add-auth，然后切换过去

> 看看最近 5 次提交都改了什么
```

## 实战：用 Claude Code 开发一个项目

来看一个真实的例子 — 用 Claude Code 从零创建一个 Node.js REST API：

```
> 帮我创建一个 Express + TypeScript 项目，包含：
> 1. 用户注册和登录接口（JWT 认证）
> 2. SQLite 数据库
> 3. 输入验证（zod）
> 4. 错误处理中间件
> 5. 单元测试（vitest）
```

Claude Code 会：
1. 初始化项目结构（`package.json`、`tsconfig.json` 等）
2. 安装依赖
3. 创建路由、控制器、模型
4. 编写认证中间件
5. 添加测试用例
6. 运行测试确保通过

整个过程你只需要审查它的操作，确认或拒绝即可。

## 进阶技巧

### 1. 使用 CLAUDE.md 文件

在项目根目录创建 `CLAUDE.md` 文件，写入项目的背景信息、编码规范、架构说明等。Claude Code 每次启动时会自动读取这个文件，相当于给它一个项目说明书。

```markdown
# CLAUDE.md

## 项目简介
这是一个电商后台管理系统，使用 React + TypeScript + Ant Design。

## 编码规范
- 使用函数组件 + Hooks，不用 Class 组件
- 状态管理用 Zustand
- API 请求统一放在 src/api/ 目录
- 组件文件名用 PascalCase

## 常用命令
- `npm run dev` — 启动开发服务器
- `npm run test` — 运行测试
- `npm run build` — 构建生产版本
```

### 2. 使用 /compact 节省 token

长时间对话后，上下文会变得很长，消耗大量 token。使用 `/compact` 命令可以让 Claude Code 压缩历史对话，保留关键信息，减少消耗。

### 3. 多文件操作

Claude Code 擅长跨文件操作。比如：

```
> 我要给所有 API 接口加上请求日志中间件，涉及到的文件都帮我改好
```

它会自动找到所有相关文件，逐一修改。

### 4. 代码审查

```
> 审查 src/services/ 目录下的所有文件，找出潜在的安全问题和性能问题
```

## 其他开发工具配置

MaxRouter 不仅支持 Claude Code，还可以配合其他 AI 编程工具使用：

### Cursor

1. 打开 Cursor 设置 → Models
2. Override OpenAI Base URL: `https://api.maxrouter.ai/v1`
3. API Key: 填入你的 MaxRouter Key
4. 模型选择: `claude-sonnet-4`

### Cline（VS Code 插件）

1. 安装 Cline 插件
2. 设置 → API Provider → OpenAI Compatible
3. Base URL: `https://api.maxrouter.ai/v1`
4. API Key: 填入你的 MaxRouter Key

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

## 常见问题

### Q: Claude Code 报错 403 怎么办？
A: 这是因为 Anthropic 限制了你的 IP 地区。使用 MaxRouter 中转可以解决这个问题，不需要代理工具。

### Q: 安装时网络超时怎么办？
A: 可以通过 npm 安装：`npm install -g @anthropic-ai/claude-code`。如果 npm 也慢，先配置 npm 镜像：`npm config set registry https://registry.npmmirror.com`。

### Q: ANTHROPIC_BASE_URL 要不要加 /v1？
A: **不要加。** 设置为 `https://api.maxrouter.ai` 即可，Claude Code 会自动拼接路径。

### Q: 支持流式输出吗？
A: 支持。Claude Code 默认使用流式输出，MaxRouter 完整支持 SSE 流式传输，体验跟官方一致。

### Q: 数据安全吗？
A: MaxRouter 不存储任何对话内容和代码，请求直接转发到上游 API 供应商。

### Q: 速度怎么样？
A: Claude 模型本身的推理时间通常在几秒到几十秒，网络中转增加的延迟（约 100-300ms）相比之下可以忽略不计。

### Q: 怎么查看用了多少钱？
A: 在 Claude Code 中输入 `/cost` 查看当前会话消耗。也可以登录 [MaxRouter 控制台](https://www.maxrouter.ai/console/overview) 查看详细用量。

### Q: 除了 Claude，还能用什么模型？
A: MaxRouter 支持 80+ 模型，包括 GPT-5、GPT-4o、Gemini 2.5 Pro、DeepSeek、通义千问等。在 Claude Code 之外的场景（如 Cursor、自己的项目），你可以通过同一个 API Key 调用任何模型。

## 相关资源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [MaxRouter 官网](https://www.maxrouter.ai)
- [MaxRouter 完整文档](https://www.maxrouter.ai/docs)
- [MaxRouter 模型列表与价格](https://www.maxrouter.ai/pricing)
- [Anthropic 官方 Claude Code 介绍](https://www.anthropic.com/claude-code)

---

如果这个教程帮到了你，欢迎 ⭐ Star 这个 repo，也欢迎提 Issue 反馈问题或建议。
