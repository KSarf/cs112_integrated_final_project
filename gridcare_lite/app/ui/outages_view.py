"""Outages view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from collections.abc import Callable

from gridcare_lite.app.ui.tk_compat import require_tkinter, tk, ttk


DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


if tk is not None:

    class OutagesView(tk.Frame):
        """Display reported grid outages."""

        def __init__(
            self,
            parent: object,
            on_back: Callable[[], None],
        ) -> None:
            super().__init__(parent)

            self._on_back = on_back

            # Header
            tk.Label(
                self,
                text="Grid Outages",
                font=("Arial", 20, "bold"),
            ).pack(pady=15)

            # Back button
            tk.Button(
                self,
                text="← Back to Dashboard",
                command=self._on_back,
            ).pack(pady=(0, 10))

            # Table
            table_frame = tk.Frame(self)
            table_frame.pack(
                fill=tk.BOTH,
                expand=True,
                padx=20,
                pady=10,
            )

            columns = (
                "id",
                "title",
                "substation",
                "severity",
                "status",
                "reported_at",
            )

            self.table = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings",
            )

            self.table.heading("id", text="ID")
            self.table.heading("title", text="Title")
            self.table.heading("substation", text="Substation")
            self.table.heading("severity", text="Severity")
            self.table.heading("status", text="Status")
            self.table.heading("reported_at", text="Reported At")

            self.table.column("id", width=50)
            self.table.column("title", width=220)
            self.table.column("substation", width=180)
            self.table.column("severity", width=100)
            self.table.column("status", width=120)
            self.table.column("reported_at", width=160)

            scrollbar = ttk.Scrollbar(
                table_frame,
                orient="vertical",
                command=self.table.yview,
            )

            self.table.configure(
                yscrollcommand=scrollbar.set
            )

            self.table.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
            )

            scrollbar.pack(
                side=tk.RIGHT,
                fill=tk.Y,
            )

            self.load_outages()

        def load_outages(self) -> None:
            """Load outages from SQLite."""

            with sqlite3.connect(DATABASE_PATH) as connection:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT
                        outages.id,
                        outages.title,
                        substations.name,
                        outages.severity,
                        outages.status,
                        outages.reported_at
                    FROM outages
                    JOIN substations
                        ON outages.substation_id = substations.id
                    ORDER BY outages.id
                    """
                )

                rows = cursor.fetchall()

            for row in rows:
                self.table.insert(
                    "",
                    tk.END,
                    values=row,
                )


else:

    class OutagesView:  # pragma: no cover
        """Fallback when Tkinter is unavailable."""

        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()