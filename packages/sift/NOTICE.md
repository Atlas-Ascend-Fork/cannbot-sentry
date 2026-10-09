# NOTICE

本包以下文件改编（derive）自 Anthropic 的 skill-creator，其源码以
Apache License 2.0 发布（许可证全文见 [LICENSES/Apache-2.0.txt](LICENSES/Apache-2.0.txt)，
上游仓库：<https://github.com/anthropics/skills/tree/main/skills/skill-creator>）：

| 本包文件（相对于 `packages/sift/`） | 上游文件 | 主要修改 |
|---|---|---|
| `agents/grader.md` | `agents/grader.md` | 从「读 transcript 文件的多步判分」改为单次内联判分；新增 Tier 3 语义断言输入、输出截断规格与中文输出要求 |
| `agents/comparator.md` | `agents/comparator.md` | 适配本仓库 CLI 数据格式（内联输出对照、结构化返回）；中文输出要求 |
| `agents/analyzer.md` | `agents/analyzer.md` | 适配本仓库 benchmark 数据格式与双率（programmatic / LLM）维度；中文输出要求 |
| `src/sift/reporting/templates/viewer.html` | `eval-viewer/viewer.html` | 在上游基础上扩展报告区块（双率、盲比较、遵循性 / 审计等），保留原布局与样式骨架 |
| `src/sift/reporting/viewer.py`（保留历史衍生来源） | `eval-viewer/generate_review.py` | 最初适配运行目录与报告展示；2026-09-18 重写目录发现、文件预览、MIME 解析及服务响应，进一步统一报告记录组装与提示词读取，保留输出契约与历史归属 |

按 Apache License 2.0 第 4 条（ redistribution of Derivative Works）要求在此声明：
上述文件的第三方衍生部分继续保留 Apache License 2.0 的许可与归属声明。
上游版权声明为 `Copyright 2026 Anthropic, PBC.`。
Sentry 中的 Sift 原创部分遵循仓库根目录的 [CANN OSL 2.0](../../LICENSE)，
该项目级许可不替代上述第三方部分的 Apache 许可。
`viewer.py` 的历史来源在文件头保留；此前仅列两个目录遍历函数的范围描述不完整，
本次改按文件登记。重写并不抹除该文件的历史衍生关系。
文件中的 CANN 声明仅适用于 Sift 的原创增加部分。

本文中的路径均相对于 `packages/sift/`；原文件注释中的“根目录 NOTICE.md”指本包目录。
第三方登记见仓库根目录的 `Third_Party_Open_Source_Software_Notice`。
