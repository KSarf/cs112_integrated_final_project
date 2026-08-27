"""Substations view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from gridcare_lite.app.ui.tk_compat import require_tkinter, tk, ttk


DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


if tk is not None:

    class SubstationsView(tk.Frame):
        """Display substations stored in the GridCare database."""

        def __init__(self, parent: object) -> None:
            super().__init__(parent)

            tk.Label(
                self,
                text="Substations",
                font=("Arial", 18, "bold"),
            ).pack(pady=15)

            # Create table
            columns = (
                "id",
                "name",
                "region",
                "voltage",
                "capacity",
                "status",
            )

            self.table = ttk.Treeview(
                self,
                columns=columns,
                show="headings",
            )

            self.table.heading("id", text="ID")
            self.table.heading("name", text="Name")
            self.table.heading("region", text="Region")
            self.table.heading("voltage", text="Voltage (kV)")
            self.table.heading("capacity", text="Capacity (MVA)")
            self.table.heading("status", text="Status")

            self.table.column("id", width=50)
            self.table.column("name", width=200)
            self.table.column("region", width=120)
            self.table.column("voltage", width=100)
            self.table.column("capacity", width=110)
            self.table.column("status", width=100)

            self.table.pack(
                fill=tk.BOTH,
                expand=True,
                padx=20,
                pady=10,
            )

            self.load_substations()

        def load_substations(self) -> None:
            """Load substations from SQLite."""

            with sqlite3.connect(DATABASE_PATH) as connection:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        region,
                        voltage_kv,
                        capacity_mva,
                        status
                    FROM substations
                    ORDER BY id
                    """
                )

                rows = cursor.fetchall()

            for row in rows:
                self.table.insert("", tk.END, values=row)


else:

    class SubstationsView:  # pragma: no cover
        """Fallback when Tkinter is unavailable."""

        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()