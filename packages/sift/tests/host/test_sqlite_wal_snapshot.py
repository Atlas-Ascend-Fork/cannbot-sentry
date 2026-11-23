# Copyright (c) 2025-2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.


import sqlite3
from contextlib import closing

import pytest

from sift.evals.opencode_db import isolated_xdg_env


@pytest.mark.parametrize(
    "journal", ["WAL", "DELETE"], ids=["live-wal", "rollback-journal"]
)
def test_isolated_snapshot_preserves_committed_data_while_source_is_open(
    tmp_path, journal
):
    source = tmp_path / "source with space.db"
    with closing(sqlite3.connect(source)) as writer:
        assert (
            writer.execute("PRAGMA journal_mode=" + journal).fetchone()[0].upper()
            == journal
        )
        writer.execute("CREATE TABLE evidence(id INTEGER PRIMARY KEY, value TEXT)")
        writer.execute("INSERT INTO evidence VALUES(1, 'committed')")
        writer.commit()
        if journal == "WAL":
            assert (tmp_path / (source.name + "-wal")).stat().st_size > 0
        assert writer.execute("SELECT * FROM evidence").fetchall() == [(1, "committed")]

        with isolated_xdg_env(source) as isolated:
            copied = isolated / "opencode/opencode.db"
            with closing(sqlite3.connect(copied)) as reader:
                assert reader.execute("SELECT * FROM evidence").fetchall() == [
                    (1, "committed")
                ]
                assert reader.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert not isolated.exists()
        assert writer.execute("SELECT * FROM evidence").fetchall() == [(1, "committed")]
