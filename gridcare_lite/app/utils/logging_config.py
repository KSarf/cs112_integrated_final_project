"""Component-specific logging setup for GridCare-Lite."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the GridCare component."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)
