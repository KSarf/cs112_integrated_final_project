"""Run repository quality checks."""

from __future__ import annotations

import subprocess
import sys


CHECKS = [
    ["ruff", "check", "."],
    ["black", "--check", "."],
    ["pytest"],
]


def run_check(command: list[str]) -> int:
    """Run a command and return its exit code."""
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    """Execute all checks and fail fast when one fails."""
    for command in CHECKS:
        exit_code = run_check(command)
        if exit_code != 0:
            return exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
