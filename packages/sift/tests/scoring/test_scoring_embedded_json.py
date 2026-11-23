# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.


"""Scoring fallbacks preserve complete JSON despite delimiters in prose."""

import json
import random
from unittest.mock import patch

import pytest

from sift.execution.comparison_suite import (
    ComparisonInputs,
    ScoringCallbacks,
    _compare_with_retry,
)
from sift.models import (
    Assertion,
    AssertionTier,
    AssertionType,
    AssertionVerdict,
    EvalCase,
)
from sift.scoring.comparator import BlindComparator
from sift.scoring.llm_grader import LLMGrader
from sift.scoring.results import (
    parse_analysis_notes,
    parse_analysis_result,
    parse_comparison_result,
)


@pytest.mark.parametrize(
    "prefix,suffix",
    [
        ("", ""),
        ("Comment {not JSON} [not JSON]\n```json\n", "\n```"),
        ("```json\n", "\n```\nComment {not JSON} [not JSON]"),
        ("Comment {not JSON} [not JSON]\n", "\nComment {not JSON} [not JSON]"),
    ],
)
@pytest.mark.parametrize(
    "kind", ["comparison", "analysis", "notes", "grading", "tier3"]
)
def test_scoring_json_fallback_ignores_prose_delimiters(tmp_path, prefix, suffix, kind):
    evidence = '引用含 }、]、"转义引号和\\反斜杠'
    payloads = {
        "comparison": {"winner": "A", "reasoning": evidence},
        "analysis": {
            "winner_strengths": [evidence],
            "instruction_following": {"A": {"issues": [evidence]}},
        },
        "notes": [evidence],
        "grading": {
            "expectations": [{"text": "one", "passed": True, "evidence": evidence}],
            "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0},
        },
        "tier3": [{"index": 0, "verdict": "PASS", "evidence": evidence}],
    }
    payload = payloads.get(kind)
    assert payload is not None
    response = prefix + json.dumps(payload) + suffix
    if kind == "comparison":
        result = parse_comparison_result(response)
        assert not result.failed
        assert result.winner == "A"
        assert result.reasoning == evidence
    elif kind == "analysis":
        result = parse_analysis_result(response)
        assert result is not None
        assert result.winner_strengths == [evidence]
        assert result.instruction_following["A"].issues == [evidence]
    elif kind == "notes":
        assert parse_analysis_notes(response) == [evidence]
    else:
        with patch("sift.scoring.client.call_llm_with_retry", return_value=response):
            grader = LLMGrader()
            if kind == "grading":
                result = grader.grade(
                    EvalCase(id=1, prompt="check", expectations=["one"]), "t", tmp_path
                )
                rows = result.expectations
            else:
                assertion = Assertion(
                    name="one", type=AssertionType.LLM_GRADE, tier=AssertionTier.TIER3
                )
                rows = grader.grade_tier3([assertion], "t", tmp_path)
        assert rows[0].passed
        assert rows[0].evidence == evidence


def test_unparseable_comparison_keeps_failure():
    assert parse_comparison_result("{broken response}").failed


def test_unparseable_analysis_keeps_none():
    assert parse_analysis_result("{broken response}") is None


def test_plain_notes_keep_line_fallback():
    assert parse_analysis_notes("- first\n- second") == ["first", "second"]


def test_unparseable_grading_keeps_uneval(tmp_path):
    with patch(
        "sift.scoring.client.call_llm_with_retry", return_value="{broken response}"
    ):
        result = LLMGrader().grade(
            EvalCase(id=1, prompt="check", expectations=["one"]), "t", tmp_path
        )
    assert result.expectations[0].verdict == AssertionVerdict.UNEVAL


@pytest.mark.parametrize(
    "prefix",
    [
        {},
        {"unrelated": 1},
        {"example": {"winner": "A", "winner_strengths": ["example"]}},
        [{"winner": "A", "winner_strengths": ["example"]}],
        {"winner": "A", "winner_strengths": ["example"]},
    ],
)
@pytest.mark.parametrize("trailing_unrelated", [False, True])
@pytest.mark.parametrize("kind", ["comparison", "analysis"])
def test_scoring_result_uses_the_actual_outer_object_after_format_examples(
    prefix, trailing_unrelated, kind
):
    actual = (
        {"winner": "B", "reasoning": "actual decision"}
        if kind == "comparison"
        else {"winner_strengths": ["actual strength"], "instruction_following": {}}
    )
    response = (
        "Format example: "
        + json.dumps(prefix)
        + "\nActual result:\n"
        + json.dumps(actual)
    )
    if trailing_unrelated:
        response += "\nTrailing note: " + json.dumps({"unrelated": 2})
    if kind == "comparison":
        result = parse_comparison_result(response)
        assert not result.failed
        assert result.winner == "B"
        assert result.reasoning == "actual decision"
    else:
        result = parse_analysis_result(response)
        assert result is not None
        assert result.winner_strengths == ["actual strength"]


@pytest.mark.parametrize(
    "noise", [{}, {"unrelated": 1}, {"example": {"winner": "A"}}, [{"winner": "A"}]]
)
def test_unrelated_or_nested_objects_do_not_make_a_successful_result(noise):
    response = "Only a format example: " + json.dumps(noise)
    assert parse_comparison_result(response).failed
    assert parse_analysis_result(response) is None


def test_explicit_empty_analysis_fields_preserve_the_existing_schema():
    result = parse_analysis_result(
        '{"winner_strengths": [], "instruction_following": {}}'
    )
    assert result is not None
    assert result.winner_strengths == []
    assert result.instruction_following == {}


def test_arbitrary_json_object_causes_real_comparator_pair_retry():
    comparator = BlindComparator(rng=random.Random(0))
    actual = json.dumps({"winner": "B", "reasoning": "actual decision"})
    with (
        patch(
            "sift.scoring.client.call_llm_with_retry", side_effect=["{}", actual]
        ) as complete,
        patch("sift.execution.comparison_suite.time"),
    ):
        result = _compare_with_retry(
            comparator=comparator,
            max_retries=2,
            comparison=ComparisonInputs(
                output_a="a", output_b="b", eval_prompt="p", expectations=None
            ),
            callbacks=ScoringCallbacks(),
        )
    assert result is not None
    assert not result.failed
    assert result.winner in ("with", "without")
    assert result.reasoning == "actual decision"
    assert complete.call_count == 2
