# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Static analysis engine — runs all checks and produces scorecard."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from sift.models import AnalysisReport, CheckResult, SkillCategory
from sift.parser import parse_skill_md, resolve_skill_dir
from sift.static_analysis.checks import ALL_CHECKS
from sift.static_analysis.classifier import classify_skill


class StaticAnalyzer:
    @staticmethod
    def analyze(skill_path: Path) -> AnalysisReport:
        skill_path = resolve_skill_dir(skill_path)
        name, description, content, frontmatter, body = parse_skill_md(skill_path)

        checks: list[CheckResult] = []
        for check_type, check_fn in ALL_CHECKS:
            if check_type == "frontmatter":
                result = check_fn(frontmatter)
            elif check_type == "content":
                result = check_fn(content)
            elif check_type == "body":
                result = check_fn(body)
            elif check_type == "path":
                result = check_fn(skill_path)
            else:
                continue
            checks.append(result)

        category = classify_skill(body, description)

        return AnalysisReport(
            skill_name=name,
            skill_path=str(skill_path),
            category=category,
            checks=checks,
            score=sum(1 for c in checks if c.passed),
            max_score=len(checks),
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
