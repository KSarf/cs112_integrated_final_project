"""Complaints view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from gridcare_lite.app.ui.tk_compat import (
    messagebox,
    require_tkinter,
    tk,
    ttk,
)

DATABASE_PATH = Path("gridcare_lite/database/gridcare.db")


if tk is not None:

    class ComplaintsView(tk.Frame):
        """Display and manage customer complaints."""

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
            self._build_form()
            self._build_complaints_section()
            self._load_complaints()

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
                rowheight=34,
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
                pady=(28, 10),
            )

            back_button = tk.Button(
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
            )
            back_button.pack(
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
                text="Customer Complaints",
                font=("Segoe UI Semibold", 24),
                fg="#182230",
                bg="#F7F9FC",
            ).pack(
                anchor="w",
            )

            tk.Label(
                title_area,
                text="Log and review customer complaints",
                font=("Segoe UI", 10),
                fg="#667085",
                bg="#F7F9FC",
            ).pack(
                anchor="w",
                pady=(3, 0),
            )

        def _build_form(self) -> None:
            """Create the complaint submission form."""

            form_card = tk.Frame(
                self,
                bg="#FFFFFF",
                highlightbackground="#E4E7EC",
                highlightthickness=1,
            )
            form_card.pack(
                fill=tk.X,
                padx=35,
                pady=(10, 18),
            )

            tk.Label(
                form_card,
                text="Submit a Complaint",
                font=("Segoe UI Semibold", 14),
                fg="#182230",
                bg="#FFFFFF",
            ).grid(
                row=0,
                column=0,
                columnspan=2,
                sticky="w",
                padx=22,
                pady=(18, 14),
            )

            tk.Label(
                form_card,
                text="Customer Name",
                font=("Segoe UI Semibold", 10),
                fg="#344054",
                bg="#FFFFFF",
            ).grid(
                row=1,
                column=0,
                sticky="w",
                padx=(22, 10),
                pady=6,
            )

            self.customer_name_entry = tk.Entry(
                form_card,
                font=("Segoe UI", 10),
                width=32,
                relief="solid",
                bd=1,
                bg="#FFFFFF",
                fg="#1D2939",
                insertbackground="#1D2939",
            )
            self.customer_name_entry.grid(
                row=1,
                column=1,
                sticky="ew",
                padx=(0, 22),
                pady=6,
                ipady=7,
            )

            tk.Label(
                form_card,
                text="Complaint Details",
                font=("Segoe UI Semibold", 10),
                fg="#344054",
                bg="#FFFFFF",
            ).grid(
                row=2,
                column=0,
                sticky="nw",
                padx=(22, 10),
                pady=6,
            )

            self.details_text = tk.Text(
                form_card,
                font=("Segoe UI", 10),
                width=32,
                height=4,
                relief="solid",
                bd=1,
                bg="#FFFFFF",
                fg="#1D2939",
                insertbackground="#1D2939",
                wrap=tk.WORD,
            )
            self.details_text.grid(
                row=2,
                column=1,
                sticky="ew",
                padx=(0, 22),
                pady=6,
            )

            tk.Label(
                form_card,
                text="Outage ID",
                font=("Segoe UI Semibold", 10),
                fg="#344054",
                bg="#FFFFFF",
            ).grid(
                row=3,
                column=0,
                sticky="w",
                padx=(22, 10),
                pady=6,
            )

            self.outage_id_entry = tk.Entry(
                form_card,
                font=("Segoe UI", 10),
                width=32,
                relief="solid",
                bd=1,
                bg="#FFFFFF",
                fg="#1D2939",
                insertbackground="#1D2939",
            )
            self.outage_id_entry.grid(
                row=3,
                column=1,
                sticky="ew",
                padx=(0, 22),
                pady=6,
                ipady=7,
            )

            tk.Label(
                form_card,
                text="Optional",
                font=("Segoe UI", 9),
                fg="#98A2B3",
                bg="#FFFFFF",
            ).grid(
                row=3,
                column=2,
                sticky="w",
                padx=(0, 10),
            )

            button_area = tk.Frame(
                form_card,
                bg="#FFFFFF",
            )
            button_area.grid(
                row=4,
                column=0,
                columnspan=3,
                sticky="w",
                padx=22,
                pady=(12, 20),
            )

            tk.Button(
                button_area,
                text="Submit Complaint",
                command=self._submit_complaint,
                font=("Segoe UI Semibold", 10),
                bg="#2563EB",
                fg="#FFFFFF",
                activebackground="#1D4ED8",
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                padx=20,
                pady=9,
                cursor="hand2",
            ).pack(
                side=tk.LEFT,
                padx=(0, 8),
            )

            tk.Button(
                button_area,
                text="Clear",
                command=self._clear_form,
                font=("Segoe UI Semibold", 10),
                bg="#F2F4F7",
                fg="#344054",
                activebackground="#E4E7EC",
                activeforeground="#1D2939",
                relief="flat",
                bd=0,
                padx=20,
                pady=9,
                cursor="hand2",
            ).pack(
                side=tk.LEFT,
            )

            form_card.columnconfigure(
                1,
                weight=1,
            )

        def _build_complaints_section(self) -> None:
            """Create the expandable complaints table."""

            section = tk.Frame(
                self,
                bg="#F7F9FC",
            )
            section.pack(
                fill=tk.BOTH,
                expand=True,
                padx=35,
                pady=(0, 18),
            )

            section_title = tk.Frame(
                section,
                bg="#F7F9FC",
            )
            section_title.pack(
                fill=tk.X,
                pady=(0, 8),
            )

            tk.Label(
                section_title,
                text="Existing Complaints",
                font=("Segoe UI Semibold", 15),
                fg="#182230",
                bg="#F7F9FC",
            ).pack(
                side=tk.LEFT,
            )

            self.complaint_count_label = tk.Label(
                section_title,
                text="",
                font=("Segoe UI", 9),
                fg="#667085",
                bg="#F7F9FC",
            )
            self.complaint_count_label.pack(
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
                "customer",
                "details",
                "outage",
                "status",
                "created",
            )

            self.tree = ttk.Treeview(
                table_container,
                columns=columns,
                show="headings",
                style="GridCare.Treeview",
                selectmode="browse",
            )

            self.tree.heading(
                "id",
                text="ID",
            )
            self.tree.heading(
                "customer",
                text="Customer",
            )
            self.tree.heading(
                "details",
                text="Complaint Details",
            )
            self.tree.heading(
                "outage",
                text="Outage ID",
            )
            self.tree.heading(
                "status",
                text="Status",
            )
            self.tree.heading(
                "created",
                text="Created At",
            )

            self.tree.column(
                "id",
                width=60,
                minwidth=50,
                anchor=tk.CENTER,
                stretch=False,
            )

            self.tree.column(
                "customer",
                width=160,
                minwidth=120,
                anchor=tk.W,
                stretch=False,
            )

            self.tree.column(
                "details",
                width=420,
                minwidth=250,
                anchor=tk.W,
                stretch=True,
            )

            self.tree.column(
                "outage",
                width=100,
                minwidth=80,
                anchor=tk.CENTER,
                stretch=False,
            )

            self.tree.column(
                "status",
                width=110,
                minwidth=90,
                anchor=tk.CENTER,
                stretch=False,
            )

            self.tree.column(
                "created",
                width=180,
                minwidth=150,
                anchor=tk.CENTER,
                stretch=False,
            )

            vertical_scrollbar = ttk.Scrollbar(
                table_container,
                orient=tk.VERTICAL,
                command=self.tree.yview,
                style="GridCare.Vertical.TScrollbar",
            )

            horizontal_scrollbar = ttk.Scrollbar(
                table_container,
                orient=tk.HORIZONTAL,
                command=self.tree.xview,
                style="GridCare.Horizontal.TScrollbar",
            )

            self.tree.configure(
                yscrollcommand=vertical_scrollbar.set,
                xscrollcommand=horizontal_scrollbar.set,
            )

            self.tree.grid(
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

        def _load_complaints(self) -> None:
            """Load complaints from the database."""

            for item in self.tree.get_children():
                self.tree.delete(item)

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        SELECT
                            id,
                            customer_name,
                            details,
                            outage_id,
                            status,
                            created_at
                        FROM complaints
                        ORDER BY id DESC
                        """
                    )

                    complaints = cursor.fetchall()

                for complaint in complaints:
                    (
                        complaint_id,
                        customer,
                        details,
                        outage_id,
                        status,
                        created_at,
                    ) = complaint

                    self.tree.insert(
                        "",
                        tk.END,
                        values=(
                            complaint_id,
                            customer,
                            details,
                            outage_id if outage_id is not None else "-",
                            status,
                            created_at,
                        ),
                    )

                count = len(complaints)

                if count == 1:
                    text = "1 complaint"
                else:
                    text = f"{count} complaints"

                self.complaint_count_label.config(
                    text=text,
                )

            except sqlite3.Error as error:
                self.complaint_count_label.config(
                    text="Unable to load complaints",
                )

                messagebox.showerror(
                    "Database Error",
                    f"Could not load complaints:\n{error}",
                )

        def _submit_complaint(self) -> None:
            """Save a new complaint to the database."""

            customer_name = (
                self.customer_name_entry
                .get()
                .strip()
            )

            details = (
                self.details_text
                .get(
                    "1.0",
                    tk.END,
                )
                .strip()
            )

            outage_id_text = (
                self.outage_id_entry
                .get()
                .strip()
            )

            if not customer_name:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter the customer's name.",
                )
                return

            if not details:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter the complaint details.",
                )
                return

            outage_id = None

            if outage_id_text:
                try:
                    outage_id = int(outage_id_text)
                except ValueError:
                    messagebox.showwarning(
                        "Invalid Outage ID",
                        "Outage ID must be a number.",
                    )
                    return

            try:
                with sqlite3.connect(DATABASE_PATH) as connection:
                    cursor = connection.cursor()

                    if outage_id is not None:
                        cursor.execute(
                            "SELECT id FROM outages WHERE id = ?",
                            (outage_id,),
                        )

                        if cursor.fetchone() is None:
                            messagebox.showwarning(
                                "Invalid Outage",
                                f"Outage ID {outage_id} does not exist.",
                            )
                            return

                    created_at = datetime.now().isoformat(
                        timespec="seconds"
                    )

                    cursor.execute(
                        """
                        INSERT INTO complaints
                        (
                            customer_name,
                            details,
                            outage_id,
                            status,
                            created_at
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            customer_name,
                            details,
                            outage_id,
                            "Open",
                            created_at,
                        ),
                    )

                    connection.commit()

                messagebox.showinfo(
                    "Complaint Submitted",
                    "The complaint was successfully submitted.",
                )

                self._clear_form()
                self._load_complaints()

            except sqlite3.Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not save the complaint:\n{error}",
                )

        def _clear_form(self) -> None:
            """Clear all complaint form fields."""

            self.customer_name_entry.delete(
                0,
                tk.END,
            )

            self.details_text.delete(
                "1.0",
                tk.END,
            )

            self.outage_id_entry.delete(
                0,
                tk.END,
            )

            self.customer_name_entry.focus_set()


else:

    class ComplaintsView:  # pragma: no cover
        """Fallback when Tkinter is unavailable."""

        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()