# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software; you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Encoding for JSON values embedded in inline JavaScript."""

from __future__ import annotations

import json
from typing import Any


def dumps_for_script(value: Any, *, indent: int | None = None) -> str:
    """Serialize JSON so data cannot terminate its containing HTML script element."""
    payload = json.dumps(value, ensure_ascii=False, indent=indent)
    # U+2028/U+2029 were parsed as JavaScript string terminators by older
    # engines even though they are valid JSON characters.
    return (
        payload.replace("<", r"\u003c")
        .replace("\u2028", r"\u2028")
        .replace("\u2029", r"\u2029")
    )
