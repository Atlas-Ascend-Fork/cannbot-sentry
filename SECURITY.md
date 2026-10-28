# 安全声明

本文件声明 CANNBot-Sentry 仓库的安全策略，包括公网地址声明、文件权限参考与安全漏洞反馈渠道。

📖 [贡献指南](CONTRIBUTING.md) · [许可证](LICENSE) · [所属 SIG](https://gitcode.com/cann/community/tree/master/CANN/sigs/cannbot)

---

## 一、安全设计原则

CANNBot-Sentry 是旁路观测 · 审计 · 评测工具，安全边界遵循以下原则：

- **本地优先，数据不出域**：只读取本机的 opencode / Claude Code 会话记录与网关捕获文件，不向外部服务上传会话数据
- **零侵入**：不修改 Agent（opencode / Claude Code）工作流，不在 Agent 进程内注入代码
- **密钥永不落盘**：网关捕获（cpx）在唯一落盘入口对敏感字段与各厂家 API Key 形态统一打码

## 二、公网地址声明表

本仓库代码与文档中引用的公网地址声明如下。除下表所列地址外，源码中不得硬编码其他公网地址；新增公网地址须先在本表登记并通过评审。

| 序号 | 公网地址 | 用途 | 引用位置 |
|------|---------|------|---------|
| 1 | `https://gitcode.com/cann/cannbot-sentry` | 本仓库托管地址 | README.md / README-zh.md |
| 2 | `https://gitcode.com/cann/community` | 社区仓（CLA、行为准则、SIG 信息） | README.md / CONTRIBUTING.md |
| 3 | `https://gitcode.com/cann/cannbot-skills` | 上游技能仓（部分包的迁出来源） | README.md / packages/ |
| 4 | `https://gitcode.com/cann/cannbot-sentry/issues` | 问题反馈 | README.md / CONTRIBUTING.md |
| 5 | `https://img.shields.io` | README 徽章图 | README.md / README-zh.md |

> 注：三方依赖的上游社区地址统一在 `Third_Party_Open_Source_Software_Notice` 中登记，不在此表重复维护。

## 三、文件权限参考

本仓库对关键文件的推荐权限如下（与社区安全编码规范"多用户系统中按需指定文件权限"要求对应）：

| 路径 | 推荐权限 | 说明 |
|------|---------|------|
| `install.sh`、`scripts/*.sh` | `755` | 可执行脚本，不含敏感信息 |
| `LICENSE`、`README*.md`、`CONTRIBUTING.md`、`SECURITY.md`、`OAT.xml` | `644` | 只读文档与合规配置 |
| `.gitignore` | `644` | Git 配置 |
| `packages/*/...` 源码 | `644` | 源码文件 |
| 运行时产物（`*.db`、`captures/`、导出文件） | `600` 或不提交 | 会话数据可能含敏感内容，禁止入库（见 `.gitignore`） |

## 四、安全红线

以下内容**禁止**提交到本仓库：

- API Key、Token、口令等凭据（包括 `.env` 文件，已列入 `.gitignore`）
- 未脱敏的真实会话数据、捕获文件、导出报告
- 内部网络地址、未公开的公网地址（见第二节声明表）
- 任何恶意代码或未声明的开源片段引用

## 五、安全漏洞反馈

如发现本仓库存在安全漏洞，请通过 [GitCode Issue](https://gitcode.com/cann/cannbot-sentry/issues) 提交，并选择安全标签；敏感问题可先联系 [CANNBot SIG](https://gitcode.com/cann/community/tree/master/CANN/sigs/cannbot) Maintainer 私密处理。请在报告中说明：影响范围、复现步骤、可能的利用方式。我们将在确认后按社区流程修复并公示。

## 六、许可证

本仓库基于 [CANN Open Software License v2.0](LICENSE) 发布，安全声明与许可证条款冲突时以许可证为准。
