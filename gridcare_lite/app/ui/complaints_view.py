"""Complaints view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from gridcare_lite.app.ui.tk_compat import (
    require_tkinter,
    tk,
    ttk,
    messagebox,
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
            super().__init__(parent)

            self._on_back = on_back

            # -------------------------
            # HEADER
            # -------------------------
            tk.Label(
                self,
                text="Customer Complaints",
                font=("Arial", 20, "bold"),
            ).pack(pady=(15, 5))

            tk.Label(
                self,
                text="Log and review customer complaints",
                font=("Arial", 11),
            ).pack(pady=(0, 10))

            # -------------------------
            # FORM
            # -------------------------
            form_frame = tk.Frame(self)
            form_frame.pack(pady=10)

            tk.Label(
                form_frame,
                text="Customer Name:",
                font=("Arial", 10, "bold"),
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=5,
                sticky="e",
            )

            self.customer_name_entry = tk.Entry(
                form_frame,
                width=35,
            )
            self.customer_name_entry.grid(
                row=0,
                column=1,
                padx=5,
                pady=5,
            )

            tk.Label(
                form_frame,
                text="Complaint Details:",
                font=("Arial", 10, "bold"),
            ).grid(
                row=1,
                column=0,
                padx=5,
                pady=5,
                sticky="ne",
            )

            self.details_text = tk.Text(
                form_frame,
                width=35,
                height=5,
            )
            self.details_text.grid(
                row=1,
                column=1,
                padx=5,
                pady=5,
            )

            tk.Label(
                form_frame,
                text="Outage ID (optional):",
                font=("Arial", 10, "bold"),
            ).grid(
                row=2,
                column=0,
                padx=5,
                pady=5,
                sticky="e",
            )

            self.outage_id_entry = tk.Entry(
                form_frame,
                width=35,
            )
            self.outage_id_entry.grid(
                row=2,
                column=1,
                padx=5,
                pady=5,
            )

            # -------------------------
            # BUTTONS
            # -------------------------
            button_frame = tk.Frame(self)
            button_frame.pack(pady=10)

            tk.Button(
                button_frame,
                text="Submit Complaint",
                width=20,
                command=self._submit_complaint,
            ).grid(
                row=0,
                column=0,
                padx=5,
            )

            tk.Button(
                button_frame,
                text="Clear",
                width=12,
                command=self._clear_form,
            ).grid(
                row=0,
                column=1,
                padx=5,
            )

            # -------------------------
            # COMPLAINT LIST
            # -------------------------
            tk.Label(
                self,
                text="Existing Complaints",
                font=("Arial", 14, "bold"),
            ).pack(pady=(15, 8))

            table_frame = tk.Frame(self)
            table_frame.pack(
                fill=tk.BOTH,
                expand=True,
                padx=20,
                pady=5,
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
                table_frame,
                columns=columns,
                show="headings",
                height=8,
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
                text="Details",
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
                width=50,
                anchor="center",
            )
            self.tree.column(
                "customer",
                width=130,
            )
            self.tree.column(
                "details",
                width=280,
            )
            self.tree.column(
                "outage",
                width=75,
                anchor="center",
            )
            self.tree.column(
                "status",
                width=100,
                anchor="center",
            )
            self.tree.column(
                "created",
                width=150,
                anchor="center",
            )

            scrollbar = ttk.Scrollbar(
                table_frame,
                orient="vertical",
                command=self.tree.yview,
            )

            self.tree.configure(
                yscrollcommand=scrollbar.set,
            )

            self.tree.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
            )

            scrollbar.pack(
                side=tk.RIGHT,
                fill=tk.Y,
            )

            # -------------------------
            # BACK BUTTON
            # -------------------------
            tk.Button(
                self,
                text="Back to Dashboard",
                width=20,
                command=self._on_back,
            ).pack(pady=15)

            self._load_complaints()

        # -------------------------
        # LOAD COMPLAINTS
        # -------------------------

        def _load_complaints(self) -> None:
            """Load complaints from the database."""

            for item in self.tree.get_children():
                self.tree.delete(item)

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

        # -------------------------
        # SUBMIT COMPLAINT
        # -------------------------

        def _submit_complaint(self) -> None:
            """Save a new complaint to the database."""

            customer_name = self.customer_name_entry.get().strip()

            details = self.details_text.get(
                "1.0",
                tk.END,
            ).strip()

            outage_id_text = self.outage_id_entry.get().strip()

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

                    # Check that the outage exists if one was supplied.
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

                    # Generate the required created_at value.
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

        # -------------------------
        # CLEAR FORM
        # -------------------------

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