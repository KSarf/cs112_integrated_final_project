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

            self.configure(bg="#F7F9FC")

            self._setup_styles()
            self._build_header()
            self._build_table()
            self._build_footer()

            self.load_outages()

        def _setup_styles(self) -> None:
            """Configure table styling."""

            style = ttk.Style(self)

            try:
                style.theme_use("clam")
            except tk.TclError:
                pass

            style.configure(
                "Outages.Treeview",
                background="white",
                foreground="#1F2937",
                rowheight=40,
                fieldbackground="white",
                font=("Segoe UI", 10),
                borderwidth=0,
            )

            style.configure(
                "Outages.Treeview.Heading",
                background="#EEF2F7",
                foreground="#1F2937",
                font=("Segoe UI Semibold", 10),
                padding=(10, 10),
            )

            style.map(
                "Outages.Treeview",
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
                text="Outages",
                bg="#F7F9FC",
                fg="#111827",
                font=("Segoe UI Semibold", 26),
            ).pack(
                anchor="w",
            )

            tk.Label(
                header,
                text="Monitor reported outages and their current status.",
                bg="#F7F9FC",
                fg="#6B7280",
                font=("Segoe UI", 11),
            ).pack(
                anchor="w",
                pady=(6, 0),
            )

        def _build_table(self) -> None:
            """Create the outages table."""

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
                style="Outages.Treeview",
            )

            self.table.heading(
                "id",
                text="ID",
            )

            self.table.heading(
                "title",
                text="Outage",
            )

            self.table.heading(
                "substation",
                text="Substation",
            )

            self.table.heading(
                "severity",
                text="Severity",
            )

            self.table.heading(
                "status",
                text="Status",
            )

            self.table.heading(
                "reported_at",
                text="Reported",
            )

            self.table.column(
                "id",
                width=55,
                minwidth=55,
                anchor=tk.CENTER,
            )

            self.table.column(
                "title",
                width=270,
                minwidth=180,
                anchor=tk.W,
            )

            self.table.column(
                "substation",
                width=180,
                minwidth=130,
                anchor=tk.W,
            )

            self.table.column(
                "severity",
                width=110,
                minwidth=90,
                anchor=tk.CENTER,
            )

            self.table.column(
                "status",
                width=130,
                minwidth=100,
                anchor=tk.CENTER,
            )

            self.table.column(
                "reported_at",
                width=170,
                minwidth=130,
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
                command=self.load_outages,
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

        def load_outages(self) -> None:
            """Load outages from the SQLite database."""

            for item in self.table.get_children():
                self.table.delete(item)

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    cursor.execute("""
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
                print(f"Could not load outages: {error}")

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
