# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Python syntax assertions must inspect Python grammar, without executing code."""

from types import SimpleNamespace

import pytest

from sift.models import Assertion, AssertionType, AssertionVerdict, EvalCase
import sift.scoring.programmatic as programmatic
from sift.scoring.programmatic import ProgrammaticChecker


@pytest.mark.parametrize(
    "code,passed",
    [
        ('value = "]"\n', True),
        ("# closing bracket ] in a comment\nvalue = 1\n", True),
        ('doc = """[text)"""\n', True),
        ("value = [1, 2]\n", True),
        ("\ufeffvalue = 1\n", True),
        ("value = 1\x00\n", False),
        ("value = \n", False),
        ("if True\n    value = 1\n", False),
        ("value = [1, 2)\n", False),
        ('raise RuntimeError("must not run")\n', True),
    ],
)
def test_public_python_syntax_assertion(tmp_path, code, passed):
    (tmp_path / "example.py").write_text(code)
    case = EvalCase(
        id=1,
        prompt="check syntax",
        assertions=[
            Assertion(
                name="Python syntax",
                type=AssertionType.CODE_COMPILES,
                params={"include": "*.py"},
            )
        ],
    )
    result = ProgrammaticChecker().check(case, tmp_path)[0]
    assert result.passed is passed


def test_non_python_bracket_check_is_preserved(tmp_path):
    (tmp_path / "example.ts").write_text("const a = [1, 2);")
    case = EvalCase(
        id=1,
        prompt="check syntax",
        assertions=[
            Assertion(
                name="TS syntax",
                type=AssertionType.CODE_COMPILES,
                params={"include": "*.ts"},
            )
        ],
    )
    assert not ProgrammaticChecker().check(case, tmp_path)[0].passed


def test_documented_ast_value_error_keeps_the_assertion_batch_running(
    monkeypatch, tmp_path
):
    (tmp_path / "example.py").write_bytes(b"value = 1\x00\n")

    def documented_parse_failure(source, **_kwargs):
        assert "\x00" in source
        raise ValueError("source code string cannot contain null bytes")

    # Isolate the documented parser exception without replacing pytest's ast.
    monkeypatch.setattr(
        programmatic, "ast", SimpleNamespace(parse=documented_parse_failure)
    )
    case = EvalCase(
        id=1,
        prompt="check syntax and continue",
        assertions=[
            Assertion(
                name="Python syntax",
                type=AssertionType.CODE_COMPILES,
                params={"include": "*.py"},
            ),
            Assertion(
                name="file remains available",
                type=AssertionType.FILE_EXISTS,
                params={"filename": "example.py"},
            ),
        ],
    )
    results = ProgrammaticChecker().check(case, tmp_path)
    assert [result.verdict for result in results] == [
        AssertionVerdict.FAIL,
        AssertionVerdict.PASS,
    ]
    assert "null bytes" in results[0].evidence
