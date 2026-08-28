"""Outage services for GridCare-Lite."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from gridcare_lite.app.database.connection import get_connection


@dataclass(slots=True)
class OutageService:
    """Create and update outages."""

    database_path: Path

    def create_outage(
        self,
        title: str,
        description: str,
        substation_id: int,
        severity: str,
        reported_at: str,
        reported_by: int,
    ) -> int:
        """Create a new outage."""

        if not title.strip():
            raise ValueError("Outage title is required.")

        if not description.strip():
            raise ValueError("Description is required.")

        if severity not in {"Low", "Medium", "High", "Critical"}:
            raise ValueError("Invalid severity.")

        with get_connection(self.database_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT id FROM substations WHERE id = ?",
                (substation_id,),
            )

            if cursor.fetchone() is None:
                raise ValueError("Selected substation does not exist.")

            cursor.execute(
                """
                SELECT id
                FROM outages
                WHERE substation_id = ?
                  AND title = ?
                  AND status NOT IN ('Resolved', 'Closed')
                """,
                (substation_id, title.strip()),
            )

            if cursor.fetchone() is not None:
                raise ValueError("A matching active outage already exists.")

            cursor.execute(
                """
                INSERT INTO outages (
                    title,
                    description,
                    substation_id,
                    severity,
                    status,
                    reported_by,
                    reported_at
                )
                VALUES (?, ?, ?, ?, 'Reported', ?, ?)
                """,
                (
                    title.strip(),
                    description.strip(),
                    substation_id,
                    severity,
                    reported_by,
                    reported_at,
                ),
            )

            outage_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO status_history (
                    outage_id,
                    old_status,
                    new_status,
                    changed_by,
                    changed_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    outage_id,
                    None,
                    "Reported",
                    reported_by,
                    reported_at,
                ),
            )

            connection.commit()

        return int(outage_id)

    def review_outage(
        self,
        outage_id: int,
        changed_by: int,
        changed_at: str,
    ) -> None:
        """Move a reported outage to Under Review."""

        with get_connection(self.database_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT status FROM outages WHERE id = ?",
                (outage_id,),
            )

            row = cursor.fetchone()

            if row is None:
                raise ValueError("Outage does not exist.")

            if row[0] != "Reported":
                raise ValueError("Only reported outages can be reviewed.")

            cursor.execute(
                """
                UPDATE outages
                SET status = 'Under Review'
                WHERE id = ?
                """,
                (outage_id,),
            )

            cursor.execute(
                """
                INSERT INTO status_history (
                    outage_id,
                    old_status,
                    new_status,
                    changed_by,
                    changed_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    outage_id,
                    "Reported",
                    "Under Review",
                    changed_by,
                    changed_at,
                ),
            )

            connection.commit()
