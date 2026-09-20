# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Plugin registry for extensible assertion types."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

PluginHandler = Callable[[dict, Path], tuple[bool, str]]


class AssertionPluginRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, PluginHandler] = {}

    def register(self, plugin_type: str, handler: PluginHandler) -> None:
        self._handlers[plugin_type] = handler

    def get(self, plugin_type: str) -> PluginHandler | None:
        return self._handlers.get(plugin_type)

    def list_plugins(self) -> list[str]:
        return sorted(self._handlers.keys())
