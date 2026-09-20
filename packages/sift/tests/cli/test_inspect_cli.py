# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""inspect 命令(trigger_probes 显示)的 CLI 测试。"""

from typer.testing import CliRunner

from sift.cli.main import app
from sift.models import EvalCase, EvalSet, TriggerProbe


def _write(es: EvalSet, path):
    path.write_text(es.model_dump_json(), encoding="utf-8")
    return path


def test_inspect_shows_trigger_probes_breakdown(tmp_path):
    es = EvalSet(
        skill_name="sk",
        evals=[EvalCase(id=1, prompt="p", expectations=["e"])],
        trigger_probes=[
            TriggerProbe(id=1, prompt="q1", expect_trigger=True, rationale=""),
            TriggerProbe(id=2, prompt="q2", expect_trigger=False, rationale=""),
            TriggerProbe(id=3, prompt="q3", expect_trigger=True, rationale=""),
        ],
    )
    es_path = _write(es, tmp_path / "evals.json")
    r = CliRunner().invoke(app, ["inspect", str(es_path)])
    assert r.exit_code == 0, r.output
    assert "trigger 探题" in r.output
    assert "3 道" in r.output
    assert "should-trigger 2" in r.output  # 2 个 expect_trigger=True
    assert "should-not 1" in r.output  # 1 个 expect_trigger=False


def test_inspect_no_trigger_probes_omits_line(tmp_path):
    """无 trigger_probes → 不出 trigger 行(别出噪声)。"""
    es = EvalSet(skill_name="sk", evals=[EvalCase(id=1, prompt="p", expectations=["e"])])
    es_path = _write(es, tmp_path / "evals.json")
    r = CliRunner().invoke(app, ["inspect", str(es_path)])
    assert r.exit_code == 0, r.output
    assert "trigger 探题" not in r.output
