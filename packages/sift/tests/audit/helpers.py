# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""CLI 审计测试复用的固定输入工厂。"""

import json
from pathlib import Path


def create_cli_skill(tmp_path: Path) -> Path:
    """创建默认 myskill 声明目录。"""
    sp = tmp_path / "skill"
    sp.mkdir()
    (sp / "SKILL.md").write_text(
        "---\nname: myskill\ndescription: d\n---\n# body\n",
        encoding="utf-8",
    )
    return sp


def write_jsonl(path: Path, records: list[dict]) -> Path:
    """逐条写入 UTF-8 JSONL，保留每条记录的换行。"""
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return path


def create_named_skill(tmp_path: Path, name: str = "skillA") -> Path:
    """创建指定名字的声明目录，默认用于 skillA 场景。"""
    sp = tmp_path / name
    sp.mkdir()
    (sp / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: d\n---\n# body\n",
        encoding="utf-8",
    )
    return sp


def create_root_skill(tmp_path: Path, name: str = "wf") -> Path:
    """创建 root 场景使用的声明，保留 wf 默认名字。"""
    return create_named_skill(tmp_path, name)
