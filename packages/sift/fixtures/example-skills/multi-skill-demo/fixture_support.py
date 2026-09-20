# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

import json
import logging


def output(message, stream):
    handler = logging.Handler()

    def emit(record):
        stream.write(record.getMessage() + "\n")

    handler.emit = emit
    handler.handle(logging.LogRecord(__name__, logging.INFO, __file__, 0, str(message), (), None))


def review_issue(severity, category, description):
    return {"line": 2, "severity": severity, "category": category, "description": description}


def review_report(path, issue, summary=None):
    payload = {"file": path}
    if summary is not None:
        payload["summary"] = summary
    payload["issues"] = [issue]
    return json.dumps(payload, ensure_ascii=False, indent=2)
