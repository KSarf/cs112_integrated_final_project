"""Authentication services for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from gridcare_lite.app.security.passwords import verify_password


@dataclass(slots=True)
class AuthenticatedUser:
    """Information about a successfully authenticated user."""

    user_id: int
    username: str
    role: str


@dataclass(slots=True)
class AuthService:
    """Authenticate users against the GridCare database."""

    database_path: Path

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> AuthenticatedUser | None:
        """Authenticate a user and return their account information."""

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    password_hash,
                    role
                FROM users
                WHERE username = ?
                """,
                (username,),
            )

            user = cursor.fetchone()

        if user is None:
            return None

        user_id, stored_username, password_hash, role = user

        try:
            valid_password = verify_password(
                password,
                password_hash,
            )
        except (ValueError, TypeError):
            return None

        if not valid_password:
            return None

        return AuthenticatedUser(
            user_id=user_id,
            username=stored_username,
            role=role,
        )