# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Dataclass option declarations using Typer's normal parameter conversion."""

from dataclasses import fields
from inspect import Parameter, Signature, getdoc
from typing import get_type_hints


def options_command(app, options_type, name=None, **metadata):
    """Register declared fields as normal Typer options, then pass one options value."""
    annotations = get_type_hints(options_type)
    signature = Signature(
        Parameter(
            field.name,
            Parameter.KEYWORD_ONLY,
            default=field.default,
            annotation=annotations[field.name],
        )
        for field in fields(options_type)
    )

    def register(handler):
        def entrypoint(**values):
            return handler(options_type(**values))

        # Let Typer derive the CLI options and convert values from the declared fields.
        entrypoint.__name__ = handler.__name__
        entrypoint.__annotations__ = annotations
        entrypoint.__signature__ = signature
        app.command(name, **{"help": getdoc(handler), **metadata})(entrypoint)
        return handler

    return register
