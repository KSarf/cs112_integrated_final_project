"""Entry point for GridCare-Lite starter application."""

from __future__ import annotations

from gridcare_lite.app.config import load_config
from gridcare_lite.app.database.schema import initialize_database
from gridcare_lite.app.ui.application import GridCareApplication


def run() -> None:
    """Initialize database and start Tkinter app."""
    config = load_config()
    initialize_database(config.database_path)
    app = GridCareApplication(config)
    app.mainloop()


if __name__ == "__main__":
    run()
