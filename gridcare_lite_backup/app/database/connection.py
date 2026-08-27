"""SQLite connection helpers for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from pathlib import Path


def get_connection(database_path: Path) -> sqlite3.Connection:
    """Create a sqlite3 connection and ensure parent directory exists."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(database_path)
