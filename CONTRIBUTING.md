# 贡献指南

欢迎参与 CANNBot-Sentry 建设。本仓库是面向 LLM 编码 Agent（opencode / Claude Code）的观测 · 审计 · 评测哨站，采用 Monorepo（一仓一包）组织方式。本文档说明如何参与贡献。

📖 [中文文档](README-zh.md) · [English](README.md) · [安全声明](SECURITY.md) · [许可证](LICENSE)

---

## 快速开始

### 前置条件

1. 阅读[社区行为准则](https://gitcode.com/cann/community)
2. 签署 [CLA 协议](https://gitcode.com/cann/community)
3. Node.js >= 20（各包的 engines 约束以 `packages/<pkg>/package.json` 为准）

### 我能贡献什么

| 贡献类型 | 说明 |
|--------|------|
| 新增 / 改进包内能力 | 在 `packages/insight`、`packages/cpx`、`packages/sift` 内开发功能 |
| 新增包 | 在 `packages/` 下新增一个目录 = 一个独立安装包（先提 Issue 讨论） |
| Bug 修复 | 修复已有功能问题，直接提交 PR |
| 文档改进 | 修正文档错误、补充说明，直接提交 PR |
| 测试补充 | 增加测试覆盖，参考各包 `tests/` 目录 |

### 仓库布局约定

- **一仓一包**：`packages/` 下一个目录即一个独立安装包，可单独安装、组合安装或全量安装（见 `install.sh`）
- **包间零 import、零依赖**：包之间不允许源码级依赖，只允许运行时契约（数据文件格式、CLI 接口）耦合
- **零侵入原则**：不修改 Agent（opencode / Claude Code）本身的工作流，能力以旁路方式叠加

---

## 贡献流程

### 总体流程

```
提出 Issue → 讨论方案 → 提交 PR → CI 自动检查（License 门禁 + UT） → Committer 审批 → 合入
```

### 何时需要先提交 Issue

以下情况**必须**先提交 [Issue](https://gitcode.com/cann/cannbot-sentry/issues) 进行方案讨论：

- 在 `packages/` 下新增一个包
- 对现有包的功能范围做重大调整
- 修改包间运行时契约（数据格式、CLI 接口）
- 不确定改动是否需要讨论时

以下情况可直接提交 PR：

- 文档纠错（错别字、格式修正）
- 不改变逻辑的代码风格修正
- 简单的 Bug 修复（经 Issue 讨论确认后）

### Issue 规范

- 标题使用简洁的问题描述，正文包含：问题背景、复现步骤（Bug 类）或使用场景（功能类）、期望行为、实际行为
- 附上会话证据（insight 导出 / cpx 捕获片段）者优先处理，注意先对敏感信息脱敏
- 一个 Issue 聚焦一个问题

### PR 规范

- 一个 PR 只做一件事；PR 标题遵循 `type(scope): summary`（如 `feat(insight): ...`、`fix(cpx): ...`、`docs: ...`）
- PR 需包含：变更说明、测试方式、必要的截图或导出证据
- 新增依赖必须在 `Third_Party_Open_Source_Software_Notice` 中登记（License 须与 CANN OSL 2.0 兼容）
- 所有源文件须携带 CANN OSL 2.0 许可证头（见 `scripts/` 许可证门禁脚本）
- 合入需 2 位 Committer 审批（1 位 LGTM + 1 位 Approve）

### 质量门槛

| 检查项 | 要求 |
|--------|------|
| 单元测试 | 全量 UT 通过且日志无 ERROR |
| License 门禁 | 源码许可证头齐全，三方件清单登记完整 |
| 安全红线 | 禁止提交密钥、会话原始数据、内部地址（见 [SECURITY.md](SECURITY.md)） |

---

## 相关信息

- [安全声明](SECURITY.md) — 公网地址声明、文件权限、漏洞反馈
- [许可证](LICENSE) — CANN Open Software License v2.0
- [所属 SIG](https://gitcode.com/cann/community/tree/master/CANN/sigs/cannbot) — CANNBot SIG
- [问题反馈](https://gitcode.com/cann/cannbot-sentry/issues) — GitCode Issue
