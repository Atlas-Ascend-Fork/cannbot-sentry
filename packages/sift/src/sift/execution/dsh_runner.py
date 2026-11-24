# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""DeepSeek Harness headless executor.

The runner drives ``dsh --profile <profile> --json -`` and projects the NDJSON
events into SIFT's ``RunOutput`` contract. DSH owns the agent loop and tool
execution; SIFT only supplies the non-interactive task prompt and consumes the
resulting evidence.
"""

from __future__ import annotations

import dataclasses
import json
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path

from sift.errors import DshRunnerError
from sift.evals.transcript import _norm_tool
from sift.execution.cli_runner import build_live_prompt
from sift.execution.options import ExecutionOptions
from sift.models import RunOutput, ToolCallRecord
from sift.parser import parse_skill_md


def _dsh_binary() -> str:
    return os.environ.get("SIFT_DSH_BIN", "dsh")


def _dsh_profile() -> str:
    return os.environ.get("SIFT_DSH_PROFILE", "headless")


def _agent_prompt(prompt: str, agent_path: Path) -> str:
    name, _description, _content, _refs, body = parse_skill_md(agent_path)
    return (
        f"You are the following Agent declaration. Follow it for the task below.\n\n"
        f'<agent name="{name}">\n{body}\n</agent>\n\n'
        "<non_interactive_mode>\n"
        "This is a NON-INTERACTIVE automated evaluation. Execute the task end-to-end. "
        "When user input is required, state a reasonable assumption and continue. "
        "Do not fabricate data that is absent from the workspace.\n"
        "</non_interactive_mode>\n\n---\n\n"
        f"{prompt}"
    )


def _usage_tokens(usage: object) -> int:
    if not isinstance(usage, dict):
        return 0
    total = usage.get("totalTokens")
    if isinstance(total, int) and total > 0:
        return total
    return sum(
        int(usage.get(key) or 0)
        for key in ("inputTokens", "outputTokens", "cacheReadTokens", "cacheWriteTokens", "reasoningTokens")
    )


@dataclasses.dataclass
class _DshEvents:
    """NDJSON 事件流的归集状态（_parse_events 的可变收集器）。"""

    texts: list[str] = dataclasses.field(default_factory=list)
    final_text: str = ""
    stop_reason: str = ""
    error_message: str = ""
    total_tokens: int = 0
    max_turn: int = 0
    tool_calls: dict[str, int] = dataclasses.field(default_factory=dict)
    trace: list[ToolCallRecord] = dataclasses.field(default_factory=list)
    by_call_id: dict[str, ToolCallRecord] = dataclasses.field(default_factory=dict)


def _iter_dsh_events(stdout: str):
    """逐行解析 NDJSON；空行 / 畸形行 / 非对象行静默跳过。"""
    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            yield event


def _parse_events(stdout: str) -> RunOutput:
    state = _DshEvents()
    for event in _iter_dsh_events(stdout):
        _apply_dsh_event(event, state)
    transcript = "\n".join(part for part in state.texts if part.strip())
    result_text = state.final_text or (state.texts[-1] if state.texts else "")
    return RunOutput(
        exit_code=0,
        stdout=stdout,
        total_tokens=state.total_tokens,
        transcript=transcript,
        tool_calls=state.tool_calls,
        tool_trace=state.trace,
        result_text=result_text,
        num_turns=state.max_turn,
        stop_reason=state.stop_reason or state.error_message,
    )


def _apply_dsh_event(event: dict, state: _DshEvents) -> None:
    """按事件类型分派给对应的归集器。"""
    event_type = event.get("type")
    if event_type == "status":
        _apply_status_event(event, state)
        return
    if event_type == "text" and isinstance(event.get("text"), str):
        state.texts.append(event["text"])
        return
    if event_type == "tool_call":
        _apply_tool_call_event(event, state)
        return
    if event_type == "tool_result":
        _apply_tool_result_event(event, state)
        return
    if event_type == "final":
        value = event.get("text")
        if isinstance(value, str):
            state.final_text = value
        return
    if event_type == "error":
        value = event.get("message")
        if isinstance(value, str):
            state.error_message = value


def _apply_status_event(event: dict, state: _DshEvents) -> None:
    turn = event.get("turn")
    if isinstance(turn, int):
        state.max_turn = max(state.max_turn, turn)
    if event.get("phase") == "step_end":
        state.total_tokens += _usage_tokens(event.get("usage"))
    if event.get("phase") == "turn_end":
        _apply_turn_end_reason(event.get("reason"), state)


def _apply_turn_end_reason(reason: object, state: _DshEvents) -> None:
    if isinstance(reason, dict):
        state.stop_reason = str(reason.get("kind") or reason.get("reason") or "")
    elif reason:
        state.stop_reason = str(reason)


def _apply_tool_call_event(event: dict, state: _DshEvents) -> None:
    name = _norm_tool(str(event.get("tool") or ""))
    call_id = str(event.get("callId") or "")
    value = event.get("input")
    record = ToolCallRecord(
        name=name,
        input_summary=json.dumps(value, ensure_ascii=False)[:200] if value is not None else "",
        input=value if isinstance(value, dict) else None,
        tool_use_id=call_id or None,
        session_id=str(event.get("sessionId") or "") or None,
    )
    state.trace.append(record)
    if call_id:
        state.by_call_id[call_id] = record
    state.tool_calls[name] = state.tool_calls.get(name, 0) + 1


def _apply_tool_result_event(event: dict, state: _DshEvents) -> None:
    record = state.by_call_id.get(str(event.get("callId") or ""))
    if record is not None:
        record.result = event.get("result")
        record.is_error = event.get("status") == "error"
        record.succeeded = not record.is_error


class DshRunner:
    """Run one non-interactive task through a DSH headless profile."""

    @staticmethod
    def complete(prompt: str, options: ExecutionOptions = ExecutionOptions()) -> RunOutput:
        """Run one plain prompt without injecting a Skill body."""
        return DshRunner._run_prompt(prompt, options)

    @staticmethod
    def run(prompt: str, skill_path: Path | None = None, options: ExecutionOptions = ExecutionOptions()) -> RunOutput:
        return DshRunner._run_prompt(build_live_prompt(prompt, skill_path), options)

    @staticmethod
    def run_trigger(
        prompt: str,
        cwd: Path | str,
        env: dict,
        options: ExecutionOptions = ExecutionOptions(),
    ) -> RunOutput:
        """Run a raw trigger probe without injecting the skill body."""
        trigger_options = options._replace(cwd=Path(cwd))
        return DshRunner._run_prompt(prompt, trigger_options, env=env)

    @staticmethod
    def run_agent(
        prompt: str,
        agent_path: Path,
        options: ExecutionOptions = ExecutionOptions(),
    ) -> RunOutput:
        return DshRunner._run_prompt(_agent_prompt(prompt, agent_path), options)

    @staticmethod
    def _run_prompt(prompt: str, options: ExecutionOptions, env: dict | None = None) -> RunOutput:
        binary = _dsh_binary()
        if shutil.which(binary) is None:
            raise DshRunnerError(
                f"dsh CLI not found ({binary}); install DSH or set SIFT_DSH_BIN"
            )
        profile = _dsh_profile()
        if options.on_progress:
            options.on_progress(f"▶ dsh profile={profile}")
        started = time.perf_counter()
        stdout, stderr, timed_out, returncode = _spawn_dsh(prompt, binary, profile, options, env)
        duration_ms = int((time.perf_counter() - started) * 1000)
        parsed = _parse_events(stdout)
        _attach_task_event(parsed, stdout, prompt)
        parsed.duration_ms = duration_ms
        if timed_out:
            parsed.exit_code = -1
            parsed.stop_reason = f"timed_out_after_{options.timeout}s"
            if not stdout.strip():
                raise DshRunnerError(f"dsh headless timed out after {options.timeout}s")
            return parsed
        _apply_exit_status(parsed, stdout, stderr, returncode)
        if options.on_progress:
            options.on_progress(
                f"  dsh done: {parsed.num_turns} turns · {parsed.total_tokens} tokens · {parsed.stop_reason}"
            )
        return parsed


def _spawn_dsh(
    prompt: str,
    binary: str,
    profile: str,
    options: ExecutionOptions,
    env: dict | None,
) -> tuple[str, str, bool, int | None]:
    """spawn dsh 子进程并收满 stdout/stderr；超时杀整组并按超时路径收尾。

    返回 (stdout, stderr, timed_out, returncode)。
    """
    cwd = options.cwd or Path.cwd()
    command = [binary, "--profile", profile, "--json", "-"]
    proc = subprocess.Popen(
        command,
        cwd=cwd,
        env=dict(env) if env is not None else os.environ.copy(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(prompt, timeout=options.timeout)
        return stdout, stderr, False, proc.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = proc.communicate()
        return stdout, stderr, timed_out, proc.returncode


def _attach_task_event(parsed: RunOutput, stdout: str, prompt: str) -> None:
    # Keep the task in SIFT's persisted transcript envelope so audit/rebuild
    # can reconstruct a user turn. DSH itself does not emit the submitted task.
    task_event = json.dumps({"type": "task", "text": prompt}, ensure_ascii=False)
    parsed.stdout = f"{task_event}\n{stdout}" if stdout else f"{task_event}\n"


def _apply_exit_status(parsed: RunOutput, stdout: str, stderr: str, returncode: int | None) -> None:
    parsed.exit_code = returncode if returncode is not None else -1
    if parsed.exit_code != 0:
        if not stdout.strip():
            raise DshRunnerError(f"dsh headless exited with code {parsed.exit_code}: {stderr[:500]}")
        parsed.stop_reason = parsed.stop_reason or f"exit_{parsed.exit_code}"
    elif not parsed.stop_reason:
        parsed.stop_reason = "completed"
