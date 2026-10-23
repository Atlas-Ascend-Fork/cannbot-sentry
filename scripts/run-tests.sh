#!/usr/bin/env bash
# CANNBot-Sentry unit test runner (insight + cpx + sift) — 薄壳，转调各包自己的
# insight/cpx 只跑 tests/ut；tests/e2e 真进程/浏览器/环境依赖用例按需单独跑：
#   cd packages/<pkg> && npm run test:e2e
# sift 由包内 pytest 脚本决定测试范围：默认排除 e2e 标记用例（真 CLI/网络/
# auth），SIFT_RUN_E2E=1 含入或 -m e2e 单独跑。
# scripts/run-tests.sh（测试知识归包：insight 管慢速用例排除，cpx 管 vitest
# 二进制回退）。Usage:
#   ./scripts/run-tests.sh                    # auto：按改动文件选范围（默认）
#   ./scripts/run-tests.sh auto               # 同上
#   ./scripts/run-tests.sh insight            # 强制 insight
#   ./scripts/run-tests.sh cpx                # 强制 cpx
#   ./scripts/run-tests.sh sift               # 强制 sift
#   ./scripts/run-tests.sh all                # 强制全量
# 任意命令追加 --coverage（或 -c）：UT 附带覆盖率收集（insight/cpx 追加
# vitest --coverage，sift 追加 pytest --cov=sift），报告落各包 coverage/；
# 等价环境变量 COVERAGE=1（供流水线注入）。默认关闭，门禁路径与耗时不变。
#
# auto 判定（托底原则：判定环节永不报错；归属检查不出来就全量）：
#   git diff <base>...HEAD（base 默认 origin/master，可用 RUN_TESTS_BASE 覆盖）
#   + 未提交变更 → 改动只在 packages/insight 下则只跑 insight，只在
#   packages/cpx 下则只跑 cpx；packages/sift 下的变更只跑 sift。
#   根/共享文件或无法判断范围时全量兜底；现有 insight/cpx 联动规则保留：
#   - base 引用解析不出（浅克隆无 master / 无 git）——已提交改动无法计算
#   - 根/共享文件（scripts/、docs/、配置…）
#   - packages/insight/package.json（cpx 运行时借 insight 的 vitest）
#   - packages/cpx/src/redactor*（insight 的 lake 测试直接 import 它）
#
# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# 参数解析：scope 与 --coverage/-c 顺序不限；环境变量 COVERAGE=1 等价
SCOPE="" COV_REQ=0
for a in "$@"; do
  case "$a" in
    --coverage|-c) COV_REQ=1 ;;
    auto|insight|cpx|sift|all) [ -z "$SCOPE" ] && SCOPE="$a" ;;
    *) echo "Usage: $0 [auto|insight|cpx|sift|all] [--coverage|-c]" >&2; exit 2 ;;
  esac
done
SCOPE="${SCOPE:-auto}"
[ "$COV_REQ" -eq 1 ] && export COVERAGE=1
FAILED=()

detect_scope() {
  local base="${RUN_TESTS_BASE:-origin/master}"
  if ! command -v git >/dev/null 2>&1 \
    || ! git -C "$REPO_ROOT" rev-parse --verify -q "$base^{commit}" >/dev/null 2>&1; then
    echo "  (base '$base' not resolvable — full suite)" >&2
    echo "insight cpx sift"
    return
  fi
  local files
  files="$(git -C "$REPO_ROOT" diff --name-only "$base...HEAD" 2>/dev/null)"
  if [ -z "$files" ]; then
    files="$(git -C "$REPO_ROOT" diff --name-only "$base" HEAD 2>/dev/null)"
  fi
  files="$files"$'\n'"$(git -C "$REPO_ROOT" status --porcelain 2>/dev/null | cut -c4-)"

  local run_ins=0 run_cpx=0 run_sift=0
  while IFS= read -r f; do
    case "$f" in
      '') ;;
      packages/insight/package.json) run_ins=1; run_cpx=1 ;;
      packages/insight/*) run_ins=1 ;;
      packages/cpx/src/redactor*) run_ins=1; run_cpx=1 ;;
      packages/cpx/*) run_cpx=1 ;;
      packages/sift/*) run_sift=1 ;;
      *) run_ins=1; run_cpx=1; run_sift=1 ;;
    esac
  done <<< "$files"

  if [ "$run_ins" -eq 0 ] && [ "$run_cpx" -eq 0 ] && [ "$run_sift" -eq 0 ]; then
    echo "  (no changes detected vs $base — full suite)" >&2
    echo "insight cpx sift"
  else
    local selected=()
    [ "$run_ins" -eq 1 ] && selected+=(insight)
    [ "$run_cpx" -eq 1 ] && selected+=(cpx)
    [ "$run_sift" -eq 1 ] && selected+=(sift)
    echo "${selected[*]}"
  fi
}

run_pkg() {
  local pkg="$1"
  local script="$REPO_ROOT/packages/$pkg/scripts/run-tests.sh"
  echo "==> [$pkg] packages/$pkg/scripts/run-tests.sh"
  if [ ! -x "$script" ]; then
    echo "    missing script: $script" >&2
    return 1
  fi
  "$script"
}

dispatch() {
  local pkg
  for pkg in "$@"; do
    run_pkg "$pkg" || FAILED+=("$pkg")
  done
}

case "$SCOPE" in
  insight|cpx|sift) dispatch "$SCOPE" ;;
  all) dispatch insight cpx sift ;;
  auto)
    DETECTED="$(detect_scope)"
    echo "==> scope: $DETECTED"
    dispatch $DETECTED
    ;;
esac

echo
if [ "${#FAILED[@]}" -eq 0 ]; then
  echo "==> ALL PASSED"
  exit 0
fi
echo "==> FAILED: ${FAILED[*]}"
exit 1
