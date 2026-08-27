"""Tkinter compatibility helpers."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except ModuleNotFoundError:  # pragma: no cover - environment-specific
    tk = None
    messagebox = None
    ttk = None


def require_tkinter() -> None:
    """Raise a helpful error when tkinter is unavailable."""
    if tk is None:
        raise RuntimeError("tkinter is not available in this Python environment.")
