"""Work orders view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from pathlib import Path

from gridcare_lite.app.security.permissions import has_permission
from gridcare_lite.app.services.work_order_service import WorkOrderService
from gridcare_lite.app.ui.tk_compat import messagebox, require_tkinter, tk, ttk

DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


if tk is not None:

    class WorkOrdersView(tk.Frame):
        """Display and manage GridCare work orders."""

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
            ).pack(anchor="w")

            if has_permission(self._role, "update_work_orders"):
                description = "View and update work assigned to you."
            else:
                description = (
                    "Manage and monitor maintenance work assigned to grid teams."
                )

            tk.Label(
                header,
                text=description,
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
                selectmode="browse",
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
                width=120,
                minwidth=100,
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
                width=300,
                minwidth=200,
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
                width=150,
                minwidth=110,
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

            if has_permission(self._role, "create_work_orders"):
                tk.Button(
                    footer,
                    text="Create Work Order",
                    command=self._create_work_order_dialog,
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

            if has_permission(self._role, "update_work_orders"):
                tk.Button(
                    footer,
                    text="Start Selected",
                    command=self._start_selected,
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
                    text="Complete Selected",
                    command=self._complete_selected,
                    bg="#2A9D8F",
                    fg="white",
                    activebackground="#23867A",
                    activeforeground="white",
                    relief=tk.FLAT,
                    bd=0,
                    font=("Segoe UI Semibold", 10),
                    padx=18,
                    pady=9,
                    cursor="hand2",
                ).pack(
                    side=tk.LEFT,
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

        def _create_work_order_dialog(self) -> None:
            """Open the work-order creation form."""

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    cursor.execute("""
                        SELECT id, title
                        FROM outages
                        WHERE status = 'Under Review'
                        ORDER BY id
                        """)
                    outages = cursor.fetchall()

                    cursor.execute("""
                        SELECT id, username
                        FROM users
                        WHERE role = 'Technician'
                        ORDER BY username
                        """)
                    technicians = cursor.fetchall()

            except sqlite3.Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not load work-order information:\n{error}",
                )
                return

            if not outages:
                messagebox.showwarning(
                    "No Reviewed Outages",
                    "There are no outages ready for assignment.",
                )
                return

            if not technicians:
                messagebox.showwarning(
                    "No Technicians",
                    "There are no technician accounts available.",
                )
                return

            window = tk.Toplevel(self)
            window.title("Create Work Order")
            window.geometry("480x430")
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
                text="Create Work Order",
                font=("Segoe UI Semibold", 18),
                bg="white",
                fg="#111827",
            ).pack(
                anchor="w",
                pady=(0, 15),
            )

            tk.Label(
                form,
                text="Outage",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            outage_var = tk.StringVar()

            outage_values = [f"{outage_id} - {title}" for outage_id, title in outages]

            outage_box = ttk.Combobox(
                form,
                textvariable=outage_var,
                values=outage_values,
                state="readonly",
            )
            outage_box.pack(
                fill=tk.X,
                pady=(4, 12),
            )
            outage_box.current(0)

            tk.Label(
                form,
                text="Technician",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            technician_var = tk.StringVar()

            technician_values = [
                f"{technician_id} - {username}"
                for technician_id, username in technicians
            ]

            technician_box = ttk.Combobox(
                form,
                textvariable=technician_var,
                values=technician_values,
                state="readonly",
            )
            technician_box.pack(
                fill=tk.X,
                pady=(4, 12),
            )
            technician_box.current(0)

            tk.Label(
                form,
                text="Scheduled Date",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            scheduled_entry = tk.Entry(
                form,
                font=("Segoe UI", 10),
            )
            scheduled_entry.pack(
                fill=tk.X,
                pady=(4, 12),
            )

            tk.Label(
                form,
                text="Instructions",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            instructions_text = tk.Text(
                form,
                height=6,
                font=("Segoe UI", 10),
            )
            instructions_text.pack(
                fill=tk.X,
                pady=(4, 15),
            )

            def save_work_order() -> None:
                outage_id = int(
                    outage_var.get().split(
                        " - ",
                        1,
                    )[0]
                )

                technician_id = int(
                    technician_var.get().split(
                        " - ",
                        1,
                    )[0]
                )

                scheduled_date = scheduled_entry.get().strip()

                instructions = instructions_text.get(
                    "1.0",
                    tk.END,
                ).strip()

                service = WorkOrderService(DATABASE_PATH)

                try:
                    service.create_work_order(
                        outage_id=outage_id,
                        technician_id=technician_id,
                        scheduled_date=scheduled_date,
                        instructions=instructions,
                        changed_by=self._user_id,
                    )

                except ValueError as error:
                    messagebox.showwarning(
                        "Work Order",
                        str(error),
                    )
                    return

                except sqlite3.Error as error:
                    messagebox.showerror(
                        "Database Error",
                        f"Could not create work order:\n{error}",
                    )
                    return

                messagebox.showinfo(
                    "Work Order Created",
                    "The technician has been assigned.",
                )

                window.destroy()
                self.load_work_orders()

            tk.Button(
                form,
                text="Create Work Order",
                command=save_work_order,
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

        def _start_selected(self) -> None:
            """Start the selected technician work order."""

            selected = self.table.selection()

            if not selected:
                messagebox.showwarning(
                    "Select Work Order",
                    "Please select a work order first.",
                )
                return

            values = self.table.item(
                selected[0],
                "values",
            )

            work_order_id = int(values[0])

            service = WorkOrderService(DATABASE_PATH)

            try:
                service.start_work(
                    work_order_id=work_order_id,
                    technician_id=self._user_id,
                )

            except (ValueError, PermissionError) as error:
                messagebox.showwarning(
                    "Work Order",
                    str(error),
                )
                return

            except sqlite3.Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not start work:\n{error}",
                )
                return

            messagebox.showinfo(
                "Work Started",
                "The work order is now In Progress.",
            )

            self.load_work_orders()

        def _complete_selected(self) -> None:
            """Open a form to complete the selected work order."""

            selected = self.table.selection()

            if not selected:
                messagebox.showwarning(
                    "Select Work Order",
                    "Please select a work order first.",
                )
                return

            values = self.table.item(
                selected[0],
                "values",
            )

            work_order_id = int(values[0])

            window = tk.Toplevel(self)
            window.title("Complete Work Order")
            window.geometry("430x280")
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
                text="Complete Work Order",
                font=("Segoe UI Semibold", 18),
                bg="white",
                fg="#111827",
            ).pack(
                anchor="w",
                pady=(0, 12),
            )

            tk.Label(
                form,
                text="Resolution Notes",
                bg="white",
                fg="#374151",
            ).pack(anchor="w")

            resolution_text = tk.Text(
                form,
                height=6,
                font=("Segoe UI", 10),
            )
            resolution_text.pack(
                fill=tk.X,
                pady=(4, 15),
            )

            def save_completion() -> None:
                resolution_notes = resolution_text.get(
                    "1.0",
                    tk.END,
                ).strip()

                service = WorkOrderService(DATABASE_PATH)

                try:
                    service.complete_work(
                        work_order_id=work_order_id,
                        technician_id=self._user_id,
                        resolution_notes=resolution_notes,
                    )

                except (ValueError, PermissionError) as error:
                    messagebox.showwarning(
                        "Work Order",
                        str(error),
                    )
                    return

                except sqlite3.Error as error:
                    messagebox.showerror(
                        "Database Error",
                        f"Could not complete work:\n{error}",
                    )
                    return

                messagebox.showinfo(
                    "Work Completed",
                    "The work order is complete and the outage is resolved.",
                )

                window.destroy()
                self.load_work_orders()

            tk.Button(
                form,
                text="Complete Work",
                command=save_completion,
                bg="#2A9D8F",
                fg="white",
                activebackground="#23867A",
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

        def load_work_orders(self) -> None:
            """Load work orders from the SQLite database."""

            for item in self.table.get_children():
                self.table.delete(item)

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    if has_permission(
                        self._role,
                        "update_work_orders",
                    ):
                        cursor.execute(
                            """
                            SELECT
                                work_orders.id,
                                work_orders.outage_id,
                                users.username,
                                work_orders.scheduled_date,
                                work_orders.status,
                                work_orders.instructions,
                                work_orders.resolution_notes,
                                work_orders.completed_at
                            FROM work_orders
                            LEFT JOIN users
                                ON work_orders.assigned_to = users.id
                            WHERE work_orders.assigned_to = ?
                            ORDER BY work_orders.id
                            """,
                            (self._user_id,),
                        )

                    else:
                        cursor.execute("""
                            SELECT
                                work_orders.id,
                                work_orders.outage_id,
                                users.username,
                                work_orders.scheduled_date,
                                work_orders.status,
                                work_orders.instructions,
                                work_orders.resolution_notes,
                                work_orders.completed_at
                            FROM work_orders
                            LEFT JOIN users
                                ON work_orders.assigned_to = users.id
                            ORDER BY work_orders.id
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
