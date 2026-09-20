# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""audit 子包:transcript 对账(transcript_path -> tool_trace/text/digest 重建 + checker)。

当前包含 rebuild(薄封装 build_digest,供 auditor 复用)和 provenance(确定性文件归因分析)。
"""

__all__ = ["analyze_provenance"]


from sift.audit.provenance import analyze_provenance
