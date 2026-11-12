#!/usr/bin/env bash
# insight 单元用例入口（供仓顶 scripts/run-tests.sh 转调，也可单独执行）。
# 依赖缺失时自动 npm install（fresh clone / 流水线一条命令可跑；postinstall
# 会生成 Prisma client）。
# tests 分层与入口：`npm run test` 一条命令全覆盖——pretest（tsc + 库预备）
# → vitest（tests/ut 组件契约 + tests/pipeline 数据管线）→ Playwright
# （tests/e2e 浏览器全栈，自举 boot-server：e2e.db 重建 + 按需构建 + 起服）。
# 单层入口：npm run e2e（仅浏览器）/ npm run test:pipeline（仅管线）。
# COVERAGE=1 时改跑 npm run test:cov（pretest + vitest --coverage，v8
# provider 统计 src/ 全量；npm 只对 test 名挂 pretest 钩子，test:cov 需显式串）。
# --coverage / -c 参数等价置 COVERAGE=1。
#
# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
set -u

cd "$(dirname "${BASH_SOURCE[0]}")/.."

for a in "$@"; do
  case "$a" in
    --coverage|-c) COVERAGE=1 ;;
    *) echo "Usage: $0 [--coverage|-c]" >&2; exit 2 ;;
  esac
done

if [ ! -x node_modules/.bin/vitest ]; then
  echo "==> [insight] deps missing, running npm install (first run may take minutes)"
  npm install --no-audit --no-fund || exit 1
fi
if [ ! -x node_modules/.bin/vitest ]; then
  echo "vitest still missing after npm install" >&2
  exit 1
fi

if [ "${COVERAGE:-0}" = "1" ]; then
  # 与 cpx 对称：provider 被单独剥离（如 --omit=dev 装过）时自愈补装
  node -e "require.resolve('@vitest/coverage-v8')" 2>/dev/null \
    || { echo "==> [insight] coverage provider missing (@vitest/coverage-v8), installing"; \
         npm install --no-audit --no-fund || exit 1; }
  npm run test:cov
  rc=$?
  # vitest 默认失败 run 不产报告（reportOnFailure: false），提示行只在
  # 报告实际落盘后才打，避免指向不存在的文件
  [ -f coverage/lcov.info ] \
    && echo "==> [insight] 覆盖率明细: packages/insight/coverage/index.html（浏览器）/ lcov.info"
  exit "$rc"
else
  # UT 门禁 = pretest + vitest 全量（tests/ut + tests/pipeline + tests/cli），
  # 与仓顶 scripts/run-tests.sh 分层一致：tests/e2e 浏览器用例按需单独跑
  # （npm run e2e）。此前误走 npm run test（vitest && playwright）踩过两坑：
  # 1) e2e 套件未合入时 playwright 无 config，按默认 testMatch 把全部 vitest
  #    *.test.ts 当 spec 加载——数百个 internal state / next/server 解析错误
  #    拖垮门禁（vitest 曾因失败短路挡住了这一层，UT 修绿后即暴露）；
  # 2) 配套的浏览器自愈下载被静默且无超时，在被限流的 runner 上可挂死数
  #    小时（实测 2h10m 起）。UT 门禁不碰浏览器，两个坑一并根除。
  npm run pretest && npx vitest run
fi
