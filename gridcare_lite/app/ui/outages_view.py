"""Outages view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from pathlib import Path

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

            # -------------------------
            # HEADER
            # -------------------------
            header = tk.Frame(self)
            header.pack(fill=tk.X, padx=20, pady=(20, 10))

            tk.Button(
                header,
                text="Back to Dashboard",
                command=self._on_back,
            ).pack(side=tk.LEFT)

            tk.Label(
                header,
                text="Grid Outages",
                font=("Arial", 20, "bold"),
            ).pack(side=tk.LEFT, padx=25)

            # -------------------------
            # TABLE
            # -------------------------
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

            self.tree = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings",
            )

            self.tree.heading("id", text="ID")
            self.tree.heading("title", text="Title")
            self.tree.heading("substation", text="Substation")
            self.tree.heading("severity", text="Severity")
            self.tree.heading("status", text="Status")
            self.tree.heading("reported_at", text="Reported At")

            self.tree.column("id", width=50, anchor=tk.CENTER)
            self.tree.column("title", width=220)
            self.tree.column("substation", width=150)
            self.tree.column("severity", width=100, anchor=tk.CENTER)
            self.tree.column("status", width=130, anchor=tk.CENTER)
            self.tree.column("reported_at", width=160)

            scrollbar = ttk.Scrollbar(
                table_frame,
                orient=tk.VERTICAL,
                command=self.tree.yview,
            )

            self.tree.configure(
                yscrollcommand=scrollbar.set,
            )

            self.tree.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
            )

            scrollbar.pack(
                side=tk.RIGHT,
                fill=tk.Y,
            )

            # -------------------------
            # REFRESH BUTTON
            # -------------------------
            tk.Button(
                self,
                text="Refresh Outages",
                command=self.load_outages,
            ).pack(pady=(5, 20))

            # Load database records
            self.load_outages()

        def load_outages(self) -> None:
            """Load outage records from the database."""

            # Remove existing rows
            for item in self.tree.get_children():
                self.tree.delete(item)

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
                    LEFT JOIN substations
                        ON outages.substation_id = substations.id
                    ORDER BY outages.id
                    """
                )

                rows = cursor.fetchall()

            for row in rows:
                self.tree.insert(
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