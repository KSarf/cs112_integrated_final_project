"""Operational reports view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from pathlib import Path

from gridcare_lite.app.ui.tk_compat import require_tkinter, tk, ttk

DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


if tk is not None:

    class ReportsView(tk.Frame):
        """Display basic GridCare operational reports."""

        def __init__(
            self,
            parent: object,
            on_back: Callable[[], None],
        ) -> None:
            super().__init__(parent)

            self._on_back = on_back
            self.configure(bg="#F7F9FC")

            self._build_header()
            self._build_summary()
            self._build_region_table()

            self.load_reports()

        def _build_header(self) -> None:
            """Create the report page header."""

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
                text="Operational Reports",
                bg="#F7F9FC",
                fg="#111827",
                font=("Segoe UI Semibold", 26),
            ).pack(anchor="w")

            tk.Label(
                header,
                text="Basic outage and resolution statistics.",
                bg="#F7F9FC",
                fg="#6B7280",
                font=("Segoe UI", 11),
            ).pack(
                anchor="w",
                pady=(6, 0),
            )

        def _build_summary(self) -> None:
            """Create summary report cards."""

            summary = tk.Frame(
                self,
                bg="#F7F9FC",
            )
            summary.pack(
                fill=tk.X,
                padx=35,
                pady=(0, 20),
            )

            open_card = tk.Frame(
                summary,
                bg="white",
                highlightbackground="#E5E7EB",
                highlightthickness=1,
                padx=25,
                pady=20,
            )
            open_card.pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=True,
                padx=(0, 10),
            )

            tk.Label(
                open_card,
                text="Open Outages",
                bg="white",
                fg="#6B7280",
                font=("Segoe UI", 10),
            ).pack(anchor="w")

            self.open_outages_label = tk.Label(
                open_card,
                text="0",
                bg="white",
                fg="#111827",
                font=("Segoe UI Semibold", 24),
            )
            self.open_outages_label.pack(
                anchor="w",
                pady=(5, 0),
            )

            resolution_card = tk.Frame(
                summary,
                bg="white",
                highlightbackground="#E5E7EB",
                highlightthickness=1,
                padx=25,
                pady=20,
            )
            resolution_card.pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=True,
                padx=(10, 0),
            )

            tk.Label(
                resolution_card,
                text="Average Resolution Time",
                bg="white",
                fg="#6B7280",
                font=("Segoe UI", 10),
            ).pack(anchor="w")

            self.resolution_time_label = tk.Label(
                resolution_card,
                text="0 hours",
                bg="white",
                fg="#111827",
                font=("Segoe UI Semibold", 24),
            )
            self.resolution_time_label.pack(
                anchor="w",
                pady=(5, 0),
            )

        def _build_region_table(self) -> None:
            """Create outages-by-region table."""

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
                pady=(0, 30),
            )

            tk.Label(
                card,
                text="Outages by Region",
                bg="white",
                fg="#111827",
                font=("Segoe UI Semibold", 15),
            ).pack(
                anchor="w",
                padx=20,
                pady=(20, 10),
            )

            columns = (
                "region",
                "count",
            )

            self.table = ttk.Treeview(
                card,
                columns=columns,
                show="headings",
                height=10,
            )

            self.table.heading(
                "region",
                text="Region",
            )

            self.table.heading(
                "count",
                text="Outages",
            )

            self.table.column(
                "region",
                width=300,
                anchor=tk.W,
            )

            self.table.column(
                "count",
                width=120,
                anchor=tk.CENTER,
            )

            self.table.pack(
                fill=tk.BOTH,
                expand=True,
                padx=20,
                pady=(0, 20),
            )

        def load_reports(self) -> None:
            """Load operational report values from the database."""

            for item in self.table.get_children():
                self.table.delete(item)

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM outages
                        WHERE status NOT IN ('Resolved', 'Closed')
                        """)
                    open_outages = cursor.fetchone()[0]

                    cursor.execute("""
                        SELECT AVG(
                            (julianday(resolved_at) - julianday(reported_at))
                            * 24
                        )
                        FROM outages
                        WHERE resolved_at IS NOT NULL
                        """)
                    average_hours = cursor.fetchone()[0]

                    cursor.execute("""
                        SELECT
                            COALESCE(substations.region, 'Unknown'),
                            COUNT(outages.id)
                        FROM outages
                        LEFT JOIN substations
                            ON outages.substation_id = substations.id
                        GROUP BY substations.region
                        ORDER BY COUNT(outages.id) DESC
                        """)
                    regions = cursor.fetchall()

                self.open_outages_label.config(
                    text=str(open_outages),
                )

                if average_hours is None:
                    resolution_text = "No data"
                else:
                    resolution_text = f"{average_hours:.1f} hours"

                self.resolution_time_label.config(
                    text=resolution_text,
                )

                for region, count in regions:
                    self.table.insert(
                        "",
                        tk.END,
                        values=(
                            region,
                            count,
                        ),
                    )

            except sqlite3.Error as error:
                print(f"Could not load reports: {error}")

else:

    class ReportsView:  # pragma: no cover
        """Fallback when Tkinter is unavailable."""

        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()
