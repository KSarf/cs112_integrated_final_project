"""Login view for GridCare-Lite."""

from __future__ import annotations

from collections.abc import Callable

from gridcare_lite.app.config import GridCareConfig
from gridcare_lite.app.services.auth_service import AuthService
from gridcare_lite.app.ui.tk_compat import messagebox, require_tkinter, tk

if tk is not None:

    class LoginView(tk.Frame):
        """Login screen for GridCare-Lite."""

        BG = "#F5F7FA"
        NAVY = "#102A43"
        BLUE = "#168AAD"
        DARK = "#172B4D"
        MUTED = "#627D98"
        BORDER = "#D9E2EC"
        WHITE = "#FFFFFF"

        def __init__(
            self,
            parent: object,
            config: GridCareConfig,
            on_success: Callable[[str], None],
        ) -> None:
            super().__init__(parent, bg=self.BG)

            self._config = config
            self._on_success = on_success

            self._build_interface()

        def _build_interface(self) -> None:
            """Build the login interface."""

            # Main container
            container = tk.Frame(
                self,
                bg=self.BG,
            )
            container.pack(
                fill=tk.BOTH,
                expand=True,
            )

            # Login card
            card = tk.Frame(
                container,
                bg=self.WHITE,
                highlightbackground=self.BORDER,
                highlightthickness=1,
                width=430,
                height=510,
            )
            card.place(
                relx=0.5,
                rely=0.5,
                anchor="center",
            )
            card.pack_propagate(False)

            # Logo
            logo = tk.Label(
                card,
                text="⚡",
                font=("Segoe UI", 32, "bold"),
                bg=self.WHITE,
                fg=self.BLUE,
            )
            logo.pack(pady=(35, 5))

            # Brand name
            tk.Label(
                card,
                text="GRIDCARE",
                font=("Segoe UI", 23, "bold"),
                bg=self.WHITE,
                fg=self.NAVY,
            ).pack()

            tk.Label(
                card,
                text="LITE",
                font=("Segoe UI", 9, "bold"),
                bg=self.WHITE,
                fg=self.BLUE,
            ).pack(pady=(0, 8))

            # Description
            tk.Label(
                card,
                text="Grid Infrastructure Management System",
                font=("Segoe UI", 10),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(pady=(0, 28))

            # Username label
            tk.Label(
                card,
                text="USERNAME",
                font=("Segoe UI", 9, "bold"),
                bg=self.WHITE,
                fg=self.DARK,
            ).pack(
                anchor="w",
                padx=55,
            )

            self.username_entry = tk.Entry(
                card,
                font=("Segoe UI", 11),
                bg="#F8FAFC",
                fg=self.DARK,
                relief=tk.FLAT,
                highlightbackground=self.BORDER,
                highlightcolor=self.BLUE,
                highlightthickness=1,
                insertbackground=self.DARK,
            )
            self.username_entry.pack(
                fill=tk.X,
                padx=55,
                ipady=9,
                pady=(6, 18),
            )

            # Password label
            tk.Label(
                card,
                text="PASSWORD",
                font=("Segoe UI", 9, "bold"),
                bg=self.WHITE,
                fg=self.DARK,
            ).pack(
                anchor="w",
                padx=55,
            )

            self.password_entry = tk.Entry(
                card,
                font=("Segoe UI", 11),
                show="•",
                bg="#F8FAFC",
                fg=self.DARK,
                relief=tk.FLAT,
                highlightbackground=self.BORDER,
                highlightcolor=self.BLUE,
                highlightthickness=1,
                insertbackground=self.DARK,
            )
            self.password_entry.pack(
                fill=tk.X,
                padx=55,
                ipady=9,
                pady=(6, 25),
            )

            # Sign-in button
            self.sign_in_button = tk.Button(
                card,
                text="Sign In",
                command=self._attempt_login,
                font=("Segoe UI", 11, "bold"),
                bg=self.NAVY,
                fg=self.WHITE,
                activebackground=self.BLUE,
                activeforeground=self.WHITE,
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
            )
            self.sign_in_button.pack(
                fill=tk.X,
                padx=55,
                ipady=9,
            )

            # Footer
            tk.Label(
                card,
                text="Secure access to GridCare operations",
                font=("Segoe UI", 9),
                bg=self.WHITE,
                fg=self.MUTED,
            ).pack(pady=(22, 0))

            # Enter key support
            self.username_entry.focus_set()
            self.username_entry.bind(
                "<Return>",
                lambda event: self._attempt_login(),
            )

            self.password_entry.bind(
                "<Return>",
                lambda event: self._attempt_login(),
            )

        def _attempt_login(self) -> None:
            """Check login credentials."""

            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()

            if not username or not password:
                if messagebox is not None:
                    messagebox.showwarning(
                        "Missing information",
                        "Please enter your username and password.",
                    )
                return

            auth_service = AuthService(self._config.database_path)

            user = auth_service.authenticate(
                username,
                password,
            )

            if user is not None:
                self._on_success(user.username)
                return

            if messagebox is not None:
                messagebox.showwarning(
                    "Login failed",
                    "Invalid username or password.",
                )

else:

    class LoginView:  # pragma: no cover
        """Fallback when Tkinter is unavailable."""

        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()
