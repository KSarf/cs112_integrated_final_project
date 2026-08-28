"""Outages view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from gridcare_lite.app.security.permissions import has_permission
from gridcare_lite.app.services.outage_service import OutageService
from gridcare_lite.app.ui.tk_compat import messagebox, require_tkinter, tk, ttk

DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


if tk is not None:

    class OutagesView(tk.Frame):
        """Display and manage reported grid outages."""

        def __init__(
            self,
            parent: object,
            on_back: Callable[[], None],
            user_id: int,
            role: str,
        ) -> None:
            super().__init__(parent)

            self._on_back = on_back
            self._user_id = user_id
            self._role = role

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
                selectmode="browse",
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

            if has_permission(self._role, "create_outages"):
                tk.Button(
                    footer,
                    text="Log Outage",
                    command=self._create_outage_dialog,
                    bg="#168AAD",
                    fg="white",
                    activebackground="#126E8A",
                    activeforeground="white",
                    relief=tk.FLAT,
                    bd=0,
                    font=("Segoe UI Semibold", 10),
                    padx=18,
                    pady=9,
                    cursor="hand2",
                ).pack(
                    side=tk.LEFT,
                    padx=(0, 10),
                )

            if has_permission(self._role, "review_outages"):
                tk.Button(
                    footer,
                    text="Review Selected",
                    command=self._review_selected,
                    bg="#168AAD",
                    fg="white",
                    activebackground="#126E8A",
                    activeforeground="white",
                    relief=tk.FLAT,
                    bd=0,
                    font=("Segoe UI Semibold", 10),
                    padx=18,
                    pady=9,
                    cursor="hand2",
                ).pack(
                    side=tk.LEFT,
                    padx=(0, 10),
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

        def _create_outage_dialog(self) -> None:
            """Open a form for reporting an outage."""

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    cursor.execute("""
                        SELECT id, name
                        FROM substations
                        ORDER BY name
                        """)

                    substations = cursor.fetchall()

            except sqlite3.Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not load substations:\n{error}",
                )
                return

            if not substations:
                messagebox.showwarning(
                    "No Substations",
                    "No substations are available.",
                )
                return

            window = tk.Toplevel(self)
            window.title("Log Outage")
            window.geometry("450x430")
            window.resizable(False, False)
            window.configure(bg="white")

            form = tk.Frame(
                window,
                bg="white",
                padx=25,
                pady=20,
            )
            form.pack(
                fill=tk.BOTH,
                expand=True,
            )

            tk.Label(
                form,
                text="Log New Outage",
                font=("Segoe UI Semibold", 18),
                bg="white",
                fg="#111827",
            ).pack(
                anchor="w",
                pady=(0, 15),
            )

            tk.Label(
                form,
                text="Title",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            title_entry = tk.Entry(
                form,
                font=("Segoe UI", 10),
            )
            title_entry.pack(
                fill=tk.X,
                pady=(4, 12),
            )

            tk.Label(
                form,
                text="Substation",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            substation_var = tk.StringVar()

            substation_values = [
                f"{substation_id} - {name}" for substation_id, name in substations
            ]

            substation_box = ttk.Combobox(
                form,
                textvariable=substation_var,
                values=substation_values,
                state="readonly",
            )
            substation_box.pack(
                fill=tk.X,
                pady=(4, 12),
            )
            substation_box.current(0)

            tk.Label(
                form,
                text="Severity",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            severity_var = tk.StringVar(value="Medium")

            severity_box = ttk.Combobox(
                form,
                textvariable=severity_var,
                values=(
                    "Low",
                    "Medium",
                    "High",
                    "Critical",
                ),
                state="readonly",
            )
            severity_box.pack(
                fill=tk.X,
                pady=(4, 12),
            )

            tk.Label(
                form,
                text="Description",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            description_text = tk.Text(
                form,
                height=5,
                font=("Segoe UI", 10),
            )
            description_text.pack(
                fill=tk.X,
                pady=(4, 15),
            )

            def save_outage() -> None:
                title = title_entry.get().strip()

                description = description_text.get(
                    "1.0",
                    tk.END,
                ).strip()

                selected_substation = substation_var.get()

                if not selected_substation:
                    messagebox.showwarning(
                        "Missing Information",
                        "Please select a substation.",
                    )
                    return

                substation_id = int(
                    selected_substation.split(
                        " - ",
                        1,
                    )[0]
                )

                service = OutageService(DATABASE_PATH)

                try:
                    service.create_outage(
                        title=title,
                        description=description,
                        substation_id=substation_id,
                        severity=severity_var.get(),
                        reported_at=datetime.now().isoformat(timespec="seconds"),
                        reported_by=self._user_id,
                    )

                except ValueError as error:
                    messagebox.showwarning(
                        "Outage",
                        str(error),
                    )
                    return

                except sqlite3.Error as error:
                    messagebox.showerror(
                        "Database Error",
                        f"Could not save outage:\n{error}",
                    )
                    return

                messagebox.showinfo(
                    "Outage Created",
                    "The outage was successfully reported.",
                )

                window.destroy()
                self.load_outages()

            tk.Button(
                form,
                text="Save Outage",
                command=save_outage,
                bg="#168AAD",
                fg="white",
                activebackground="#126E8A",
                activeforeground="white",
                relief=tk.FLAT,
                bd=0,
                font=("Segoe UI Semibold", 10),
                padx=18,
                pady=9,
                cursor="hand2",
            ).pack(
                anchor="e",
            )

        def _review_selected(self) -> None:
            """Mark the selected outage as Under Review."""

            selected = self.table.selection()

            if not selected:
                messagebox.showwarning(
                    "Select Outage",
                    "Please select an outage first.",
                )
                return

            values = self.table.item(
                selected[0],
                "values",
            )

            outage_id = int(values[0])

            service = OutageService(DATABASE_PATH)

            try:
                service.review_outage(
                    outage_id=outage_id,
                    changed_by=self._user_id,
                    changed_at=datetime.now().isoformat(timespec="seconds"),
                )

            except ValueError as error:
                messagebox.showwarning(
                    "Outage",
                    str(error),
                )
                return

            except sqlite3.Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not review outage:\n{error}",
                )
                return

            messagebox.showinfo(
                "Outage Reviewed",
                "The outage is now Under Review.",
            )

            self.load_outages()

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
