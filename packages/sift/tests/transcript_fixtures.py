# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.


def dispatch_sequence(user_task: str, pairs: list[tuple[str, str, str, str]], closing: str) -> list[dict]:
    recs: list[dict] = [{"message": {"role": "user", "content": [{"type": "text", "text": user_task}]}}]
    for tid, role, prompt, result in pairs:
        recs.append(
            {
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": tid,
                            "name": "Task",
                            "input": {"subagent_type": role, "prompt": prompt},
                        }
                    ],
                }
            }
        )
        recs.append(
            {"message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tid, "content": result}]}}
        )
    recs.append({"message": {"role": "assistant", "content": [{"type": "text", "text": closing}]}})
    return recs
