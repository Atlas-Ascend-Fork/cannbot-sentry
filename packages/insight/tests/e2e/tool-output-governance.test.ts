// Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
// This program is free software: you can redistribute it and/or modify it under the terms and conditions of
// CANN Open Software License Agreement Version 2.0 (the "License").
// Please refer to the License for details. You may not use this file except in compliance with the License.
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
// See LICENSE in the root of the software repository for the full text of the License.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { describe, expect, it } from 'vitest';
import { governText } from '@/lib/lake/governance';
import { redactRecord } from '../../../cpx/src/redactor';
import type { ProxyRecord } from '../../../cpx/src/types';

const fixture = JSON.parse(fs.readFileSync(
  new URL('../data/tool-output-credential-forms.json', import.meta.url), 'utf8'
));

describe('tool output capture governance at the staging file boundary', () => {
  it('masks URI and existing credential forms with no residue and preserves ordinary output', () => {
    expect(fixture.synthetic_only).toBe(true);
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'insight-tool-governance-fixture-'));
    try {
      for (const form of fixture.forms) {
        const content = {
          type: 'bash_code_execution_result', stdout: 'ordinary output',
          stderr: 'ordinary error', return_code: 7, content: [],
        };
        content[form.field as 'stdout' | 'stderr'] = form.value;
        const block = { type: 'bash_code_execution_tool_result', tool_use_id: 'fixture', content };
        const raw = JSON.stringify({ type: 'assistant', message: { role: 'assistant', content: [block] } }) + '\n';
        const source = path.join(directory, form.name + '-source.jsonl');
        const staged = path.join(directory, form.name + '-staged.jsonl');
        fs.writeFileSync(source, raw);
        const governed = governText(fs.readFileSync(source, 'utf8'));
        expect(governed.residue, form.name).toEqual([]);
        fs.writeFileSync(staged, governed.output);
        expect(fs.readFileSync(source, 'utf8')).toBe(raw);
        const saved = JSON.parse(fs.readFileSync(staged, 'utf8')).message.content;
        expect(saved[0].content[form.field], form.name).toBe(form.expected);
        expect(saved[0].content.return_code).toBe(7);
        expect(saved[0].content.content).toEqual([]);
        if (form.secret) expect(governed.output).not.toContain(form.secret);
        const record = { request: { path: '', body: {} }, response: { content: [block] } } as ProxyRecord;
        redactRecord(record);
        expect(saved).toEqual(record.response.content);
        expect(governText(governed.output)).toEqual(governed);
      }
    } finally {
      fs.rmSync(directory, { recursive: true, force: true });
    }
  });
});
