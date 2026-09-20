# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""执行层发布的具名进度事件，终端渲染器和其他消费者共用。"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProgressUpdate:
    """一次进度通知中的执行信息和完成计数。"""

    eval_name: str
    config_name: str
    eval_idx: int
    total_evals: int
    completed: int
    total: int
    grading: Any
    run_duration: float = 0.0
    run_output: Any = None
    phase: str = ""
    substep: str = ""
