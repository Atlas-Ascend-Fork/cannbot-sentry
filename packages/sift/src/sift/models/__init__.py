# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Pydantic data models for sift."""

__all__ = [
    # Audit models
    "AuditCategory",
    "AuditFinding",
    "AuditMethod",
    "AuditReport",
    "AuditVerdict",
    # Enums
    "AssertionTier",
    "AssertionType",
    "AssertionVerdict",
    "CalibrationVerdict",
    "CheckMethod",
    "InstructionPriority",
    "InstructionSource",
    "NodeStatus",
    "ProcessStatus",
    "ScannerStatus",
    "SecuritySeverity",
    "SecurityVerdict",
    "SkillCategory",
    # Eval models
    "Assertion",
    "EvalCase",
    "EvalSet",
    "FixtureFile",
    "TriggerProbe",
    # Grading models
    "Claim",
    "EvalFeedback",
    "EvalFeedbackSuggestion",
    "ExecutionMetrics",
    "ExpectationResult",
    "GradingResult",
    "GradingSummary",
    "TimingData",
    "UserNotes",
    # Execution models
    "CheckResult",
    "RunConfig",
    "RunOutput",
    "ScoringConfig",
    "ToolCallRecord",
    "FileEffectRecord",
    "ProvenanceEvent",
    "SiftRecordsV2",
    "SiftRecordsV2Blob",
    "SiftRecordsV2Capture",
    "SiftRecordsV2FileEffect",
    "SiftRecordsV2NativeSession",
    "SiftRecordsV2Record",
    "SiftRecordsV2Session",
    "SiftRecordsV2ToolCall",
    "ProvenanceFinding",
    "ProvenanceAuditResult",
    "ProvenanceTimelineEntry",
    # Benchmark models
    "AnalysisReport",
    "AnomalyReport",
    "ComplianceSummary",
    "RunAnomaly",
    "RunResultEntry",
    "RunResultMetrics",
    "RunSummaryConfig",
    "StatsValue",
    # Comparison models
    "ComparisonExpectationDetail",
    "ComparisonExpectationResults",
    "ComparisonOutputQuality",
    "ComparisonOutputRubric",
    "ComparisonResult",
    "ComparisonRubricScores",
    "ComparisonStructureScores",
    # Analysis models
    "AnalysisImprovementSuggestion",
    "AnalysisInstructionFollowing",
    "AnalysisResult",
    # Batch + remaining models
    "BenchmarkData",
    "BenchmarkMetadata",
    "ComparisonSummary",
    "CalibrationReport",
    "CalibrationSummary",
    "HardViolation",
    "InstructionCheck",
    "ScannerResult",
    "SecurityFinding",
    "SecurityReport",
    # Trigger-accuracy report
    "ProbeResult",
    "Suggestion",
    "TriggerReport",
    # Coverage grid report
    "CoveragePoint",
    "CoverageReport",
]


from sift.models.analysis_models import (
    AnalysisImprovementSuggestion,
    AnalysisInstructionFollowing,
    AnalysisResult,
)
from sift.models.audit_models import (
    AuditCategory,
    AuditFinding,
    AuditMethod,
    AuditReport,
    AuditVerdict,
)
from sift.models.batch_models import (
    BenchmarkData,
    BenchmarkMetadata,
    CalibrationReport,
    CalibrationSummary,
    ComparisonSummary,
    HardViolation,
    InstructionCheck,
    ScannerResult,
    SecurityFinding,
    SecurityReport,
)
from sift.models.benchmark_models import (
    AnalysisReport,
    AnomalyReport,
    ComplianceSummary,
    RunAnomaly,
    RunResultEntry,
    RunResultMetrics,
    RunSummaryConfig,
    StatsValue,
)
from sift.models.comparison_models import (
    ComparisonExpectationDetail,
    ComparisonExpectationResults,
    ComparisonOutputQuality,
    ComparisonOutputRubric,
    ComparisonResult,
    ComparisonRubricScores,
    ComparisonStructureScores,
)
from sift.models.coverage_report import (
    CoveragePoint,
    CoverageReport,
)
from sift.models.enums import (
    AssertionTier,
    AssertionType,
    AssertionVerdict,
    CalibrationVerdict,
    CheckMethod,
    InstructionPriority,
    InstructionSource,
    NodeStatus,
    ProcessStatus,
    ScannerStatus,
    SecuritySeverity,
    SecurityVerdict,
    SkillCategory,
)
from sift.models.eval_models import (
    Assertion,
    EvalCase,
    EvalSet,
    FixtureFile,
    TriggerProbe,
)
from sift.models.execution_models import (
    CheckResult,
    FileEffectRecord,
    ProvenanceEvent,
    RunConfig,
    RunOutput,
    ScoringConfig,
    ToolCallRecord,
)
from sift.models.grading_models import (
    Claim,
    EvalFeedback,
    EvalFeedbackSuggestion,
    ExecutionMetrics,
    ExpectationResult,
    GradingResult,
    GradingSummary,
    TimingData,
    UserNotes,
)
from sift.models.provenance_audit_models import (
    ProvenanceAuditResult,
    ProvenanceFinding,
    ProvenanceTimelineEntry,
)
from sift.models.sift_records_v2 import (
    SiftRecordsV2,
    SiftRecordsV2Blob,
    SiftRecordsV2Capture,
    SiftRecordsV2FileEffect,
    SiftRecordsV2NativeSession,
    SiftRecordsV2Record,
    SiftRecordsV2Session,
    SiftRecordsV2ToolCall,
)
from sift.models.trigger_report import (
    ProbeResult,
    Suggestion,
    TriggerReport,
)
