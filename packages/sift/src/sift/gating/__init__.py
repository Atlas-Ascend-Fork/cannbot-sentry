# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""gate 判决包(块 C):post-hoc 对 benchmark.json 出 PASS/FAIL/N/A。"""

__all__ = ["AxisVerdict", "GateResult", "evaluate_gate", "parse_delta"]


from sift.gating.models import AxisVerdict, GateResult
from sift.gating.verdict import evaluate_gate, parse_delta
