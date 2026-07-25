"""Main Tkinter application window for GridCare-Lite."""

from __future__ import annotations

from gridcare_lite.app.config import GridCareConfig
from gridcare_lite.app.ui.dashboard_view import DashboardView
from gridcare_lite.app.ui.login_view import LoginView
from gridcare_lite.app.ui.tk_compat import require_tkinter, tk

if tk is not None:

    class GridCareApplication(tk.Tk):
        """Tkinter app container for the starter prototype."""

        def __init__(self, config: GridCareConfig) -> None:
            super().__init__()
            self.title("GridCare-Lite")
            self.geometry("640x420")
            self._config = config
            self._active_frame: object | None = None
            self.show_login()

        def show_login(self) -> None:
            """Render the login view."""
            self._swap_frame(LoginView(self, self._config, self.show_dashboard))

        def show_dashboard(self, username: str) -> None:
            """Render the dashboard view."""
            self._swap_frame(DashboardView(self, username))

        def _swap_frame(self, frame: object) -> None:
            if self._active_frame is not None:
                self._active_frame.destroy()
            self._active_frame = frame
            self._active_frame.pack(fill=tk.BOTH, expand=True)

else:

    class GridCareApplication:  # pragma: no cover - environment-specific
        """Fallback class used when tkinter is unavailable."""

        def __init__(self, *args: object, **kwargs: object) -> None:
            _ = args, kwargs
            require_tkinter()
