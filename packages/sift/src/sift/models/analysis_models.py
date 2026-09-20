# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Analysis models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AnalysisImprovementSuggestion(BaseModel):
    priority: str = "medium"
    category: str = ""
    suggestion: str = ""
    expected_impact: str = ""


class AnalysisInstructionFollowing(BaseModel):
    score: int | None = None
    issues: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    winner_strengths: list[str] = Field(default_factory=list)
    loser_weaknesses: list[str] = Field(default_factory=list)
    instruction_following: dict[str, AnalysisInstructionFollowing] = Field(default_factory=dict)
    improvement_suggestions: list[AnalysisImprovementSuggestion] = Field(default_factory=list)
    transcript_insights: dict[str, str] = Field(default_factory=dict)
