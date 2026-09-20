# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

import sift.cli.commands.add  # noqa: F401

# import 顺序 = --help 分区(panel)的显示顺序 = 工作流顺序:
# 静态体检 → 出题 → 评测 → 真任务 → 审计 → 判决 → 触发 → 看结果
import sift.cli.commands.analyze  # noqa: F401
import sift.cli.commands.audit  # noqa: F401
import sift.cli.commands.coverage  # noqa: F401
import sift.cli.commands.critique  # noqa: F401
import sift.cli.commands.freeze  # noqa: F401
import sift.cli.commands.gate  # noqa: F401
import sift.cli.commands.init  # noqa: F401
import sift.cli.commands.inspect  # noqa: F401
import sift.cli.commands.report  # noqa: F401
import sift.cli.commands.run  # noqa: F401  # eval + run(评测 → 真任务)
import sift.cli.commands.trigger  # noqa: F401
import sift.cli.commands.vet  # noqa: F401
from sift.cli.main import app
