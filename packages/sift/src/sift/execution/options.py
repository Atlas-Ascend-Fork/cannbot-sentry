# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""执行器共享的运行配置；技能和 agent 的注入方式仍由各入口决定。"""

from pathlib import Path
from typing import Callable, NamedTuple


class ExecutionOptions(NamedTuple):
    model: str | None = None
    timeout: int = 120
    cwd: Path | None = None
    max_turns: int = 10
    on_progress: Callable[[str], None] | None = None


class LiveTaskOptions(NamedTuple):
    """真实任务的工作目录、执行次数、输出位置和执行器配置。"""

    cwd: Path | None = None
    runs: int = 1
    model: str | None = None
    timeout: int = 300
    max_turns: int = 10
    output_dir: Path = Path("output")
    on_progress: Callable[..., None] | None = None
    on_run_progress: Callable[..., None] | None = None
    executors: list[str] | None = None
