"""Work-order model for GridCare-Lite."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WorkOrder:
    """Represents maintenance work order."""

    id: int | None
    outage_id: int
    assigned_to: str
    status: str
