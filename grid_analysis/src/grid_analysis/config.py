"""Configuration for grid-analysis paths and defaults."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GridAnalysisConfig:
    """Holds directory locations for grid-analysis assets."""

    repository_root: Path

    @property
    def raw_data_dir(self) -> Path:
        return self.repository_root / "data" / "raw"

    @property
    def processed_data_dir(self) -> Path:
        return self.repository_root / "data" / "processed"
