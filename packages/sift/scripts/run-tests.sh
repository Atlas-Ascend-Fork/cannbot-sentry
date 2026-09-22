#!/usr/bin/env bash
# sift 测试入口：供仓顶 scripts/run-tests.sh 转调，也可单独执行。
# 复用包内 .venv，缺失时用 PYTHON（默认 python3，要求 >= 3.10）创建；
# 测试依赖缺失时按上游 pyproject.toml 的 dev extra 安装，执行原有 pytest。
# 可传 pytest 参数，例如 ./scripts/run-tests.sh tests/test_parser.py。
# 分层：默认排除 e2e 标记用例（真 CLI/网络/auth，环境不齐必红）——
#   SIFT_RUN_E2E=1 ./scripts/run-tests.sh     # 全量（含 e2e）
#   ./scripts/run-tests.sh -m e2e             # 只跑 e2e
#   传参里已带 -m 时尊重调用方选择，不再叠加默认过滤。
# Debian/Ubuntu 把 ensurepip 拆到 python3.<minor>-venv 包：venv 创建失败且
# 报 ensurepip 时自动 apt 安装补齐（root 直接装 / 非 root 走 sudo），装不上
# 则原样报错并给出手工指引退出。
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
  VENV_ERR="$(mktemp)"
  if ! "${PYTHON:-python3}" -m venv .venv >"$VENV_ERR" 2>&1; then
    if grep -q "ensurepip" "$VENV_ERR"; then
      PY_MINOR="$("${PYTHON:-python3}" -c 'import sys; print(sys.version_info.minor)')"
      VENV_PKG="python3.${PY_MINOR}-venv"
      echo "==> [sift] venv needs ensurepip (Debian/Ubuntu splits it into ${VENV_PKG}), installing..."
      APT_ERR="$(mktemp)"
      if [ "$(id -u)" -eq 0 ]; then
        apt-get update >/dev/null 2>>"$APT_ERR" && apt-get install -y "$VENV_PKG" 2>>"$APT_ERR"
      elif command -v sudo >/dev/null 2>&1; then
        # --non-interactive：无 tty 的 CI 里密码提示会挂死，失败走手工指引更快
        sudo --non-interactive apt-get update >/dev/null 2>>"$APT_ERR" \
          && sudo --non-interactive apt-get install -y "$VENV_PKG" 2>>"$APT_ERR"
      else
        false
      fi || {
        cat "$VENV_ERR" >&2
        cat "$APT_ERR" >&2
        echo "error: cannot install ${VENV_PKG}; install it manually (apt install ${VENV_PKG}) and re-run" >&2
        rm -f "$VENV_ERR" "$APT_ERR"
        exit 1
      }
      rm -f "$APT_ERR"
      # 重试的输出覆写 VENV_ERR，失败时展示的是本次原因而非首次的旧错误
      "${PYTHON:-python3}" -m venv .venv >"$VENV_ERR" 2>&1 \
        || { cat "$VENV_ERR" >&2; rm -f "$VENV_ERR"; exit 1; }
    else
      cat "$VENV_ERR" >&2
      rm -f "$VENV_ERR"
      exit 1
    fi
  fi
  rm -f "$VENV_ERR"
fi
PY="$PWD/.venv/bin/python"
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else "sift requires Python >= 3.10")'
if ! "$PY" -c 'import pytest, pytest_mock, sift, typer, rich, pydantic, yaml' >/dev/null 2>&1; then
  echo "==> [sift] test deps missing, installing .[dev]"
  "$PY" -m pip --version >/dev/null 2>&1 || "$PY" -m ensurepip
  "$PY" -m pip install -e '.[dev]'
fi

PYTEST_ARGS=()
has_m=0
for a in "$@"; do [ "$a" = "-m" ] && has_m=1; done
if [ "$has_m" -eq 0 ] && [ "${SIFT_RUN_E2E:-0}" != "1" ]; then
  PYTEST_ARGS+=(-m "not e2e")
fi
# ${PYTEST_ARGS[@]+...}：bash < 4.4 + set -u 下空数组直接展开会 unbound variable
# （macOS 系统自带 bash 3.2 即中招，恰是 -m e2e / SIFT_RUN_E2E=1 两条路径）
exec "$PY" -m pytest -q ${PYTEST_ARGS[@]+"${PYTEST_ARGS[@]}"} "$@"
