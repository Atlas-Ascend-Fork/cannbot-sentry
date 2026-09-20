# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Custom exceptions and error codes for sift."""

from __future__ import annotations


class SiftError(Exception):
    exit_code: int = 1


class InputError(SiftError):
    exit_code: int = 2


class ExecutionError(SiftError):
    exit_code: int = 3


class SkillParseError(InputError):
    pass


class EvalValidationError(InputError):
    pass


class ManifestError(InputError):
    pass


class CyclicDependencyError(InputError):
    pass


class ClaudeRunnerError(ExecutionError):
    pass


class ScoringError(ExecutionError):
    pass


class ComplianceError(ExecutionError):
    pass


class CalibrationError(ExecutionError):
    pass


class ReportError(ExecutionError):
    pass


class OpencodeDbError(ExecutionError):
    """opencode .db → export 流程失败(binary 缺失 / 非零退出 / 超时 / 无 session / id 不匹配)。"""

    pass
