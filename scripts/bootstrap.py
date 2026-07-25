"""Bootstrap local environment checks for the scaffold."""

from __future__ import annotations

from pathlib import Path


def main() -> None:
    """Create expected local folders that should exist for runtime artifacts."""
    for path in [
        Path("data/raw"),
        Path("data/processed"),
        Path("gridcare_lite/database"),
        Path("cliniccare_lite/uploads"),
    ]:
        path.mkdir(parents=True, exist_ok=True)
    print("Bootstrap complete.")


if __name__ == "__main__":
    main()
