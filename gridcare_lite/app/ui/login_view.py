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
                text="GridCare-Lite Login",
                font=("Arial", 16, "bold"),
            ).pack(pady=15)

            tk.Label(
                self,
                text="Username",
            ).pack()

            self.username_entry = tk.Entry(self)
            self.username_entry.pack(pady=5)

            tk.Label(
                self,
                text="Password",
            ).pack()

            self.password_entry = tk.Entry(
                self,
                show="*",
            )
            self.password_entry.pack(pady=5)

            tk.Button(
                self,
                text="Login",
                command=self._attempt_login,
            ).pack(pady=15)

        def _attempt_login(self) -> None:
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()

            if (
                self._config.enable_demo_login
                and username == "demo"
                and password == "demo"
            ):
                self._on_success(username)
                return

            assert messagebox is not None

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