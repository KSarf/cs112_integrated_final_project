"""Base repository placeholders for GridCare-Lite."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class BaseRepository:
    """Base repository storing db path reference."""

    database_path: Path
