"""Dashboard placeholder view for GridCare-Lite."""

from __future__ import annotations

import tkinter as tk


class DashboardView(tk.Frame):
    """Prototype dashboard displayed after login."""

    def __init__(self, parent: tk.Widget, username: str) -> None:
        super().__init__(parent)
        tk.Label(self, text=f"Welcome, {username}", font=("Arial", 16, "bold")).pack(pady=8)
        tk.Label(self, text="Initial prototype: functionality pending implementation.").pack(
            pady=4
        )
        tk.Label(self, text="TODO: Add outage, work-order, and complaint management workflows.").pack(
            pady=4
        )
