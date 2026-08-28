"""Registration view for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable

from gridcare_lite.app.config import GridCareConfig
from gridcare_lite.app.security.passwords import hash_password
from gridcare_lite.app.ui.tk_compat import messagebox, require_tkinter, tk

if tk is not None:

    class RegisterView(tk.Frame):
        """Create a new GridCare-Lite user account."""

        BG = "#F5F7FA"
        NAVY = "#102A43"
        BLUE = "#168AAD"
        DARK = "#172B4D"
        MUTED = "#627D98"
        BORDER = "#D9E2EC"
        WHITE = "#FFFFFF"
        ERROR = "#E63946"

        FONT = "Segoe UI"

        def __init__(
            self,
            parent: object,
            config: GridCareConfig,
            on_registered: Callable[[], None],
            on_back: Callable[[], None],
        ) -> None:
            super().__init__(parent, bg=self.BG)

            self._config = config
            self._on_registered = on_registered
            self._on_back = on_back

            self._build_interface()

        def _build_interface(self) -> None:
            container = tk.Frame(
                self,
                bg=self.BG,
            )

            container.pack(
                fill=tk.BOTH,
                expand=True,
            )

            card = tk.Frame(
                container,
                bg=self.WHITE,
                highlightbackground=self.BORDER,
                highlightthickness=1,
                width=500,
                height=650,
            )

            card.place(
                relx=0.5,
                rely=0.5,
                anchor="center",
            )

            card.pack_propagate(False)

            tk.Label(
                card,
                text="⚡",
                font=(self.FONT, 28, "bold"),
                bg=self.WHITE,
                fg=self.BLUE,
            ).pack(pady=(25, 0))

            tk.Label(
                card,
                text="CREATE ACCOUNT",
                font=(self.FONT, 21, "bold"),
                bg=self.WHITE,
                fg=self.NAVY,
            ).pack(pady=(3, 2))

            tk.Label(
                card,
                text="Register for GridCare-Lite operations",
                font=(self.FONT, 10),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(pady=(0, 18))

            form = tk.Frame(
                card,
                bg=self.WHITE,
            )

            form.pack(
                fill=tk.X,
                padx=55,
            )

            self._add_label(
                form,
                "FULL NAME",
                0,
            )

            self.full_name_entry = self._add_entry(
                form,
                1,
            )

            self._add_label(
                form,
                "EMAIL ADDRESS",
                2,
            )

            self.email_entry = self._add_entry(
                form,
                3,
            )

            self._add_label(
                form,
                "USERNAME",
                4,
            )

            self.username_entry = self._add_entry(
                form,
                5,
            )

            self._add_label(
                form,
                "PASSWORD",
                6,
            )

            self.password_entry = self._add_entry(
                form,
                7,
                show="•",
            )

            self._add_label(
                form,
                "CONFIRM PASSWORD",
                8,
            )

            self.confirm_password_entry = self._add_entry(
                form,
                9,
                show="•",
            )

            self._add_label(
                form,
                "ROLE",
                10,
            )

            self.role_var = tk.StringVar(value="Engineer")

            self.role_menu = tk.OptionMenu(
                form,
                self.role_var,
                "Engineer",
                "Technician",
                "Administrator",
                "Customer-service representative",
            )

            self.role_menu.config(
                font=(self.FONT, 10),
                bg="#F8FAFC",
                fg=self.DARK,
                activebackground="#E8F1F5",
                activeforeground=self.DARK,
                relief=tk.FLAT,
                bd=0,
                highlightthickness=1,
                highlightbackground=self.BORDER,
            )

            self.role_menu["menu"].config(font=(self.FONT, 10))

            self.role_menu.grid(
                row=11,
                column=0,
                sticky="ew",
                pady=(5, 16),
                ipady=5,
            )

            form.grid_columnconfigure(
                0,
                weight=1,
            )

            self.register_button = tk.Button(
                card,
                text="Create Account",
                command=self._register,
                font=(self.FONT, 11, "bold"),
                bg=self.NAVY,
                fg=self.WHITE,
                activebackground=self.BLUE,
                activeforeground=self.WHITE,
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
            )

            self.register_button.pack(
                fill=tk.X,
                padx=55,
                ipady=9,
            )

            tk.Button(
                card,
                text="Back to Sign In",
                command=self._on_back,
                font=(self.FONT, 9, "bold"),
                bg=self.WHITE,
                fg=self.BLUE,
                activebackground=self.WHITE,
                activeforeground=self.NAVY,
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
            ).pack(pady=(12, 0))

            tk.Label(
                card,
                text="Your password is securely encrypted.",
                font=(self.FONT, 8),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(pady=(8, 0))

            self.full_name_entry.focus_set()

        def _add_label(
            self,
            parent: object,
            text: str,
            row: int,
        ) -> None:

            tk.Label(
                parent,
                text=text,
                font=(self.FONT, 8, "bold"),
                bg=self.WHITE,
                fg=self.DARK,
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=(0, 2),
            )

        def _add_entry(
            self,
            parent: object,
            row: int,
            show: str | None = None,
        ) -> tk.Entry:

            entry = tk.Entry(
                parent,
                font=(self.FONT, 10),
                bg="#F8FAFC",
                fg=self.DARK,
                relief=tk.FLAT,
                highlightbackground=self.BORDER,
                highlightcolor=self.BLUE,
                highlightthickness=1,
                insertbackground=self.DARK,
            )

            if show is not None:
                entry.config(show=show)

            entry.grid(
                row=row,
                column=0,
                sticky="ew",
                pady=(0, 10),
                ipady=7,
            )

            return entry

        def _register(self) -> None:
            full_name = self.full_name_entry.get().strip()
            email = self.email_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            role = self.role_var.get()

            if not full_name:
                self._warning("Please enter your full name.")
                return

            if not email:
                self._warning("Please enter your email address.")
                return

            if "@" not in email or "." not in email:
                self._warning("Please enter a valid email address.")
                return

            if not username:
                self._warning("Please choose a username.")
                return

            if len(username) < 3:
                self._warning("Username must contain at least 3 characters.")
                return

            if not password:
                self._warning("Please create a password.")
                return

            if len(password) < 8:
                self._warning("Password must contain at least 8 characters.")
                return

            if password != confirm_password:
                self._warning("Passwords do not match.")
                return

            database_path = self._config.database_path

            try:
                with sqlite3.connect(database_path) as connection:
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        SELECT id
                        FROM users
                        WHERE username = ?
                        """,
                        (username,),
                    )

                    if cursor.fetchone() is not None:
                        self._warning("That username is already in use.")
                        return

                    cursor.execute(
                        """
                        SELECT id
                        FROM users
                        WHERE email = ?
                        """,
                        (email,),
                    )

                    if cursor.fetchone() is not None:
                        self._warning("That email address is already registered.")
                        return

                    password_hash = hash_password(password)

                    cursor.execute(
                        """
                        INSERT INTO users
                        (
                            username,
                            password_hash,
                            role,
                            full_name,
                            email
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            username,
                            password_hash,
                            role,
                            full_name,
                            email,
                        ),
                    )

                    connection.commit()

                if messagebox is not None:
                    messagebox.showinfo(
                        "Account Created",
                        "Your GridCare account has been created successfully.\n\n"
                        "You can now sign in with your username and password.",
                    )

                self._clear_form()
                self._on_registered()

            except sqlite3.Error as error:
                if messagebox is not None:
                    messagebox.showerror(
                        "Registration Error",
                        f"Could not create the account:\n{error}",
                    )

        def _warning(self, message: str) -> None:
            if messagebox is not None:
                messagebox.showwarning(
                    "Registration",
                    message,
                )

        def _clear_form(self) -> None:
            self.full_name_entry.delete(
                0,
                tk.END,
            )

            self.email_entry.delete(
                0,
                tk.END,
            )

            self.username_entry.delete(
                0,
                tk.END,
            )

            self.password_entry.delete(
                0,
                tk.END,
            )

            self.confirm_password_entry.delete(
                0,
                tk.END,
            )

            self.role_var.set("Engineer")

else:

    class RegisterView:  # pragma: no cover

        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()
