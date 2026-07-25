"""Database tests for GridCare-Lite starter schema."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from gridcare_lite.app.database.schema import initialize_database


def test_initialize_database_creates_users_table(tmp_path: Path) -> None:
    db_path = tmp_path / "gridcare_test.db"
    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None
