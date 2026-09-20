# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""coverage HTML 报告生成器(抄 audit_viewer / trigger_viewer 模式)。"""

import json
from pathlib import Path

from sift.models.coverage_report import CoverageReport

_TEMPLATE = Path(__file__).parent / "templates" / "coverage-report.html"


class CoverageReportGenerator:
    @staticmethod
    def generate_html(report: CoverageReport) -> str:
        tpl = _TEMPLATE.read_text(encoding="utf-8")
        payload = json.dumps(report.model_dump(mode="json"), ensure_ascii=False)
        return tpl.replace("/*__EMBEDDED_DATA__*/", f"var EMBEDDED_DATA = {payload};")

    def write_html(self, report: CoverageReport, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.generate_html(report), encoding="utf-8")
