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
            super().__init__(
                parent,
                bg="#F7F9FC",
            )

            self._on_back = on_back

            self._configure_styles()
            self._build_header()
            self._build_table()
            self.load_substations()

        def _configure_styles(self) -> None:
            """Configure the visual style."""

            style = ttk.Style(self)

            try:
                style.theme_use("clam")
            except tk.TclError:
                pass

            style.configure(
                "GridCare.Treeview",
                background="#FFFFFF",
                foreground="#1F2937",
                rowheight=36,
                fieldbackground="#FFFFFF",
                font=("Segoe UI", 10),
                borderwidth=0,
            )

            style.configure(
                "GridCare.Treeview.Heading",
                background="#E9EEF5",
                foreground="#1F2937",
                font=("Segoe UI Semibold", 10),
                relief="flat",
            )

            style.map(
                "GridCare.Treeview",
                background=[
                    ("selected", "#DCEAFE"),
                ],
                foreground=[
                    ("selected", "#111827"),
                ],
            )

            style.configure(
                "GridCare.Vertical.TScrollbar",
                troughcolor="#EEF2F7",
                background="#B8C2D1",
                borderwidth=0,
                arrowsize=14,
            )

            style.configure(
                "GridCare.Horizontal.TScrollbar",
                troughcolor="#EEF2F7",
                background="#B8C2D1",
                borderwidth=0,
                arrowsize=14,
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
                pady=(28, 18),
            )

            tk.Button(
                header,
                text="← Dashboard",
                command=self._on_back,
                font=("Segoe UI Semibold", 10),
                bg="#FFFFFF",
                fg="#344054",
                activebackground="#E9EEF5",
                activeforeground="#1F2937",
                relief="solid",
                bd=1,
                padx=16,
                pady=8,
                cursor="hand2",
            ).pack(
                side=tk.LEFT,
            )

            title_area = tk.Frame(
                header,
                bg="#F7F9FC",
            )
            title_area.pack(
                side=tk.LEFT,
                padx=22,
            )

            tk.Label(
                title_area,
                text="Substations",
                font=("Segoe UI Semibold", 24),
                fg="#182230",
                bg="#F7F9FC",
            ).pack(
                anchor="w",
            )

            tk.Label(
                title_area,
                text="View substations and their operating information",
                font=("Segoe UI", 10),
                fg="#667085",
                bg="#F7F9FC",
            ).pack(
                anchor="w",
                pady=(3, 0),
            )

        def _build_table(self) -> None:
            """Create the substations table."""

            section = tk.Frame(
                self,
                bg="#F7F9FC",
            )
            section.pack(
                fill=tk.BOTH,
                expand=True,
                padx=35,
                pady=(0, 20),
            )

            section_header = tk.Frame(
                section,
                bg="#F7F9FC",
            )
            section_header.pack(
                fill=tk.X,
                pady=(0, 8),
            )

            tk.Label(
                section_header,
                text="Substation Records",
                font=("Segoe UI Semibold", 15),
                fg="#182230",
                bg="#F7F9FC",
            ).pack(
                side=tk.LEFT,
            )

            self.count_label = tk.Label(
                section_header,
                text="",
                font=("Segoe UI", 9),
                fg="#667085",
                bg="#F7F9FC",
            )
            self.count_label.pack(
                side=tk.LEFT,
                padx=10,
            )

            table_card = tk.Frame(
                section,
                bg="#FFFFFF",
                highlightbackground="#E4E7EC",
                highlightthickness=1,
            )
            table_card.pack(
                fill=tk.BOTH,
                expand=True,
            )

            table_container = tk.Frame(
                table_card,
                bg="#FFFFFF",
            )
            table_container.pack(
                fill=tk.BOTH,
                expand=True,
                padx=1,
                pady=1,
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
                table_container,
                columns=columns,
                show="headings",
                style="GridCare.Treeview",
                selectmode="browse",
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
                width=70,
                minwidth=60,
                anchor=tk.CENTER,
                stretch=False,
            )

            self.table.column(
                "name",
                width=250,
                minwidth=180,
                anchor=tk.W,
                stretch=True,
            )

            self.table.column(
                "region",
                width=180,
                minwidth=130,
                anchor=tk.W,
                stretch=True,
            )

            self.table.column(
                "voltage",
                width=150,
                minwidth=120,
                anchor=tk.CENTER,
                stretch=False,
            )

            self.table.column(
                "capacity",
                width=160,
                minwidth=130,
                anchor=tk.CENTER,
                stretch=False,
            )

            self.table.column(
                "status",
                width=150,
                minwidth=120,
                anchor=tk.CENTER,
                stretch=False,
            )

            vertical_scrollbar = ttk.Scrollbar(
                table_container,
                orient=tk.VERTICAL,
                command=self.table.yview,
                style="GridCare.Vertical.TScrollbar",
            )

            horizontal_scrollbar = ttk.Scrollbar(
                table_container,
                orient=tk.HORIZONTAL,
                command=self.table.xview,
                style="GridCare.Horizontal.TScrollbar",
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

            table_container.rowconfigure(
                0,
                weight=1,
            )

            table_container.columnconfigure(
                0,
                weight=1,
            )

            button_area = tk.Frame(
                section,
                bg="#F7F9FC",
            )
            button_area.pack(
                fill=tk.X,
                pady=(10, 0),
            )

            tk.Button(
                button_area,
                text="Refresh Substations",
                command=self.load_substations,
                font=("Segoe UI Semibold", 10),
                bg="#2563EB",
                fg="#FFFFFF",
                activebackground="#1D4ED8",
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                padx=18,
                pady=9,
                cursor="hand2",
            ).pack(
                side=tk.LEFT,
            )

        def load_substations(self) -> None:
            """Load substations from SQLite."""

            for item in self.table.get_children():
                self.table.delete(item)

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    cursor.execute("""
                        SELECT
                            id,
                            name,
                            region,
                            voltage_kv,
                            capacity_mva,
                            status
                        FROM substations
                        ORDER BY id
                        """)

                    rows = cursor.fetchall()

                for row in rows:
                    self.table.insert(
                        "",
                        tk.END,
                        values=row,
                    )

                if len(rows) == 1:
                    text = "1 substation"
                else:
                    text = f"{len(rows)} substations"

                self.count_label.config(
                    text=text,
                )

            except sqlite3.Error as error:
                self.count_label.config(
                    text="Unable to load substations",
                )

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
