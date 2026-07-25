"""Reusable Tkinter components for GridCare-Lite starter UI."""

from __future__ import annotations

import tkinter as tk


def section_title(parent: tk.Widget, text: str) -> tk.Label:
    """Create a standardized section title label."""
    return tk.Label(parent, text=text, font=("Arial", 14, "bold"))
