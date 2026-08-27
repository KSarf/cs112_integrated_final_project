"""Reusable Tkinter components for GridCare-Lite starter UI."""

from __future__ import annotations

from gridcare_lite.app.ui.tk_compat import require_tkinter, tk


def section_title(parent: object, text: str) -> object:
    """Create a standardized section title label."""
    require_tkinter()
    assert tk is not None
    return tk.Label(parent, text=text, font=("Arial", 14, "bold"))
