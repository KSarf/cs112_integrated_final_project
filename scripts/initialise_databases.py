"""Initialize starter SQLite databases."""

from __future__ import annotations

from pathlib import Path

from gridcare_lite.app.database.schema import initialize_database


def main() -> None:
    """Initialize local sqlite database files for starter development."""
    gridcare_db = Path("gridcare_lite/database/gridcare.db")
    initialize_database(gridcare_db)
    print(f"Initialized GridCare-Lite database at {gridcare_db}")


if __name__ == "__main__":
    main()
