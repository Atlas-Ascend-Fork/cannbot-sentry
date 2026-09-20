# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

import subprocess
import tempfile

from sift.executables import resolve_executable


def render_inner_html(script):
    harness = (
        "var __rendered = '';\n"
        "var document = { getElementById: function () {"
        "  return { set innerHTML(v) { __rendered = v; }, get innerHTML() { return __rendered; } };"
        " } };\n" + script + "\nprocess.stdout.write(__rendered);\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(harness)
        js = f.name
    return subprocess.run([resolve_executable("node"), js], capture_output=True, text=True)
