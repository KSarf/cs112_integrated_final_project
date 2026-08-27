"""Dashboard view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from pathlib import Path

from gridcare_lite.app.ui.tk_compat import require_tkinter, tk


DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


def get_counts() -> tuple[int, int, int, int]:
    """Get basic statistics from the GridCare database."""

    with sqlite3.connect(DATABASE_PATH) as connection:
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

        def __init__(
            self,
            parent: object,
            username: str,
            on_substations: Callable[[], None],
            on_outages: Callable[[], None],
            on_work_orders: Callable[[], None],
        ) -> None:
            super().__init__(parent)

            self._on_substations = on_substations
            self._on_outages = on_outages
            self._on_work_orders = on_work_orders

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
            ).pack(pady=(0, 15))

            # -------------------------
            # STATISTICS
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
            # NAVIGATION
            # -------------------------
            tk.Label(
                self,
                text="Grid Management",
                font=("Arial", 14, "bold"),
            ).pack(pady=(25, 10))

            buttons_frame = tk.Frame(self)
            buttons_frame.pack(pady=5)

            tk.Button(
                buttons_frame,
                text="View Substations",
                width=20,
                command=self._on_substations,
            ).grid(
                row=0,
                column=0,
                padx=8,
                pady=8,
            )

            tk.Button(
                buttons_frame,
                text="View Outages",
                width=20,
                command=self._on_outages,
            ).grid(
                row=0,
                column=1,
                padx=8,
                pady=8,
            )

            tk.Button(
                buttons_frame,
                text="View Work Orders",
                width=20,
                command=self._on_work_orders,
            ).grid(
                row=0,
                column=2,
                padx=8,
                pady=8,
            )

            # -------------------------
            # STATUS
            # -------------------------
            tk.Label(
                self,
                text="Grid infrastructure data loaded successfully.",
                font=("Arial", 11),
            ).pack(pady=25)

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