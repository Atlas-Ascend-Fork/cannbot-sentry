# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Typed source and evidence records shared by audit test factories."""

from typing import NamedTuple

from sift.models.audit_models import AuditCategory, AuditMethod


class FindingOrigin(NamedTuple):
    source: str = "CONSTRAINT"
    category: AuditCategory = AuditCategory.PROHIBITION
    seq: int = 0
    section: str = ""
    derived: bool = False
    control_flow: str = ""
    excerpt: str = ""
    synthetic: bool = False


class FindingEvidence(NamedTuple):
    method: AuditMethod = AuditMethod.PROGRAMMATIC
    text: str = "e"
    related: list[str] | None = None


class ScoringRates(NamedTuple):
    programmatic: float | None = None
    llm: float | None = None
