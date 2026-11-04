# 从拿到 Key 到核对第一笔用量

修订日期：2026-11-04。本文由 MaxRouter 运营方维护。适合已有 Node.js 22 或更新版本、希望先验证 API 再配置编程工具的开发者。

目标是完成三个可核对的步骤：查到自己能用的模型、收到一条正常结束的回答、在控制台找到这次调用。示例不安装依赖，不改 Claude Code 配置，也不自动重试。

## 1. 创建自己的 API Key

从 [MaxRouter 接入文档](https://www.maxrouter.ai/docs?utm_source=github&utm_medium=readme&utm_campaign=first_call_202611&utm_content=api_quickstart) 进入账户，打开控制台的“密钥管理”，创建只供自己使用的 Key。试用额度和模型权限以账户当时展示为准。

在本教程所在仓库的根目录打开一个 Bash/Zsh 终端，运行：

```bash
node --version
read -r -s -p 'MaxRouter API Key: ' MAXROUTER_API_KEY
printf '\n'
export MAXROUTER_API_KEY
```

上面的 `read` 命令适用于 Bash；Zsh 使用：

```zsh
read -r -s 'MAXROUTER_API_KEY?MaxRouter API Key: '
printf '\n'
export MAXROUTER_API_KEY
```

输入不会显示在终端，也不会把真实 Key 写进命令历史。不要把 Key 发到 Issue 或截图里。

Windows PowerShell 可以使用安全输入，再将值转换给当前进程：

```powershell
$secure = Read-Host 'MaxRouter API Key' -AsSecureString
$env:MAXROUTER_API_KEY = [System.Net.NetworkCredential]::new('', $secure).Password
```

这些设置只影响当前终端及其子进程；关闭终端后不会作为持久配置保留。

## 2. 先查模型，不生成回答

```bash
node examples/first-call.mjs
```

默认只发送一次 `GET https://api.maxrouter.ai/v1/models`，不发送模型生成请求。响应里应有 `mode: "models-only"` 和可用模型 ID 列表。账户模型权限可能与公开目录不同。

从返回列表复制一个精确的公开 ID。2026-11-04 核对公开目录时，包含 `anthropic-claude-sonnet-5.5` 和 `anthropic-claude-opus-5.5`；这不是账户一定有权限的承诺，也不要自行把显示名称拼成 ID。

## 3. 明确发送一条测试消息

这一步会产生模型调用费用。确认账户余额和模型价格后，才执行：

```bash
node examples/first-call.mjs --send --model anthropic-claude-sonnet-5.5
```

如果上一步没有这个 ID，改为账户列表中支持文本 Chat Completions 的模型 ID。

程序只发送一次 `POST /v1/chat/completions`，内容是“只回复：你好”，设置 `stream: false`、`max_tokens: 64`，60 秒超时，不自动重试。这个输出上限不是美元费用上限；历史输入、模型价格和模型自身行为仍会影响费用。

程序会展示本次返回的 `id`、`model`、`answer`、`finish_reason` 和 `usage`，不会打印 Key。以下是字段示意，不是真实测试回包，也不是 token 数量承诺：

```json
{
  "id": "本次响应ID",
  "model": "账户使用的公开模型ID",
  "answer": "你好",
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": "接口返回的输入数量",
    "completion_tokens": "接口返回的输出数量",
    "total_tokens": "接口返回的合计数量"
  }
}
```

真实 token 字段是数值；上面用说明文字避免把虚构数字当作实际结果。模型不一定严格只回复两个字。程序遇到空回答或非 `stop` 结束会返回失败状态，避免把不完整回答当成功。

## 4. 去控制台核对

打开 [控制台 → 使用记录](https://www.maxrouter.ai/console/usage)，用调用时间和模型找到这笔记录。核对输入、输出、缓存数量和实际扣费；记录入库可能稍有延迟。

`usage` 是用量，不是扣费美元数；CLI 的统计也不能替代账户账单。实际账单以使用记录为准。余额和费用显示六位小数，小额测试也能看出变化。

失败或超时后，先查有没有调用记录，再决定是否手动重试，避免重复付费。

## 5. API 成功后再配置 Claude Code

Claude Code CLI 的网关地址与 OpenAI 兼容 SDK 的 `baseURL` 不同：

| 用途 | 地址 |
|---|---|
| 本示例的 Chat Completions API | `https://api.maxrouter.ai/v1/chat/completions` |
| OpenAI 兼容 SDK 的 baseURL | `https://api.maxrouter.ai/v1` |
| Claude Code CLI 的 ANTHROPIC_BASE_URL | `https://api.maxrouter.ai` |

MaxRouter 现行文档使用 `ANTHROPIC_API_KEY` 认证。先在当前终端核对现有网关配置；若还设置了其他服务的 `ANTHROPIC_AUTH_TOKEN` 或设置文件中的 `env`，不要同时混用。完成后可以单独在测试终端执行：

```bash
export ANTHROPIC_BASE_URL=https://api.maxrouter.ai
export ANTHROPIC_API_KEY="$MAXROUTER_API_KEY"
claude --model anthropic-claude-sonnet-5.5
```

在 `/status` 私下确认地址和凭据来源，再做一次小任务。Chat Completions 成功不等于 Claude Code 的 Messages、工具调用和所有功能均通过验收。其他客户端也要按各自配置说明接入。

网关认证的现行规则可查阅 [Claude Code 官方接入文档](https://code.claude.com/docs/en/llm-gateway-connect)。

## 常见失败怎么处理

| 现象 | 下一步 |
|---|---|
| 401 | 私下核对 Key、是否有多余空格、是否过期；不要把 Key 发出来 |
| 403 | 核对账户和模型权限，不反复重试 |
| 400 / 找不到模型 | 从账户 `/v1/models` 复制 ID，核对模型支持的请求类型 |
| 余额不足 | 查看账户余额、密钥额度和使用记录 |
| 429 | 降低请求频率，等候后再决定是否手动重试 |
| 超时、服务错误、回答不完整 | 先查使用记录，保留时间、模型及脱敏错误，再联系支持 |

反馈时只提供时间、客户端版本、公开模型 ID 和脱敏错误。不得公开 Key、完整账单、私人对话或项目源码。

## 示例的验证范围

本次维护验证了示例的离线请求格式、默认不生成、显式发送一次、错误不重试以及不打印 Key；没有用本教程新增真实生成调用，也没有据此宣称全部客户端兼容。运行离线测试：

```bash
node --test examples/first-call.test.mjs
```
