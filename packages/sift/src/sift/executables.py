# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Resolve external commands before handing them to subprocess."""

import errno
import os
import shutil


def resolve_executable(name: str) -> str:
    """Return an absolute executable path, preserving missing-command errors."""
    executable = shutil.which(name)
    if executable is None:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), name)
    return os.path.abspath(executable)
