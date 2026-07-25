"""Outage model for GridCare-Lite."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Outage:
    """Represents a reported outage."""

    id: int | None
    title: str
    status: str
    location: str
