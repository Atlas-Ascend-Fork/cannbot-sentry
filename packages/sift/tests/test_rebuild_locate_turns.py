# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""rebuild 的 locate_turns 开关:[T{idx}] 前缀 + ToolCallRecord.turn 的渲染控制。"""

from pathlib import Path

from sift.audit.rebuild import rebuild


def _write_cc_jsonl(tmp_path: Path) -> Path:
    # assistant record 带 tool_use(配 tool_result)→ tool_trace 非空,
    # 使 test_locate_turns_off_no_prefix 的 `all(t.turn is None ...)` 真 non-vacuous
    # (否则 text-only fixture 让 tool_trace 恒空、断言永真,没验到 locate_turns=False
    # 时 ToolCallRecord.turn=None 的行为)。
    p = tmp_path / "t.jsonl"
    p.write_text(
        '{"type":"user","message":{"role":"user","content":"hi"},"parent_tool_use_id":null}\n'
        '{"type":"assistant","message":{"role":"assistant","content":['
        '{"type":"text","text":"do X"},'
        '{"type":"tool_use","name":"Read","input":{"file_path":"x"},"id":"t1"}'
        "]}}\n"
        '{"type":"user","message":{"role":"user","content":['
        '{"type":"tool_result","tool_use_id":"t1","content":"x-content"}'
        "]}}\n",
        encoding="utf-8",
    )
    return p


def test_locate_turns_off_no_prefix(tmp_path):
    tp = _write_cc_jsonl(tmp_path)
    _trace, text, digest = rebuild(tp, locate_turns=False)
    assert "[T" not in text
    assert all(t.turn is None for t in digest.tool_trace)


def test_locate_turns_on_has_prefix(tmp_path):
    tp = _write_cc_jsonl(tmp_path)
    _trace, text, _digest = rebuild(tp, locate_turns=True)
    # user record 占 turn 1,assistant 占 turn 2 → 前缀 [T2](stamp 按全体 record 位置)。
    assert "[T2]" in text


def test_locate_turns_default_off(tmp_path):
    tp = _write_cc_jsonl(tmp_path)
    _trace, text, _digest = rebuild(tp)
    assert "[T" not in text
