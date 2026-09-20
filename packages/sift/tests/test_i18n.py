# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Tests for shared i18n keyword tables (P2-13).

词表是 compliance/extractor.py 与 static_analysis/checks.py 的共享契约 ——
锁住内容,防止有人误改一处忘另处。
"""

from __future__ import annotations

from sift.i18n import ANTI_FABRICATION_CN


class TestI18nKeywords:
    @staticmethod
    def test_anti_fabrication_cn_contents():
        # 反捏造词 —— extractor(提取指令)+ checks(静态检查)共用
        for w in ("捏造", "编造", "虚构", "伪造", "臆造"):
            assert w in ANTI_FABRICATION_CN

    @staticmethod
    def test_anti_fabrication_cn_well_formed():
        assert isinstance(ANTI_FABRICATION_CN, tuple)
        assert len(ANTI_FABRICATION_CN) >= 5
        assert all(isinstance(w, str) and w for w in ANTI_FABRICATION_CN)
