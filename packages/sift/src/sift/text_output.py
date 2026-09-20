# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Plain user-visible output through a logging handler, independent of log filtering."""

import logging
import sys


class TextOutputHandler(logging.Handler):
    """Write plain text; callers own flushing and stream errors propagate normally."""

    def __init__(self, stream):
        super().__init__()
        self.stream = stream

    def emit(self, record):
        self.stream.write(record.getMessage())


def write_text(text: str, *, stream) -> None:
    handler = TextOutputHandler(stream)
    record = logging.LogRecord("sift.output", logging.INFO, __file__, 0, text, (), None)
    handler.handle(record)


def print_text(text: str, *, file=None) -> None:
    stream = sys.stdout if file is None else file
    write_text(str(text), stream=stream)
    write_text("\n", stream=stream)
