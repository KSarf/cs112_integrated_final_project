"""Authentication service placeholders for GridCare-Lite."""

from __future__ import annotations

from dataclasses import dataclass

from gridcare_lite.app.config import GridCareConfig
from gridcare_lite.app.security.passwords import verify_password


@dataclass(slots=True)
class AuthService:
    """Auth service implementing development-only demo login behavior."""

    config: GridCareConfig

    def demo_login_allowed(
        self, username: str, password: str, password_hash: str
    ) -> bool:
        """Allow demo login only when explicitly enabled in config.

        TODO: Replace with proper persistent user authentication flow.
        """
        if not self.config.enable_demo_login:
            return False
        return username == "demo" and verify_password(password, password_hash)
