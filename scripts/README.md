# CANNBot-Sentry 治理脚本

仓级治理脚本目录，当前规划：

| 脚本 | 说明 | 状态 |
|------|------|------|
| `check-license.sh` | 许可证门禁：校验源码 CANN OSL 2.0 头齐全、三方件清单（`Third_Party_Open_Source_Software_List.yaml`）登记完整 | 随代码迁入提供 |
| `run-tests.sh` | 单元测试入口：转调 `packages/{insight,cpx,sift}/scripts/run-tests.sh`（默认 `auto` 按改动文件选范围，归属不明/根文件全量兜底；也可强制 `insight`/`cpx`/`sift`/`all`，任一失败退出码非 0；依赖缺失时包内脚本自动安装依赖（insight/cpx 使用 npm，sift 使用 `.venv` 和 `.[dev]`），fresh clone 一条命令可跑） | 已提供 |

脚本将在 PR 门禁流水线中自动执行，也可本地运行。随 `packages/` 各包迁入逐步补充。

评估和审计功能统一位于 `packages/sift`；auto 模式将该目录的变更归入 sift。
单独运行 sift：`./scripts/run-tests.sh sift`；包内入口 `packages/sift/scripts/run-tests.sh` 也可接收 pytest 参数。

sift 源码同步自 [guixu-labs/sift v2.6.0](https://github.com/guixu-labs/sift/tree/v2.6.0)，对应提交 `d00bcb97e85d68234c39b6e16a0aa91ae3344786`；包内 `scripts/run-tests.sh` 为 Sentry 测试接入入口。

Sift 的导入基线为上述上游提交；Sentry 在此基础上补充测试入口、版权许可头和第三方登记，
Python 业务逻辑保持不变。Apache 衍生部分的适用范围见 `packages/sift/NOTICE.md`。
