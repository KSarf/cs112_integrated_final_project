"""Login view for GridCare-Lite."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from gridcare_lite.app.config import GridCareConfig


class LoginView(tk.Frame):
    """Starter login view with development-only demo path."""

    def __init__(self, parent: tk.Widget, config: GridCareConfig, on_success: callable) -> None:
        super().__init__(parent)
        self._config = config
        self._on_success = on_success

        tk.Label(self, text="GridCare-Lite Login", font=("Arial", 16, "bold")).pack(pady=8)
        tk.Label(self, text="Prototype notice: Initial prototype, not production-ready.").pack(
            pady=4
        )

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self._attempt_login).pack(pady=10)

    def _attempt_login(self) -> None:
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if self._config.enable_demo_login and username == "demo" and password == "demo":
            self._on_success(username)
            return

        messagebox.showwarning(
            "Login failed",
            "Demo login is disabled or credentials are invalid.",
        )
