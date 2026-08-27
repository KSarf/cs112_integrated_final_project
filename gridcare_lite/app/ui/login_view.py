"""Login view for GridCare-Lite."""

from __future__ import annotations

from collections.abc import Callable

from gridcare_lite.app.config import GridCareConfig
from gridcare_lite.app.ui.tk_compat import messagebox, require_tkinter, tk


if tk is not None:

    class LoginView(tk.Frame):
        """Login screen for GridCare-Lite."""

        def __init__(
            self,
            parent: object,
            config: GridCareConfig,
            on_success: Callable[[str], None],
        ) -> None:
            super().__init__(parent)

            self._config = config
            self._on_success = on_success

            tk.Label(
                self,
                text="GridCare-Lite",
                font=("Arial", 24, "bold"),
            ).pack(pady=(35, 5))

            tk.Label(
                self,
                text="Grid Infrastructure Management System",
                font=("Arial", 11),
            ).pack(pady=(0, 25))

            tk.Label(
                self,
                text="Username",
                font=("Arial", 10, "bold"),
            ).pack()

            self.username_entry = tk.Entry(self, width=30)
            self.username_entry.pack(pady=5)

            tk.Label(
                self,
                text="Password",
                font=("Arial", 10, "bold"),
            ).pack(pady=(10, 0))

            self.password_entry = tk.Entry(
                self,
                width=30,
                show="*",
            )
            self.password_entry.pack(pady=5)

            tk.Button(
                self,
                text="Login",
                width=20,
                command=self._attempt_login,
            ).pack(pady=20)

            tk.Label(
                self,
                text="Demo login: demo / demo",
                font=("Arial", 9),
            ).pack(pady=5)

        def _attempt_login(self) -> None:
            """Check login credentials."""

            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()

            if username == "demo" and password == "demo":
                self._on_success(username)
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