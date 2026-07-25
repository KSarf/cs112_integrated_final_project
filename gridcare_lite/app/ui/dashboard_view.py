"""Dashboard placeholder view for GridCare-Lite."""

from __future__ import annotations

from gridcare_lite.app.ui.tk_compat import require_tkinter, tk

if tk is not None:

    class DashboardView(tk.Frame):
        """Prototype dashboard displayed after login."""

        def __init__(self, parent: object, username: str) -> None:
            super().__init__(parent)
            tk.Label(
                self, text=f"Welcome, {username}", font=("Arial", 16, "bold")
            ).pack(pady=8)
            tk.Label(
                self,
                text="Initial prototype: functionality pending implementation.",
            ).pack(pady=4)
            tk.Label(
                self,
                text="TODO: Add outage, work-order, and complaint management workflows.",
            ).pack(pady=4)

else:

    class DashboardView:  # pragma: no cover - environment-specific
        """Fallback class used when tkinter is unavailable."""

        def __init__(self, *args: object, **kwargs: object) -> None:
            _ = args, kwargs
            require_tkinter()
