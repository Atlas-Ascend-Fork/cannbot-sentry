# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Shared literal prompt sections; formatting is owned by each caller."""

EVAL_JSON_HEADER = (
    "\n"
    "## Output JSON (ONLY this, no other text)\n"
    "```json\n"
    "{{\n"
    '  "skill_name": "{name}",\n'
    '  "evals": [\n'
    "    {{\n"
    '      "id": 1,\n'
    '      "name": "L1-<category>-<short>",\n'
    '      "level": "L1",\n'
)

EVAL_RATIONALE_RULE = (
    '      "confidence": 0.0-1.0\n'
    "    }}\n"
    "  ]\n"
    "}}\n"
    "```\n"
    "\n"
    "## Rules\n"
    "- Every eval MUST include `rationale`: cite the exact SKILL.md span it tests (section / bullet "
    "/ quoted rule, same language as SKILL.md). `confidence` (0.0-1.0) = how sure you are this eval "
    "cleanly tests that rule (for human review triage).\n"
)

SKILL_SOURCE_SECTION = "\n## Skill\n\nname: {name}\ndescription: {description}\n\n{content}\n"

AGENT_SOURCE_HEADER = "\n## Agent\nname: {name}\ndescription: {description}\n\n## Agent system prompt(角色指令正文)\n"
