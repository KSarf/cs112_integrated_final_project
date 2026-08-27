"""Work orders view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from pathlib import Path

from gridcare_lite.app.ui.tk_compat import require_tkinter, tk, ttk

DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


if tk is not None:

    class WorkOrdersView(tk.Frame):
        """Display work orders stored in the GridCare database."""

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
            tk.Label(
                self,
                text="Work Orders",
                font=("Arial", 20, "bold"),
            ).pack(pady=(15, 5))

            tk.Label(
                self,
                text="Manage maintenance work orders for reported outages.",
                font=("Arial", 11),
            ).pack(pady=(0, 10))

            # -------------------------
            # BACK BUTTON
            # -------------------------
            tk.Button(
                self,
                text="← Back to Dashboard",
                command=self._on_back,
            ).pack(pady=5)

            # -------------------------
            # TABLE
            # -------------------------
            table_frame = tk.Frame(self)
            table_frame.pack(
                fill=tk.BOTH,
                expand=True,
                padx=20,
                pady=15,
            )

            columns = (
                "id",
                "outage",
                "assigned_to",
                "scheduled_date",
                "status",
                "instructions",
            )

            self.table = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings",
            )

            self.table.heading("id", text="ID")
            self.table.heading("outage", text="Outage")
            self.table.heading("assigned_to", text="Assigned To")
            self.table.heading("scheduled_date", text="Scheduled Date")
            self.table.heading("status", text="Status")
            self.table.heading("instructions", text="Instructions")

            self.table.column("id", width=50)
            self.table.column("outage", width=200)
            self.table.column("assigned_to", width=120)
            self.table.column("scheduled_date", width=120)
            self.table.column("status", width=110)
            self.table.column("instructions", width=250)

            scrollbar = ttk.Scrollbar(
                table_frame,
                orient=tk.VERTICAL,
                command=self.table.yview,
            )

            self.table.configure(
                yscrollcommand=scrollbar.set,
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

            # -------------------------
            # REFRESH BUTTON
            # -------------------------
            tk.Button(
                self,
                text="Refresh",
                command=self.load_work_orders,
            ).pack(pady=(0, 15))

            self.load_work_orders()

        def load_work_orders(self) -> None:
            """Load work orders from SQLite."""

            for item in self.table.get_children():
                self.table.delete(item)

            with sqlite3.connect(DATABASE_PATH) as connection:
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT
                        work_orders.id,
                        outages.title,
                        COALESCE(users.username, 'Unassigned'),
                        work_orders.scheduled_date,
                        work_orders.status,
                        COALESCE(work_orders.instructions, '')
                    FROM work_orders
                    JOIN outages
                        ON work_orders.outage_id = outages.id
                    LEFT JOIN users
                        ON work_orders.assigned_to = users.id
                    ORDER BY work_orders.id
                    """)

                rows = cursor.fetchall()

            for row in rows:
                self.table.insert(
                    "",
                    tk.END,
                    values=row,
                )

else:

    class WorkOrdersView:  # pragma: no cover
        """Fallback when Tkinter is unavailable."""

        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()
