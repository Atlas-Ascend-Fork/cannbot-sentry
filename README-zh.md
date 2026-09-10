# CANNBot-Sentry

![License](https://img.shields.io/badge/License-CANN%20OSL%20v2.0-blue?style=flat-square)

**[English](README.md)**

CANNBot-Sentry 是面向 LLM 编码 Agent（opencode / Claude Code）的**观测 · 审计 · 评测**哨站。Agent 在场上跑，Sentry 在场边：**记录现场 · 复盘事实 · 评鉴质量**。

> 仓库状态：新建仓库。正在将 [cannbot-skills](https://gitcode.com/cann/cannbot-skills)（`plugins-community/cannbot-insight`）的主体代码迁入 `packages/insight` 与 `packages/cpx`，详见[目录结构](#目录结构)。

## 核心能力

| 能力 | 回答的问题 | 亮点 |
|------|-----------|------|
| **观测 Observe**（packages/insight） | 运行中发生了什么？ | 全量画像：Token · 成本 · 上下文；Turn / Tool / Skill 可回放时间线；按时间戳重建文件现场（取证） |
| **捕获 Capture**（packages/cpx） | 线上到底传了什么？ | 网关旁路捕获全量上下文请求/响应；API Key 永不落盘（唯一落盘咽喉统一打码） |
| **审计 Audit**（packages/sift） | 有没有按声明做？ | 双重校验：流程合规 + 结果一致；执行 vs 声明（Skill · Agent · Workflow）对账，证据回链 |
| **评测 Evaluate**（packages/sift） | 做得好不好？ | 静态：分析 + 安全审查（规则驱动）；动态：A/B —— 有无 Skill · 版本对比；判决报告 + CI 门禁 |

**原则**：零侵入 —— 不改 Agent 工作流、不改 opencode / Claude Code，能力叠加其上；本地优先 —— 只读取本地会话记录，数据不出域。

## 源码下载

```bash
git clone https://gitcode.com/cann/cannbot-sentry.git
cd cannbot-sentry
```

## 安装

**npm（免克隆源码）**——已发布到公共 npm registry，一条命令安装：

```bash
npm install -g cannbot-insight   # insight 观测平台（cannbot-insight / cbi）
npm install -g cannbot-proxy     # cpx 捕获代理（cpx）
```

**源码安装**——统一安装入口支持**单包 / 组合 / 全量**三种方式：

```bash
./install.sh insight   # 安装单个包
./install.sh cpx sift  # 组合安装
./install.sh all       # 全量安装
```

> 安装脚本将随 packages/ 各包迁入逐步完全可用，各包前置要求见其 README。

## 目录结构

Monorepo，`packages/` 下一个目录 = 一个独立安装包。包间零 import、零构建依赖，仅通过运行时契约（数据格式、CLI 接口）耦合。

```
cannbot-sentry/
├── README.md / README-zh.md   # 双语总览 · 导航与安装
├── LICENSE                    # CANN OSL 2.0 · 全仓唯一
├── CONTRIBUTING.md            # 贡献指南（Issue / PR 规范）
├── SECURITY.md                # 安全声明
├── OAT.xml / .gitignore       # 合规扫描 · 忽略规则
├── install.sh                 # 统一安装：单包 / 组合 / all
├── scripts/                   # 治理脚本（许可证门禁等）
├── docs/                      # 跨包文档（架构 · 安装）
└── packages/
    ├── insight/               # 会话洞察 · 观测
    ├── cpx/                   # 网关 · 流量捕获
    └── sift/                  # 审计 · 评测
```

拓展 Sentry = 在 `packages/` 下新增一个包，即插即用。

## 贡献指南

欢迎提交 Issue 与 PR。贡献流程、Issue/PR 规范与质量门槛见[贡献指南](CONTRIBUTING.md)。

## 问题反馈

- [GitCode Issue](https://gitcode.com/cann/cannbot-sentry/issues) — Bug / 功能建议 / 文档问题
- [CANNBot SIG](https://gitcode.com/cann/community/tree/master/CANN/sigs/cannbot) — 社区治理与项目方向

## 许可证

基于 CANN Open Software License v2.0 发布，见 [LICENSE](LICENSE)。

## 相关链接

- [安全声明](SECURITY.md) · [贡献指南](CONTRIBUTING.md) · [所属 SIG](https://gitcode.com/cann/community/tree/master/CANN/sigs/cannbot)
