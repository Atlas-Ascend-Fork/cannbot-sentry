# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Explicit legacy payloads and minimal reports shared by compatibility tests."""

from sift.models import audit_models


def legacy_instruction_aggregate(text):
    return {
        "instruction_text": text,
        "source": "CONSTRAINT",
        "category": "prohibition",
        "pass_count": 1,
        "fail_count": 0,
        "na_count": 0,
        "total": 1,
        "fail_rate": 0.0,
        "fail_in_transcripts": [],
    }


def root_audit_report(text):
    return audit_models.AuditReport(
        skill_name="wf",
        transcripts=["slice.jsonl"],
        summary={"total": 1, "pass": 1, "fail": 0, "na": 0},
        findings=[
            audit_models.AuditFinding(
                instruction_text=text,
                source="HEADING_STEP",
                verdict=audit_models.AuditVerdict.PASS,
                category=audit_models.AuditCategory.STEP,
                evidence="ok",
                method=audit_models.AuditMethod.LLM,
                transcript="slice.jsonl",
            )
        ],
        warnings=[],
    )
