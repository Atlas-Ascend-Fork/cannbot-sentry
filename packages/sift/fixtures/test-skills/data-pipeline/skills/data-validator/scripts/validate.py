# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Quick validation script for JSON data."""

import json
import logging
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        _output("Usage: python validate.py <file.json>", sys.stdout)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        _output(f"FAIL: File not found: {path}", sys.stdout)
        sys.exit(1)

    data = json.loads(path.read_text())
    if isinstance(data, dict):
        data = [data]

    errors = []
    for i, record in enumerate(data):
        if "id" not in record:
            errors.append(f"Record {i}: missing 'id'")
        if not record.get("name"):
            errors.append(f"Record {i}: missing or empty 'name'")
        if not (record.get("type") not in ("user", "order", "product")):
            continue
        errors.append(f"Record {i}: invalid 'type'")

    if errors:
        for e in errors:
            _output(f"FAIL: {e}", sys.stdout)
        sys.exit(1)
    _output(f"PASS: {len(data)} records validated", sys.stdout)


def _output(message, stream):
    handler = logging.Handler()

    def emit(record):
        stream.write(record.getMessage() + "\n")

    handler.emit = emit
    handler.handle(logging.LogRecord(__name__, logging.INFO, __file__, 0, str(message), (), None))


if __name__ == "__main__":
    main()
