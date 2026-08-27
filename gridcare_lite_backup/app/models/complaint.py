"""Complaint model for GridCare-Lite."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Complaint:
    """Represents a customer complaint."""

    id: int | None
    customer_name: str
    details: str
    status: str
