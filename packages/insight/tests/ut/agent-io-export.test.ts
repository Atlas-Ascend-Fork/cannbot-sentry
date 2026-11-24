// Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
// This program is free software, you can redistribute it and/or modify it under the terms and conditions of
// CANN Open Software License Agreement Version 2.0 (the "License").
// Please refer to the License for details. You may not use this file except in compliance with the License.
// THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
// INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
// See LICENSE in the root of the software repository for the full text of the License.

import { randomUUID } from "node:crypto";
import { readFileSync } from "node:fs";
import { describe, it, expect } from "vitest";
import { prisma } from "../setup";
import { buildAgentIO } from "@/lib/export/agent-io-export";

const fixture = JSON.parse(readFileSync(new URL("../data/agent-io-export.json", import.meta.url), "utf8"));

describe("buildAgentIO (v4 Step 1)", () => {
  it("extracts a flat agent tree with envelope + I/O from its own complete bridge fixture", { timeout: 60_000 }, async () => {
    const session = await prisma.session.create({
      data: { taskId: `agent-io-export-${randomUUID()}`, framework: fixture.framework },
    });
    try {
      await prisma.turn.createMany({
        data: fixture.turns.map((turn: { turnIndex: number; role: string; content: string; isSubagent?: boolean; subagentSessionId?: string }) => ({ ...turn, sessionId: session.id })),
      });
      const turns = await prisma.turn.findMany({ where: { sessionId: session.id }, orderBy: { turnIndex: "asc" } });
      await prisma.interactionBridge.create({
        data: { ...fixture.bridge, sessionId: session.id, dispatchTurnId: turns[1].id, responseTurnId: turns[3].id },
      });
      const io = await buildAgentIO(session.taskId, prisma, fixture.framework);
      expect(io.sessionId).toBe(session.id);
      expect(io.taskQuery).toBe("Prepare the contribution report");
      expect(io.agents).toHaveLength(2);
      const main = io.agents.find(a => a.id === "main")!;
      expect(main.parentId).toBeNull();
      expect(main.role).toBe("main");
      expect(main.turns).toEqual([0, 1, 4]);
      expect(main.outputSummary).toBe("Contribution report complete");
      const subs = io.agents.filter(a => a.role === "subagent");
      expect(subs).toHaveLength(1);
      expect(subs[0]).toMatchObject({
        id: "agent-io-fixture-child", parentId: "main", role: "subagent",
        inputSummary: "Inspect the changes", outputSummary: "Analysis finished", turns: [2, 3],
      });
      const ids = new Set(io.agents.map(a => a.id));
      for (const sub of subs) expect(ids.has(sub.parentId!)).toBe(true);
      for (const agent of io.agents) {
        for (const key of ["latencySec", "tokensKt", "turnCount", "toolCallCount", "errorCount", "retryCount"] as const) {
          expect(typeof agent.envelope[key]).toBe("number");
          expect(agent.envelope[key]).toBeGreaterThanOrEqual(0);
        }
        expect(Array.isArray(agent.artifacts)).toBe(true);
        expect(new Set(agent.turns).size).toBe(agent.turns.length);
      }
    } finally {
      await prisma.session.delete({ where: { id: session.id } });
    }
  });
});
