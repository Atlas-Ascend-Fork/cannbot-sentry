// Copyright (c) 2026 Huawei Technologies Co., Ltd.
// This program is free software, you can redistribute it and/or modify it under the terms and conditions of
// CANN Open Software License Agreement Version 2.0 (the "License").
// Please refer to the License for details. You may not use this file except in compliance with the License.
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
// See LICENSE in the root of the software repository for the full text of the License.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { describe, it, expect } from 'vitest';
import { createReassembler } from '../../src/stream-reassembler.ts';
import { redactRecord } from '../../src/redactor.ts';
import type { ProxyRecord } from '../../src/types.ts';
import { appendClaudeLine } from '../../src/writer.ts';

const credentialForms = JSON.parse(fs.readFileSync(
  new URL('../data/tool-output-credential-forms.json', import.meta.url), 'utf8'
)).forms;

function reassemble(events: object[], width: number, newline = '\n') {
  const wire = events.map(e => `data: ${JSON.stringify(e)}${newline}${newline}`).join('');
  const reassembler = createReassembler('anthropic');
  for (let offset = 0; offset < wire.length; offset += width) {
    reassembler.feed(wire.slice(offset, offset + width));
  }
  return reassembler.result();
}

const payloads = [
  { type: 'web_search_tool_result', content: [{ type: 'web_search_result', title: '合成参考', encrypted_content: 'synthetic' }] },
  { type: 'tool_search_tool_result', content: { type: 'tool_search_tool_search_result', tool_references: [{ type: 'tool_reference', tool_name: 'fixture' }] } },
  { type: 'bash_code_execution_tool_result', content: { type: 'bash_code_execution_result', stdout: '合成输出', stderr: '', return_code: 0, content: [] } },
  { type: 'web_search_tool_result', content: { type: 'web_search_tool_result_error', error_code: 'max_uses_exceeded' } },
  { type: 'web_search_tool_result', content: [] },
  { type: 'tool_result', content: '' },
];

describe.each([1, 7, 10000])('Anthropic start payloads, chunk width %i', width => {

  it.each(['tool_use', 'server_tool_use'].flatMap(type =>
    [null, 0, false, [], ''].map(input => ({ type, input }))
  ))('omits invalid initial input for $type: $input', ({ type, input }) => {
    const result = reassemble([
      { type: 'content_block_start', index: 0, content_block: { type, id: 'fixture', name: 'fixture', input } },
      { type: 'content_block_stop', index: 0 },
    ], width);
    expect(result.content).toEqual([{ type, id: 'fixture', name: 'fixture' }]);
  });

  it.each(['web_search_tool_result', 'bash_code_execution_tool_result', 'tool_search_tool_result', 'tool_result'].flatMap(type =>
    [null, 0, false].map(content => ({ type, content }))
  ))('omits invalid initial content for $type: $content', ({ type, content }) => {
    const result = reassemble([
      { type: 'content_block_start', index: 0, content_block: { type, tool_use_id: 'fixture', content } },
      { type: 'content_block_stop', index: 0 },
    ], width);
    expect(result.content).toEqual([{ type, tool_use_id: 'fixture' }]);
  });

  it.each(credentialForms)('redacts $name through reassembly, record and capture file', form => {
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'cpx-tool-credential-fixture-'));
    try {
      const content = {
        type: 'bash_code_execution_result', stdout: 'ordinary output',
        stderr: 'ordinary error', return_code: 7, content: [],
      };
      content[form.field as 'stdout' | 'stderr'] = form.value;
      const result = reassemble([
        { type: 'content_block_start', index: 0, content_block: {
          type: 'bash_code_execution_tool_result', tool_use_id: 'fixture', content,
        } },
        { type: 'content_block_stop', index: 0 },
      ], width);
      const record = { request: { path: '', body: {} }, response: { content: result.content } } as ProxyRecord;
      redactRecord(record);
      const file = path.join(directory, 'capture.jsonl');
      appendClaudeLine(file, { type: 'assistant', message: { role: 'assistant', content: record.response.content } });
      const text = fs.readFileSync(file, 'utf8');
      const saved = JSON.parse(text).message.content[0].content;
      expect(saved[form.field]).toBe(form.expected);
      expect(saved[form.field === 'stdout' ? 'stderr' : 'stdout']).toBe(form.field === 'stdout' ? 'ordinary error' : 'ordinary output');
      expect(saved.return_code).toBe(7);
      expect(saved.content).toEqual([]);
      if (form.secret) expect(text).not.toContain(form.secret);
      const once = JSON.stringify(record);
      redactRecord(record);
      expect(JSON.stringify(record)).toBe(once);
    } finally {
      fs.rmSync(directory, { recursive: true, force: true });
    }
  });

  it.each(payloads.flatMap(block => ['\n', '\r\n'].map(newline => ({ block, newline }))))(
    'preserves $block.type contents with newline $newline', ({ block, newline }) => {
      const expected = { ...block, tool_use_id: 'srvtoolu_fixture' };
      const result = reassemble([
        { type: 'content_block_start', index: 0, content_block: expected },
        { type: 'content_block_stop', index: 0 },
      ], width, newline);
      expect(result.content).toEqual([expected]);
    }
  );

  it.each(['tool_use', 'server_tool_use'].flatMap(type => [
    { type, input: {} }, { type, input: { query: 'synthetic query' } },
  ]))('keeps the initial $type input', ({ type, input }) => {
    const block = { type, id: 'tool_fixture', name: 'fixture', input };
    const result = reassemble([
      { type: 'content_block_start', index: 0, content_block: block },
      { type: 'content_block_stop', index: 0 },
    ], width);
    expect(result.content).toEqual([block]);
  });

  it.each([
    { partial: '{"query":"streamed"}', expected: { query: 'streamed' } },
    { partial: '{invalid', expected: { _raw: '{invalid' } },
  ])('retains parsed/raw JSON delta priority: $partial', ({ partial, expected }) => {
    const result = reassemble([
      { type: 'content_block_start', index: 0, content_block: { type: 'tool_use', input: { old: true } } },
      { type: 'content_block_delta', index: 0, delta: { type: 'input_json_delta', partial_json: partial } },
      { type: 'content_block_stop', index: 0 },
    ], width);
    expect(result.content[0].input).toEqual(expected);
  });

  it('preserves mixed block ordering, text/thinking deltas and usage', () => {
    const result = reassemble([
      { type: 'message_start', message: { model: 'fixture-model', usage: { input_tokens: 10 } } },
      { type: 'content_block_start', index: 3, content_block: { type: 'web_search_tool_result', tool_use_id: 'tool_fixture', content: [] } },
      { type: 'content_block_start', index: 0, content_block: { type: 'text', text: 'initial ' } },
      { type: 'content_block_delta', index: 0, delta: { type: 'text_delta', text: 'text' } },
      { type: 'content_block_start', index: 1, content_block: { type: 'thinking', thinking: 'initial ' } },
      { type: 'content_block_delta', index: 1, delta: { type: 'thinking_delta', thinking: 'thought' } },
      { type: 'content_block_start', index: 2, content_block: { type: 'server_tool_use', id: 'tool_fixture', name: 'fixture', input: {} } },
      { type: 'message_delta', delta: { stop_reason: 'end_turn' }, usage: { output_tokens: 4 } },
    ], width);
    expect(result.content).toEqual([
      { type: 'text', text: 'initial text' },
      { type: 'thinking', thinking: 'initial thought' },
      { type: 'server_tool_use', id: 'tool_fixture', name: 'fixture', input: {} },
      { type: 'web_search_tool_result', tool_use_id: 'tool_fixture', content: [] },
    ]);
    expect(result.usage).toMatchObject({ input_tokens: 10, output_tokens: 4 });
    expect(result.model).toBe('fixture-model');
    expect(result.stop_reason).toBe('end_turn');
    expect(result.firstTokenAt).toBeTypeOf('number');
  });

  it('passes preserved payloads through the real record redactor', () => {
    const synthetic = ['synthetic', 'capture', 'credential'].join('-');
    const result = reassemble([
      { type: 'content_block_start', index: 0, content_block: {
        type: 'web_search_tool_result', tool_use_id: 'tool_fixture',
        content: [{ title: '合成参考', metadata: { api_key: synthetic } }],
      } },
      { type: 'content_block_stop', index: 0 },
    ], width);
    const record = { request: { path: '', body: {} }, response: { content: result.content } } as ProxyRecord;
    redactRecord(record);
    expect(record.response.content).toEqual([
      { type: 'web_search_tool_result', tool_use_id: 'tool_fixture', content: [
        { title: '合成参考', metadata: { api_key: 'synt…tial' } },
      ] },
    ]);
    expect(JSON.stringify(record)).not.toContain(synthetic);
  });
});
