# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Shared test fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_SKILL_DIR = FIXTURES_DIR / "sample-skill"


@pytest.fixture
def sample_skill_path() -> Path:
    return SAMPLE_SKILL_DIR


@pytest.fixture
def sample_evals_path() -> Path:
    return FIXTURES_DIR / "sample-evals.json"


@pytest.fixture
def sample_evals_data() -> dict:
    return json.loads((FIXTURES_DIR / "sample-evals.json").read_text(encoding="utf-8"))


@pytest.fixture
def sample_grading_data() -> dict:
    return json.loads((FIXTURES_DIR / "sample-grading.json").read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def _isolate_refine_cache_dir(monkeypatch, tmp_path):
    """所有测试的 refine 缓存目录指向 tmp_path,绝不污染 ``~/.cache/sift/refine/``。

    ``audit.refine_cache`` 跨 audit() 调用复用 LLM refine 结果,落盘到
    ``~/.cache/sift/refine/``。任何走 ``audit()``(直接或经 CLI/pipeline)
    的测试都会触缓存写——必须 function-scoped 隔离,否则:① 污染用户 home;
    ② 同 instructions 的测试跨 run 撞缓存,后者变 hit 而期望 miss 的断言失真。
    """
    from sift.audit import refine_cache

    monkeypatch.setattr(refine_cache, "_cache_dir", lambda: tmp_path)


@pytest.fixture
def no_llm_retry_wait(monkeypatch) -> None:
    """仅由明确选择它的测试关闭重试退避，不影响并发计时测试。"""
    monkeypatch.setattr("sift.audit.auditor.time.sleep", lambda *args, **kwargs: None)
