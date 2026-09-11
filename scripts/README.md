# CANNBot-Sentry 治理脚本

仓级治理脚本目录，当前规划：

| 脚本 | 说明 | 状态 |
|------|------|------|
| `check-license.sh` | 许可证门禁：校验源码 CANN OSL 2.0 头齐全、三方件清单（`Third_Party_Open_Source_Software_List.yaml`）登记完整 | 随代码迁入提供 |
| `run-tests.sh` | 单元测试入口：转调 `packages/{insight,cpx}/scripts/run-tests.sh`（默认 `auto` 按改动文件选范围，归属不明/根文件全量兜底；也可强制 `insight`/`cpx`/`all`，任一失败退出码非 0；依赖缺失时包内脚本自动 `npm install`，fresh clone 一条命令可跑） | 已提供 |

脚本将在 PR 门禁流水线中自动执行，也可本地运行。随 `packages/` 各包迁入逐步补充。
