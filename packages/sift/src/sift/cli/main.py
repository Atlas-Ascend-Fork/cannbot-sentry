# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

import typer
from rich.console import Console

from sift import __version__

app = typer.Typer(
    name="sift",
    help="评测 skill / agent 的能力 + 审计 skill / agent / 编排者的执行遵循性。",
    no_args_is_help=True,
)
console = Console()


def _version(value: bool):
    if value:
        console.print(f"sift {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(None, "--version", callback=_version, is_eager=True, help="Show version."),
):
    pass
