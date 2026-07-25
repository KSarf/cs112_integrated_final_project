"""Database schema initialization for GridCare-Lite."""

from __future__ import annotations

from pathlib import Path

from .connection import get_connection


def initialize_database(database_path: Path) -> None:
    """Create starter tables for the prototype.

    TODO: Expand constraints and indexes during implementation phase.
    """
    with get_connection(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
            """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                location TEXT NOT NULL
            )
            """)
        connection.commit()
