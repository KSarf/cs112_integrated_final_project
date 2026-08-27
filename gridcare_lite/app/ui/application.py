"""Main Tkinter application window for GridCare-Lite."""

from __future__ import annotations

from gridcare_lite.app.config import GridCareConfig
from gridcare_lite.app.ui.complaints_view import ComplaintsView
from gridcare_lite.app.ui.dashboard_view import DashboardView
from gridcare_lite.app.ui.login_view import LoginView
from gridcare_lite.app.ui.outages_view import OutagesView
from gridcare_lite.app.ui.substations_view import SubstationsView
from gridcare_lite.app.ui.tk_compat import require_tkinter, tk
from gridcare_lite.app.ui.work_orders_view import WorkOrdersView

if tk is not None:

    class GridCareApplication(tk.Tk):

        def __init__(self, config: GridCareConfig) -> None:
            super().__init__()

            self.title("GridCare-Lite")
            self.geometry("1200x750")
            self.minsize(1000, 650)
            self.configure(bg="#F7F9FC")

            self._config = config
            self._active_frame = None
            self._username = ""

            self.show_login()

        def show_login(self) -> None:
            self._swap_frame(
                LoginView(
                    self,
                    self._config,
                    self.show_dashboard,
                )
            )

        def show_dashboard(self, username: str | None = None) -> None:
            if username is not None:
                self._username = username

            self._swap_frame(
                DashboardView(
                    self,
                    self._username,
                    self.show_substations,
                    self.show_outages,
                    self.show_work_orders,
                    self.show_complaints,
                    self.logout,
                )
            )

        def show_substations(self) -> None:
            self._swap_frame(
                SubstationsView(
                    self,
                    self.show_dashboard,
                )
            )

        def show_outages(self) -> None:
            self._swap_frame(
                OutagesView(
                    self,
                    self.show_dashboard,
                )
            )

        def show_work_orders(self) -> None:
            self._swap_frame(
                WorkOrdersView(
                    self,
                    self.show_dashboard,
                )
            )

        def show_complaints(self) -> None:
            self._swap_frame(
                ComplaintsView(
                    self,
                    self.show_dashboard,
                )
            )

        def logout(self) -> None:
            self._username = ""
            self.show_login()

        def _swap_frame(self, frame: object) -> None:
            if self._active_frame is not None:
                self._active_frame.destroy()

            self._active_frame = frame
            self._active_frame.pack(
                fill=tk.BOTH,
                expand=True,
            )

else:

    class GridCareApplication:
        def __init__(
            self,
            *args: object,
            **kwargs: object,
        ) -> None:
            _ = args, kwargs
            require_tkinter()
