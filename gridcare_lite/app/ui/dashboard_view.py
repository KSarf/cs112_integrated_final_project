"""Professional dashboard view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from pathlib import Path

from gridcare_lite.app.security.permissions import has_permission
from gridcare_lite.app.ui.tk_compat import require_tkinter, tk

DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


def get_dashboard_data() -> dict[str, object]:
    """Retrieve dashboard statistics and recent activity."""

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

        cursor.execute("SELECT COUNT(*) FROM complaints")
        complaints = cursor.fetchone()[0]

        cursor.execute("""
            SELECT severity, COUNT(*)
            FROM outages
            GROUP BY severity
            """)

        severity_rows = cursor.fetchall()

        severity = {
            "Low": 0,
            "Medium": 0,
            "High": 0,
            "Critical": 0,
        }

        for level, count in severity_rows:
            severity[level] = count

        cursor.execute("""
            SELECT status, COUNT(*)
            FROM work_orders
            GROUP BY status
            """)

        work_order_rows = cursor.fetchall()

        work_status = {
            "Pending": 0,
            "Assigned": 0,
            "In Progress": 0,
            "Completed": 0,
            "Cancelled": 0,
        }

        for status, count in work_order_rows:
            work_status[status] = count

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
            ORDER BY outages.id DESC
            LIMIT 5
            """)

        recent_outages = cursor.fetchall()

    return {
        "substations": substations,
        "lines": lines,
        "outages": outages,
        "work_orders": work_orders,
        "complaints": complaints,
        "severity": severity,
        "work_status": work_status,
        "recent_outages": recent_outages,
    }


if tk is not None:

    class DashboardView(tk.Frame):
        """Professional GridCare-Lite operations dashboard."""

        BG = "#F5F7FA"
        SIDEBAR = "#102A43"
        SIDEBAR_HOVER = "#1D405F"
        WHITE = "#FFFFFF"
        TEXT = "#172B4D"
        MUTED = "#627D98"
        BORDER = "#D9E2EC"
        ACCENT = "#168AAD"
        GREEN = "#2A9D8F"
        ORANGE = "#F4A261"
        RED = "#E63946"
        PURPLE = "#6C63FF"

        FONT = "Segoe UI"

        def __init__(
            self,
            parent: object,
            username: str,
            role: str,
            on_substations: Callable[[], None],
            on_outages: Callable[[], None],
            on_work_orders: Callable[[], None],
            on_complaints: Callable[[], None],
            on_reports: Callable[[], None],
            on_logout: Callable[[], None],
        ) -> None:
            super().__init__(
                parent,
                bg=self.BG,
            )

            self._on_substations = on_substations
            self._on_outages = on_outages
            self._on_work_orders = on_work_orders
            self._on_complaints = on_complaints
            self._on_reports = on_reports
            self._on_logout = on_logout
            self._username = username
            self._role = role

            data = get_dashboard_data()

            self._build_sidebar()
            self._build_main_content(data)

        def _build_sidebar(self) -> None:
            """Create the navigation sidebar."""

            sidebar = tk.Frame(
                self,
                bg=self.SIDEBAR,
                width=235,
            )

            sidebar.pack(
                side=tk.LEFT,
                fill=tk.Y,
            )

            sidebar.pack_propagate(False)

            logo_frame = tk.Frame(
                sidebar,
                bg=self.SIDEBAR,
            )

            logo_frame.pack(
                fill=tk.X,
                padx=22,
                pady=(28, 30),
            )

            tk.Label(
                logo_frame,
                text="⚡",
                font=(self.FONT, 28, "bold"),
                bg=self.SIDEBAR,
                fg="#7FDBFF",
            ).pack(side=tk.LEFT)

            logo_text = tk.Frame(
                logo_frame,
                bg=self.SIDEBAR,
            )

            logo_text.pack(
                side=tk.LEFT,
                padx=9,
            )

            tk.Label(
                logo_text,
                text="GRIDCARE",
                font=(self.FONT, 16, "bold"),
                bg=self.SIDEBAR,
                fg=self.WHITE,
            ).pack(anchor="w")

            tk.Label(
                logo_text,
                text="LITE",
                font=(self.FONT, 9, "bold"),
                bg=self.SIDEBAR,
                fg="#7FDBFF",
            ).pack(anchor="w")

            tk.Label(
                sidebar,
                text="OPERATIONS",
                font=(self.FONT, 8, "bold"),
                bg=self.SIDEBAR,
                fg="#829AB1",
            ).pack(
                anchor="w",
                padx=24,
                pady=(0, 10),
            )

            if has_permission(self._role, "view_substations"):
                self._nav_button(
                    sidebar,
                    "⌂  Substations",
                    self._on_substations,
                )

            if has_permission(self._role, "view_outages"):
                self._nav_button(
                    sidebar,
                    "⚠  Outages",
                    self._on_outages,
                )

            if has_permission(self._role, "view_work_orders"):
                self._nav_button(
                    sidebar,
                    "✓  Work Orders",
                    self._on_work_orders,
                )

            if has_permission(self._role, "log_complaints"):
                self._nav_button(
                    sidebar,
                    "☏  Complaints",
                    self._on_complaints,
                )

            if has_permission(self._role, "view_reports"):
                self._nav_button(
                    sidebar,
                    "▤  Reports",
                    self._on_reports,
                )

            bottom = tk.Frame(
                sidebar,
                bg=self.SIDEBAR,
            )

            bottom.pack(
                side=tk.BOTTOM,
                fill=tk.X,
                padx=18,
                pady=22,
            )

            tk.Frame(
                bottom,
                bg="#36566F",
                height=1,
            ).pack(
                fill=tk.X,
                pady=(0, 16),
            )

            tk.Label(
                bottom,
                text="SIGNED IN AS",
                font=(self.FONT, 8, "bold"),
                bg=self.SIDEBAR,
                fg="#829AB1",
            ).pack(anchor="w")

            tk.Label(
                bottom,
                text=self._username,
                font=(self.FONT, 10, "bold"),
                bg=self.SIDEBAR,
                fg=self.WHITE,
            ).pack(
                anchor="w",
                pady=(3, 2),
            )

            tk.Label(
                bottom,
                text=self._role,
                font=(self.FONT, 8),
                bg=self.SIDEBAR,
                fg="#829AB1",
            ).pack(
                anchor="w",
                pady=(0, 12),
            )

            tk.Button(
                bottom,
                text="Logout",
                command=self._on_logout,
                font=(self.FONT, 9, "bold"),
                bg="#243B53",
                fg=self.WHITE,
                activebackground="#334E68",
                activeforeground=self.WHITE,
                relief=tk.FLAT,
                bd=0,
                padx=12,
                pady=8,
                cursor="hand2",
            ).pack(fill=tk.X)

        def _nav_button(
            self,
            parent: object,
            text: str,
            command: Callable[[], None],
            active: bool = False,
        ) -> None:
            """Create a sidebar navigation button."""

            button = tk.Button(
                parent,
                text=text,
                command=command,
                anchor="w",
                font=(
                    self.FONT,
                    10,
                    "bold" if active else "normal",
                ),
                bg=(self.SIDEBAR_HOVER if active else self.SIDEBAR),
                fg=(self.WHITE if active else "#BCCCDC"),
                activebackground=self.SIDEBAR_HOVER,
                activeforeground=self.WHITE,
                relief=tk.FLAT,
                bd=0,
                padx=24,
                pady=13,
                cursor="hand2",
            )

            button.pack(
                fill=tk.X,
                padx=10,
                pady=2,
            )

        def _build_main_content(
            self,
            data: dict[str, object],
        ) -> None:
            """Build the main dashboard area."""

            main = tk.Frame(
                self,
                bg=self.BG,
            )

            main.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
            )

            header = tk.Frame(
                main,
                bg=self.WHITE,
                height=105,
            )

            header.pack(fill=tk.X)
            header.pack_propagate(False)

            title_frame = tk.Frame(
                header,
                bg=self.WHITE,
            )

            title_frame.pack(
                side=tk.LEFT,
                padx=32,
                pady=16,
            )

            tk.Label(
                title_frame,
                text="GridCare-Lite",
                font=(self.FONT, 22, "bold"),
                bg=self.WHITE,
                fg=self.TEXT,
            ).pack(anchor="w")

            tk.Label(
                title_frame,
                text="National & Infrastructure Monitoring",
                font=(self.FONT, 11),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(
                anchor="w",
                pady=(3, 0),
            )

            status_frame = tk.Frame(
                header,
                bg=self.WHITE,
            )

            status_frame.pack(
                side=tk.RIGHT,
                padx=32,
            )

            tk.Label(
                status_frame,
                text="●",
                font=(self.FONT, 12),
                bg=self.WHITE,
                fg=self.GREEN,
            ).pack(side=tk.LEFT)

            tk.Label(
                status_frame,
                text=" System Online",
                font=(self.FONT, 10, "bold"),
                bg=self.WHITE,
                fg=self.TEXT,
            ).pack(side=tk.LEFT)

            content = tk.Frame(
                main,
                bg=self.BG,
            )

            content.pack(
                fill=tk.BOTH,
                expand=True,
                padx=32,
                pady=25,
            )

            tk.Label(
                content,
                text=f"Good day, {self._username}",
                font=(self.FONT, 15, "bold"),
                bg=self.BG,
                fg=self.TEXT,
            ).pack(anchor="w")

            tk.Label(
                content,
                text="Here is the current status of your grid operations.",
                font=(self.FONT, 10),
                bg=self.BG,
                fg=self.MUTED,
            ).pack(
                anchor="w",
                pady=(3, 18),
            )

            stats = tk.Frame(
                content,
                bg=self.BG,
            )

            stats.pack(fill=tk.X)

            self._stat_card(
                stats,
                "SUBSTATIONS",
                str(data["substations"]),
                "Grid facilities",
                self.ACCENT,
                0,
            )

            self._stat_card(
                stats,
                "TRANSMISSION LINES",
                str(data["lines"]),
                "Connected lines",
                self.PURPLE,
                1,
            )

            self._stat_card(
                stats,
                "ACTIVE OUTAGES",
                str(data["outages"]),
                "Reported events",
                self.RED,
                2,
            )

            self._stat_card(
                stats,
                "WORK ORDERS",
                str(data["work_orders"]),
                "Maintenance tasks",
                self.ORANGE,
                3,
            )

            self._stat_card(
                stats,
                "COMPLAINTS",
                str(data["complaints"]),
                "Customer reports",
                self.GREEN,
                4,
            )

            lower = tk.Frame(
                content,
                bg=self.BG,
            )

            lower.pack(
                fill=tk.BOTH,
                expand=True,
                pady=(22, 0),
            )

            left = tk.Frame(
                lower,
                bg=self.WHITE,
                highlightbackground=self.BORDER,
                highlightthickness=1,
            )

            left.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
                padx=(0, 10),
            )

            right = tk.Frame(
                lower,
                bg=self.WHITE,
                width=300,
                highlightbackground=self.BORDER,
                highlightthickness=1,
            )

            right.pack(
                side=tk.RIGHT,
                fill=tk.Y,
                padx=(10, 0),
            )

            right.pack_propagate(False)

            self._build_recent_outages(
                left,
                data["recent_outages"],
            )

            self._build_status_panel(
                right,
                data["severity"],
                data["work_status"],
            )

        def _stat_card(
            self,
            parent: object,
            title: str,
            value: str,
            subtitle: str,
            accent: str,
            column: int,
        ) -> None:
            """Create a dashboard statistic card."""

            card = tk.Frame(
                parent,
                bg=self.WHITE,
                highlightbackground=self.BORDER,
                highlightthickness=1,
                height=112,
            )

            card.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=5,
            )

            parent.grid_columnconfigure(
                column,
                weight=1,
            )

            card.grid_propagate(False)

            tk.Frame(
                card,
                bg=accent,
                width=5,
            ).pack(
                side=tk.LEFT,
                fill=tk.Y,
            )

            inner = tk.Frame(
                card,
                bg=self.WHITE,
            )

            inner.pack(
                fill=tk.BOTH,
                expand=True,
                padx=14,
                pady=12,
            )

            tk.Label(
                inner,
                text=title,
                font=(self.FONT, 8, "bold"),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(anchor="w")

            tk.Label(
                inner,
                text=value,
                font=(self.FONT, 24, "bold"),
                bg=self.WHITE,
                fg=self.TEXT,
            ).pack(
                anchor="w",
                pady=(2, 0),
            )

            tk.Label(
                inner,
                text=subtitle,
                font=(self.FONT, 9),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(anchor="w")

        def _build_recent_outages(
            self,
            parent: object,
            rows: list[tuple],
        ) -> None:
            """Display recent outage activity."""

            tk.Label(
                parent,
                text="Recent Outages",
                font=(self.FONT, 14, "bold"),
                bg=self.WHITE,
                fg=self.TEXT,
            ).pack(
                anchor="w",
                padx=20,
                pady=(18, 3),
            )

            tk.Label(
                parent,
                text="Latest events reported to GridCare",
                font=(self.FONT, 9),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 14),
            )

            if not rows:
                tk.Label(
                    parent,
                    text="No outages have been reported.",
                    font=(self.FONT, 10),
                    bg=self.WHITE,
                    fg=self.MUTED,
                ).pack(pady=30)

                return

            for row in rows:

                (
                    outage_id,
                    title,
                    substation,
                    severity,
                    status,
                    reported_at,
                ) = row

                item = tk.Frame(
                    parent,
                    bg=self.WHITE,
                )

                item.pack(
                    fill=tk.X,
                    padx=20,
                    pady=6,
                )

                severity_color = {
                    "Low": self.GREEN,
                    "Medium": self.ORANGE,
                    "High": "#E76F51",
                    "Critical": self.RED,
                }.get(
                    severity,
                    self.MUTED,
                )

                tk.Label(
                    item,
                    text="●",
                    font=(self.FONT, 10),
                    bg=self.WHITE,
                    fg=severity_color,
                ).pack(side=tk.LEFT)

                details = tk.Frame(
                    item,
                    bg=self.WHITE,
                )

                details.pack(
                    side=tk.LEFT,
                    fill=tk.X,
                    expand=True,
                    padx=10,
                )

                tk.Label(
                    details,
                    text=f"#{outage_id}  {title}",
                    font=(self.FONT, 9, "bold"),
                    bg=self.WHITE,
                    fg=self.TEXT,
                ).pack(anchor="w")

                tk.Label(
                    details,
                    text=(f"{substation or 'Unknown substation'} " f"• {reported_at}"),
                    font=(self.FONT, 8),
                    bg=self.WHITE,
                    fg=self.MUTED,
                ).pack(anchor="w")

                tk.Label(
                    item,
                    text=status,
                    font=(self.FONT, 8, "bold"),
                    bg=self.WHITE,
                    fg=severity_color,
                ).pack(side=tk.RIGHT)

                tk.Frame(
                    parent,
                    bg=self.BORDER,
                    height=1,
                ).pack(
                    fill=tk.X,
                    padx=20,
                )

        def _build_status_panel(
            self,
            parent: object,
            severity: dict[str, int],
            work_status: dict[str, int],
        ) -> None:
            """Display outage and work-order summaries."""

            tk.Label(
                parent,
                text="Operational Status",
                font=(self.FONT, 14, "bold"),
                bg=self.WHITE,
                fg=self.TEXT,
            ).pack(
                anchor="w",
                padx=20,
                pady=(18, 17),
            )

            tk.Label(
                parent,
                text="OUTAGE SEVERITY",
                font=(self.FONT, 8, "bold"),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(
                anchor="w",
                padx=20,
            )

            severity_colors = {
                "Critical": self.RED,
                "High": "#E76F51",
                "Medium": self.ORANGE,
                "Low": self.GREEN,
            }

            for level in (
                "Critical",
                "High",
                "Medium",
                "Low",
            ):
                self._status_row(
                    parent,
                    level,
                    severity.get(level, 0),
                    severity_colors[level],
                )

            tk.Frame(
                parent,
                bg=self.BORDER,
                height=1,
            ).pack(
                fill=tk.X,
                padx=20,
                pady=16,
            )

            tk.Label(
                parent,
                text="WORK ORDERS",
                font=(self.FONT, 8, "bold"),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(
                anchor="w",
                padx=20,
            )

            work_colors = {
                "Pending": self.ORANGE,
                "Assigned": self.PURPLE,
                "In Progress": self.ACCENT,
                "Completed": self.GREEN,
                "Cancelled": self.RED,
            }

            for status in (
                "Pending",
                "Assigned",
                "In Progress",
                "Completed",
            ):
                self._status_row(
                    parent,
                    status,
                    work_status.get(status, 0),
                    work_colors[status],
                )

        def _status_row(
            self,
            parent: object,
            label: str,
            value: int,
            accent: str,
        ) -> None:
            """Create one status row."""

            row = tk.Frame(
                parent,
                bg=self.WHITE,
            )

            row.pack(
                fill=tk.X,
                padx=20,
                pady=6,
            )

            tk.Label(
                row,
                text="●",
                font=(self.FONT, 9),
                bg=self.WHITE,
                fg=accent,
            ).pack(side=tk.LEFT)

            tk.Label(
                row,
                text=label,
                font=(self.FONT, 9),
                bg=self.WHITE,
                fg=self.TEXT,
            ).pack(
                side=tk.LEFT,
                padx=8,
            )

            tk.Label(
                row,
                text=str(value),
                font=(self.FONT, 10, "bold"),
                bg=self.WHITE,
                fg=self.TEXT,
            ).pack(side=tk.RIGHT)

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
