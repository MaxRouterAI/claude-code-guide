import test from 'node:test';
import assert from 'node:assert/strict';
import { main } from './first-call.mjs';

function run(args, payload, status = 200, env = { MAXROUTER_API_KEY: 'test-only-key' }) {
  const calls = [], output = [];
  return main(args, {
    env, log: value => output.push(value),
    fetchImpl: async (url, options) => {
      calls.push({ url, ...options });
      return { ok: status >= 200 && status < 300, status, json: async () => payload };
    },
  }).then(code => ({ code, calls, output }));
}

test('default mode only lists models; never posts a generation', async () => {
  const r = await run([], { data: [{ id: 'anthropic-claude-sonnet-5.5' }] });
  assert.equal(r.code, 0);
  assert.equal(r.calls.length, 1);
  assert.equal(r.calls[0].method, 'GET');
  assert.equal(r.calls[0].url, 'https://api.maxrouter.ai/v1/models');
  assert.equal(r.calls[0].redirect, 'error');
  assert.equal(r.calls[0].body, undefined);
  assert.doesNotMatch(r.output.join(''), /test-only-key/);
});

test('missing key, missing model and unknown flags send nothing', async () => {
  for (const args of [['--send'], ['--send', '--model'], ['--send', '--model', 'bad/model'], ['--unknown']]) {
    const r = await run(args, {});
    assert.equal(r.code, 1); assert.equal(r.calls.length, 0);
  }
  const r = await run([], {}, 200, {});
  assert.equal(r.code, 1); assert.equal(r.calls.length, 0);
});

test('help needs neither key nor network', async () => {
  const r = await run(['--help'], {}, 200, {});
  assert.equal(r.code, 0); assert.equal(r.calls.length, 0);
});

test('explicit send makes one bounded request and preserves returned usage', async () => {
  const usage = { prompt_tokens: 10, completion_tokens: 2, total_tokens: 12 };
  const r = await run(['--send', '--model', 'anthropic-claude-sonnet-5.5'], {
    id: 'sample-fixture', model: 'anthropic-claude-sonnet-5.5', usage,
    choices: [{ message: { content: '你好' }, finish_reason: 'stop' }],
  });
  assert.equal(r.code, 0); assert.equal(r.calls.length, 1);
  assert.equal(r.calls[0].method, 'POST');
  const body = JSON.parse(r.calls[0].body);
  assert.equal(body.stream, false); assert.equal(body.max_tokens, 64);
  assert.deepEqual(JSON.parse(r.output[0]).usage, usage);
});

test('HTTP failures never retry or print raw error bodies', async () => {
  for (const status of [400, 401, 402, 403, 429, 500, 503]) {
    const r = await run(['--send', '--model', 'anthropic-claude-sonnet-5.5'], { error: 'private-error-fixture' }, status);
    assert.equal(r.code, 1); assert.equal(r.calls.length, 1);
    assert.doesNotMatch(r.output.join(''), /private-error-fixture|test-only-key/);
  }
});

test('empty and truncated answers are not reported as completed', async () => {
  for (const [content, finish_reason] of [['', 'stop'], ['你好', 'length'], ['你好', null]]) {
    const r = await run(['--send', '--model', 'anthropic-claude-sonnet-5.5'], {
      choices: [{ message: { content }, finish_reason }],
    });
    assert.equal(r.code, 1); assert.equal(r.calls.length, 1);
  }
});

test('network failure sends once and does not expose exception details', async () => {
  let calls = 0; const output = [];
  const code = await main([], {
    env: { MAXROUTER_API_KEY: 'test-only-key' }, log: value => output.push(value),
    fetchImpl: async () => { calls++; throw new Error('private-error-fixture'); },
  });
  assert.equal(code, 1); assert.equal(calls, 1);
  assert.doesNotMatch(output.join(''), /private-error-fixture|test-only-key/);
});
