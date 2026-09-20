#!/usr/bin/env bash
# sift 测试入口：供仓顶 scripts/run-tests.sh 转调，也可单独执行。
# 复用包内 .venv，缺失时用 PYTHON（默认 python3，要求 >= 3.10）创建；
# 测试依赖缺失时按上游 pyproject.toml 的 dev extra 安装，执行原有 pytest。
# 可传 pytest 参数，例如 ./scripts/run-tests.sh tests/test_parser.py。
#
# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [ ! -x .venv/bin/python ]; then
  "${PYTHON:-python3}" -m venv .venv
fi
PY="$PWD/.venv/bin/python"
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else "sift requires Python >= 3.10")'
if ! "$PY" -c 'import pytest, pytest_mock, sift, typer, rich, pydantic, yaml' >/dev/null 2>&1; then
  echo "==> [sift] test deps missing, installing .[dev]"
  "$PY" -m pip --version >/dev/null 2>&1 || "$PY" -m ensurepip
  "$PY" -m pip install -e '.[dev]'
fi
exec "$PY" -m pytest -q "$@"
