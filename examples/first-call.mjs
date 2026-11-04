#!/usr/bin/env node
// Node.js 22+. No dependencies. Does not read local credential files.
import { pathToFileURL } from 'node:url';

const endpoint = 'https://api.maxrouter.ai/v1';

export async function main(args = process.argv.slice(2), {
  env = process.env, fetchImpl = fetch, log = console.log,
} = {}) {
  const send = args.includes('--send');
  if (args.includes('--help')) {
    log('MAXROUTER_API_KEY=... node examples/first-call.mjs [--send --model MODEL_ID]');
    log('Default: list models only. --send: one billable request, no automatic retry.');
    return 0;
  }
  let model;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--send') continue;
    if (args[i] === '--model' && args[i + 1] && !args[i + 1].startsWith('--')) {
      model = args[++i];
    } else {
      log('Invalid arguments. Use --help.');
      return 1;
    }
  }
  if (send && (!model || !/^[a-zA-Z0-9][a-zA-Z0-9._-]*$/.test(model))) {
    log('Pass --model with the exact public model ID from your account.');
    return 1;
  }
  const key = env.MAXROUTER_API_KEY?.trim();
  if (!key) {
    log('Set MAXROUTER_API_KEY in your local environment. Do not post your key.');
    return 1;
  }
  try {
    const response = await fetchImpl(`${endpoint}/${send ? 'chat/completions' : 'models'}`, {
      method: send ? 'POST' : 'GET',
      redirect: 'error',
      signal: AbortSignal.timeout(60_000),
      headers: {
        Authorization: `Bearer ${key}`,
        ...(send ? { 'Content-Type': 'application/json' } : {}),
      },
      ...(send ? { body: JSON.stringify({
        model, messages: [{ role: 'user', content: '只回复：你好' }],
        stream: false, max_tokens: 64,
      }) } : {}),
    });
    if (!response.ok) {
      const hints = {
        400: 'Check the model ID and supported parameters.',
        401: 'Check the key locally; do not paste it into an issue.',
        402: 'Check account balance and billing.',
        403: 'Check key/model permissions.',
        429: 'Wait and check rate limits before retrying manually.',
      };
      log(`HTTP ${response.status}: ${hints[response.status] || 'Check account usage and support before retrying manually.'}`);
      return 1;
    }
    const data = await response.json();
    if (!send) {
      if (!Array.isArray(data.data) || !data.data.every(item => typeof item?.id === 'string')) {
        throw new Error('Invalid model list');
      }
      log(JSON.stringify({ mode: 'models-only', models: data.data.map(item => item.id) }, null, 2));
      return 0;
    }
    const choice = data.choices?.[0];
    if (data.error || !choice || typeof choice.message?.content !== 'string' || !choice.message.content.trim()) {
      throw new Error('Incomplete answer');
    }
    log(JSON.stringify({
      id: data.id, model: data.model, answer: choice.message.content,
      finish_reason: choice.finish_reason ?? null,
      usage: data.usage ?? null,
    }, null, 2));
    if (choice.finish_reason !== 'stop') {
      log('The answer did not finish normally. Check usage before retrying.');
      return 1;
    }
    log('Compare this request with Console → Usage; usage tokens are not a USD charge.');
    return 0;
  } catch {
    log('Request failed, timed out or returned an unexpected response. Not retried. Check account usage before sending again.');
    return 1;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exitCode = await main();
}
