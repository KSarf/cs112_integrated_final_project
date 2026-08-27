"""Dashboard view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from gridcare_lite.app.ui.substations_view import SubstationsView
from gridcare_lite.app.ui.tk_compat import require_tkinter, tk


def get_database_path() -> Path:
    """Return the path to the GridCare database."""
    return Path("gridcare_lite/database/gridcare.db")


def get_counts() -> tuple[int, int, int, int]:
    """Get basic statistics from the GridCare database."""
    database_path = get_database_path()

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM substations")
        substations = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM lines")
        lines = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM outages")
        outages = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM work_orders")
        work_orders = cursor.fetchone()[0]

    return substations, lines, outages, work_orders


if tk is not None:

    class DashboardView(tk.Frame):
        """Main GridCare-Lite dashboard."""

        def __init__(self, parent: object, username: str) -> None:
            super().__init__(parent)

            # -------------------------
            # HEADER
            # -------------------------

            tk.Label(
                self,
                text="GridCare-Lite Dashboard",
                font=("Arial", 20, "bold"),
            ).pack(pady=(20, 5))

            tk.Label(
                self,
                text=f"Welcome, {username}",
                font=("Arial", 12),
            ).pack(pady=(0, 20))

            # -------------------------
            # DATABASE STATISTICS
            # -------------------------

            substations, lines, outages, work_orders = get_counts()

            stats_frame = tk.Frame(self)
            stats_frame.pack(pady=10)

            self._create_stat(
                stats_frame,
                "Substations",
                substations,
                0,
            )

            self._create_stat(
                stats_frame,
                "Transmission Lines",
                lines,
                1,
            )

            self._create_stat(
                stats_frame,
                "Outages",
                outages,
                2,
            )

            self._create_stat(
                stats_frame,
                "Work Orders",
                work_orders,
                3,
            )

            # -------------------------
            # STATUS MESSAGE
            # -------------------------

            tk.Label(
                self,
                text="Grid infrastructure data loaded successfully.",
                font=("Arial", 11),
            ).pack(pady=25)

            # -------------------------
            # SUBSTATIONS BUTTON
            # -------------------------

            tk.Button(
                self,
                text="View Substations",
                font=("Arial", 11, "bold"),
                command=self.show_substations,
            ).pack(pady=10)

        def show_substations(self) -> None:
            """Open the substations window."""

            window = tk.Toplevel(self)

            window.title("GridCare-Lite - Substations")
            window.geometry("850x500")

            view = SubstationsView(window)
            view.pack(fill=tk.BOTH, expand=True)

        def _create_stat(
            self,
            parent: object,
            title: str,
            value: int,
            column: int,
        ) -> None:
            """Create a dashboard statistic card."""

            frame = tk.Frame(
                parent,
                relief=tk.RIDGE,
                borderwidth=2,
                padx=20,
                pady=15,
            )

            frame.grid(
                row=0,
                column=column,
                padx=8,
            )

            tk.Label(
                frame,
                text=title,
                font=("Arial", 10, "bold"),
            ).pack()

            tk.Label(
                frame,
                text=str(value),
                font=("Arial", 20, "bold"),
            ).pack(pady=(5, 0))


else:

    class DashboardView:  # pragma: no cover
        """Fallback when Tkinter is unavailable."""

        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()