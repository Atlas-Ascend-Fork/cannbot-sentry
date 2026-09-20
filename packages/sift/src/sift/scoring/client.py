# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.


"""Shared model-call boundary for scoring components."""

from __future__ import annotations

from dataclasses import dataclass

from sift.concurrency import LLMRetryExhausted, call_llm_with_retry


@dataclass
class ScoringClient:
    """执行带重试的评分请求，耗尽后返回空结果供各评分器按领域规则降级。"""

    model: str | None = None
    timeout: int = 120
    default_schema: dict | None = None

    def complete(self, prompt: str, *, on_usage=None, schema=None) -> str:
        try:
            return call_llm_with_retry(
                prompt,
                model=self.model,
                timeout=self.timeout,
                schema=self.default_schema if schema is None else schema,
                on_usage=on_usage,
                transport="http",
            )
        except LLMRetryExhausted:
            return ""
