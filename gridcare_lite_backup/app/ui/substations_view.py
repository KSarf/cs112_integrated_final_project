"""Substations view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from pathlib import Path

from gridcare_lite.app.ui.tk_compat import require_tkinter, tk, ttk


DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


if tk is not None:

    class SubstationsView(tk.Frame):
        """Display substations stored in the GridCare database."""

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

            self.load_substations()

        def _setup_styles(self) -> None:
            """Configure the table appearance."""

            style = ttk.Style(self)

            try:
                style.theme_use("clam")
            except tk.TclError:
                pass

            style.configure(
                "Substations.Treeview",
                background="white",
                foreground="#1F2937",
                rowheight=38,
                fieldbackground="white",
                font=("Segoe UI", 10),
                borderwidth=0,
            )

            style.configure(
                "Substations.Treeview.Heading",
                background="#EEF2F7",
                foreground="#1F2937",
                font=("Segoe UI Semibold", 10),
                padding=(10, 10),
            )

            style.map(
                "Substations.Treeview",
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

            back_button = tk.Button(
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
            )
            back_button.pack(
                anchor="w",
                pady=(0, 18),
            )

            tk.Label(
                header,
                text="Substations",
                bg="#F7F9FC",
                fg="#111827",
                font=("Segoe UI Semibold", 26),
            ).pack(
                anchor="w",
            )

            tk.Label(
                header,
                text="View and monitor substations across the electricity grid.",
                bg="#F7F9FC",
                fg="#6B7280",
                font=("Segoe UI", 11),
            ).pack(
                anchor="w",
                pady=(6, 0),
            )

        def _build_table(self) -> None:
            """Create the substations table."""

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
                "name",
                "region",
                "voltage",
                "capacity",
                "status",
            )

            self.table = ttk.Treeview(
                table_frame,
                columns=columns,
                show="headings",
                style="Substations.Treeview",
            )

            self.table.heading(
                "id",
                text="ID",
            )

            self.table.heading(
                "name",
                text="Substation",
            )

            self.table.heading(
                "region",
                text="Region",
            )

            self.table.heading(
                "voltage",
                text="Voltage (kV)",
            )

            self.table.heading(
                "capacity",
                text="Capacity (MVA)",
            )

            self.table.heading(
                "status",
                text="Status",
            )

            self.table.column(
                "id",
                width=60,
                minwidth=60,
                anchor=tk.CENTER,
            )

            self.table.column(
                "name",
                width=260,
                minwidth=180,
                anchor=tk.W,
            )

            self.table.column(
                "region",
                width=180,
                minwidth=130,
                anchor=tk.W,
            )

            self.table.column(
                "voltage",
                width=140,
                minwidth=100,
                anchor=tk.CENTER,
            )

            self.table.column(
                "capacity",
                width=150,
                minwidth=110,
                anchor=tk.CENTER,
            )

            self.table.column(
                "status",
                width=140,
                minwidth=100,
                anchor=tk.CENTER,
            )

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
                command=self.load_substations,
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

        def load_substations(self) -> None:
            """Load substations from the SQLite database."""

            for item in self.table.get_children():
                self.table.delete(item)

            try:
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
                    self.table.insert(
                        "",
                        tk.END,
                        values=row,
                    )

            except sqlite3.Error as error:
                print(f"Could not load substations: {error}")


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