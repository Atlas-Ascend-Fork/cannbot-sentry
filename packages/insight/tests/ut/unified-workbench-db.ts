// Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
// This program is free software, you can redistribute it and/or modify it under the terms and conditions of
// CANN Open Software License Agreement Version 2.0 (the "License").
// Please refer to the License for details. You may not use this file except in compliance with the License.
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
// See LICENSE in the root of the software repository for the full text of the License.

// unified-workbench 的进程私有库装配（副作用模块；测试文件必须把它保持为
// 首 import——晚于 tests/setup.ts 生效、早于 @/app/page 与 @/lib/db 求值）。
// 该文件的「系统总消耗」用例对 Σ全库快照断言，而共享 test.db 在 CI 高并行
// （数十 worker、WAL 并发写）下于整个用例生命周期内持续落种子/原行更新——
// 有界重试追不上连续漂移（实测 36 路并行下「内容一致」括号连续 4 轮追不上
// 单行漂移）。这里用 better-sqlite3 在线备份把共享库快照为进程私有副本
// （表结构 + 当刻他人行的冻结态），再把 DATABASE_URL 指过去：此后并行文件
// 写原库，本文件的全部读写（含 Home 页面取数与 prisma 单例）都落在私有副
// 本上——Σ全库等式在无互扰的冻结行集上成立。私有副本由测试文件 afterAll
// 清理（含 -wal/-shm 同伴文件）。
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import Database from 'better-sqlite3';

const resolveSharedDb = (): string => {
  const url = process.env.DATABASE_URL ?? 'file:./test.db';
  let src = url.startsWith('file:') ? url.slice('file:'.length) : url;
  src = src.split('?')[0]!;
  // Prisma 的 file: 相对路径相对 schema 目录（packages/insight/prisma）解析
  return path.isAbsolute(src) ? src : path.resolve(__dirname, '../../prisma', src);
};

export const PRIVATE_DB_PATH = path.join(os.tmpdir(), `insight-uw-private-${process.pid}.db`);

if (fs.existsSync(PRIVATE_DB_PATH)) fs.rmSync(PRIVATE_DB_PATH, { force: true });

const source = new Database(resolveSharedDb(), { readonly: true });
try {
  // 在线备份：WAL 并发写下也能拿到事务一致快照（直接拷贝文件可能撕裂页面）
  await source.backup(PRIVATE_DB_PATH);
} finally {
  source.close();
}
process.env.DATABASE_URL = `file:${PRIVATE_DB_PATH}`;
