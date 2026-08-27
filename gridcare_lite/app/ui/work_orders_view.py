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

            self.configure(bg="#F7F9FC")

            self._setup_styles()
            self._build_header()
            self._build_table()
            self._build_footer()

            self.load_work_orders()

        def _setup_styles(self) -> None:
            """Configure table styling."""

            style = ttk.Style(self)

            try:
                style.theme_use("clam")
            except tk.TclError:
                pass

            style.configure(
                "WorkOrders.Treeview",
                background="white",
                foreground="#1F2937",
                rowheight=42,
                fieldbackground="white",
                font=("Segoe UI", 10),
                borderwidth=0,
            )

            style.configure(
                "WorkOrders.Treeview.Heading",
                background="#EEF2F7",
                foreground="#1F2937",
                font=("Segoe UI Semibold", 10),
                padding=(10, 10),
            )

            style.map(
                "WorkOrders.Treeview",
                background=[("selected", "#DCEBFF")],
                foreground=[("selected", "#111827")],
            )

        def _build_header(self) -> None:
            """Create the page header."""

            header = tk.Frame(
                self,
                bg="#F7F9FC",
            )
            header.pack(
                fill=tk.X,
                padx=35,
                pady=(30, 20),
            )

            tk.Button(
                header,
                text="←  Dashboard",
                command=self._on_back,
                bg="#FFFFFF",
                fg="#374151",
                activebackground="#EEF2F7",
                activeforeground="#111827",
                relief=tk.FLAT,
                bd=0,
                font=("Segoe UI Semibold", 10),
                padx=15,
                pady=8,
                cursor="hand2",
            ).pack(
                anchor="w",
                pady=(0, 18),
            )

            tk.Label(
                header,
                text="Work Orders",
                bg="#F7F9FC",
                fg="#111827",
                font=("Segoe UI Semibold", 26),
            ).pack(
                anchor="w",
            )

            tk.Label(
                header,
                text="Manage and monitor maintenance work assigned to grid teams.",
                bg="#F7F9FC",
                fg="#6B7280",
                font=("Segoe UI", 11),
            ).pack(
                anchor="w",
                pady=(6, 0),
            )

        def _build_table(self) -> None:
            """Create the work orders table."""

            card = tk.Frame(
                self,
                bg="white",
                highlightbackground="#E5E7EB",
                highlightthickness=1,
            )
            card.pack(
                fill=tk.BOTH,
                expand=True,
                padx=35,
                pady=(0, 15),
            )

            table_frame = tk.Frame(
                card,
                bg="white",
            )
            table_frame.pack(
                fill=tk.BOTH,
                expand=True,
                padx=15,
                pady=15,
            )

            columns = (
                "id",
                "outage_id",
                "assigned_to",
                "scheduled_date",
                "status",
                "instructions",
                "resolution_notes",
                "completed_at",
            )

            self.table = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings",
                style="WorkOrders.Treeview",
            )

            self.table.heading(
                "id",
                text="ID",
            )

            self.table.heading(
                "outage_id",
                text="Outage",
            )

            self.table.heading(
                "assigned_to",
                text="Assigned To",
            )

            self.table.heading(
                "scheduled_date",
                text="Scheduled",
            )

            self.table.heading(
                "status",
                text="Status",
            )

            self.table.heading(
                "instructions",
                text="Instructions",
            )

            self.table.heading(
                "resolution_notes",
                text="Resolution",
            )

            self.table.heading(
                "completed_at",
                text="Completed",
            )

            self.table.column(
                "id",
                width=55,
                minwidth=55,
                anchor=tk.CENTER,
            )

            self.table.column(
                "outage_id",
                width=80,
                minwidth=70,
                anchor=tk.CENTER,
            )

            self.table.column(
                "assigned_to",
                width=110,
                minwidth=90,
                anchor=tk.CENTER,
            )

            self.table.column(
                "scheduled_date",
                width=120,
                minwidth=100,
                anchor=tk.CENTER,
            )

            self.table.column(
                "status",
                width=120,
                minwidth=100,
                anchor=tk.CENTER,
            )

            self.table.column(
                "instructions",
                width=330,
                minwidth=220,
                anchor=tk.W,
            )

            self.table.column(
                "resolution_notes",
                width=220,
                minwidth=150,
                anchor=tk.W,
            )

            self.table.column(
                "completed_at",
                width=140,
                minwidth=100,
                anchor=tk.CENTER,
            )

            vertical_scrollbar = ttk.Scrollbar(
                table_frame,
                orient=tk.VERTICAL,
                command=self.table.yview,
            )

            horizontal_scrollbar = ttk.Scrollbar(
                table_frame,
                orient=tk.HORIZONTAL,
                command=self.table.xview,
            )

            self.table.configure(
                yscrollcommand=vertical_scrollbar.set,
                xscrollcommand=horizontal_scrollbar.set,
            )

            self.table.grid(
                row=0,
                column=0,
                sticky="nsew",
            )

            vertical_scrollbar.grid(
                row=0,
                column=1,
                sticky="ns",
            )

            horizontal_scrollbar.grid(
                row=1,
                column=0,
                sticky="ew",
            )

            table_frame.rowconfigure(
                0,
                weight=1,
            )

            table_frame.columnconfigure(
                0,
                weight=1,
            )

        def _build_footer(self) -> None:
            """Create the page footer."""

            footer = tk.Frame(
                self,
                bg="#F7F9FC",
            )
            footer.pack(
                fill=tk.X,
                padx=35,
                pady=(0, 25),
            )

            tk.Button(
                footer,
                text="Refresh",
                command=self.load_work_orders,
                bg="#1F2937",
                fg="white",
                activebackground="#374151",
                activeforeground="white",
                relief=tk.FLAT,
                bd=0,
                font=("Segoe UI Semibold", 10),
                padx=18,
                pady=9,
                cursor="hand2",
            ).pack(
                side=tk.RIGHT,
            )

        def load_work_orders(self) -> None:
            """Load work orders from the SQLite database."""

            for item in self.table.get_children():
                self.table.delete(item)

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    cursor.execute("""
                        SELECT
                            id,
                            outage_id,
                            assigned_to,
                            scheduled_date,
                            status,
                            instructions,
                            resolution_notes,
                            completed_at
                        FROM work_orders
                        ORDER BY id
                        """)

                    rows = cursor.fetchall()

                for row in rows:
                    display_row = list(row)

                    for index, value in enumerate(display_row):
                        if value is None:
                            display_row[index] = "-"

                    self.table.insert(
                        "",
                        tk.END,
                        values=display_row,
                    )

            except sqlite3.Error as error:
                print(f"Could not load work orders: {error}")

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
