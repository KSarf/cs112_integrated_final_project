"""Work-order services for GridCare-Lite."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from gridcare_lite.app.database.connection import get_connection


@dataclass(slots=True)
class WorkOrderService:
    """Manage the GridCare work-order workflow."""

    database_path: Path

    def create_work_order(
        self,
        outage_id: int,
        technician_id: int,
        scheduled_date: str,
        instructions: str,
        changed_by: int,
    ) -> int:
        """Assign a technician to a reviewed outage."""

        if not scheduled_date.strip():
            raise ValueError("Scheduled date is required.")

        if not instructions.strip():
            raise ValueError("Instructions are required.")

        with get_connection(self.database_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT status FROM outages WHERE id = ?",
                (outage_id,),
            )
            outage = cursor.fetchone()

            if outage is None:
                raise ValueError("Outage does not exist.")

            if outage[0] != "Under Review":
                raise ValueError("Outage must be reviewed first.")

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE id = ?
                  AND role = 'Technician'
                """,
                (technician_id,),
            )

            if cursor.fetchone() is None:
                raise ValueError("Selected user is not a technician.")

            cursor.execute(
                """
                SELECT id
                FROM work_orders
                WHERE outage_id = ?
                  AND status NOT IN ('Completed', 'Cancelled')
                """,
                (outage_id,),
            )

            if cursor.fetchone() is not None:
                raise ValueError("This outage already has an active work order.")

            cursor.execute(
                """
                INSERT INTO work_orders (
                    outage_id,
                    assigned_to,
                    scheduled_date,
                    status,
                    instructions
                )
                VALUES (?, ?, ?, 'Assigned', ?)
                """,
                (
                    outage_id,
                    technician_id,
                    scheduled_date.strip(),
                    instructions.strip(),
                ),
            )

            work_order_id = cursor.lastrowid

            cursor.execute(
                """
                UPDATE outages
                SET status = 'Assigned'
                WHERE id = ?
                """,
                (outage_id,),
            )

            now = datetime.now().isoformat(timespec="seconds")

            cursor.execute(
                """
                INSERT INTO status_history (
                    outage_id,
                    work_order_id,
                    old_status,
                    new_status,
                    changed_by,
                    changed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    outage_id,
                    work_order_id,
                    "Under Review",
                    "Assigned",
                    changed_by,
                    now,
                ),
            )

            connection.commit()

        return int(work_order_id)

    def start_work(
        self,
        work_order_id: int,
        technician_id: int,
    ) -> None:
        """Move an assigned work order to In Progress."""

        with get_connection(self.database_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT outage_id, assigned_to, status
                FROM work_orders
                WHERE id = ?
                """,
                (work_order_id,),
            )

            row = cursor.fetchone()

            if row is None:
                raise ValueError("Work order does not exist.")

            outage_id, assigned_to, status = row

            if assigned_to != technician_id:
                raise PermissionError("This work order is not assigned to you.")

            if status != "Assigned":
                raise ValueError("Only assigned work can be started.")

            cursor.execute(
                """
                UPDATE work_orders
                SET status = 'In Progress'
                WHERE id = ?
                """,
                (work_order_id,),
            )

            cursor.execute(
                """
                UPDATE outages
                SET status = 'In Progress'
                WHERE id = ?
                """,
                (outage_id,),
            )

            now = datetime.now().isoformat(timespec="seconds")

            cursor.execute(
                """
                INSERT INTO status_history (
                    outage_id,
                    work_order_id,
                    old_status,
                    new_status,
                    changed_by,
                    changed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    outage_id,
                    work_order_id,
                    "Assigned",
                    "In Progress",
                    technician_id,
                    now,
                ),
            )

            connection.commit()

    def complete_work(
        self,
        work_order_id: int,
        technician_id: int,
        resolution_notes: str,
    ) -> None:
        """Complete a work order and resolve its outage."""

        if not resolution_notes.strip():
            raise ValueError("Resolution notes are required.")

        with get_connection(self.database_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT outage_id, assigned_to, status
                FROM work_orders
                WHERE id = ?
                """,
                (work_order_id,),
            )

            row = cursor.fetchone()

            if row is None:
                raise ValueError("Work order does not exist.")

            outage_id, assigned_to, status = row

            if assigned_to != technician_id:
                raise PermissionError("This work order is not assigned to you.")

            if status != "In Progress":
                raise ValueError("Work must be In Progress before completion.")

            now = datetime.now().isoformat(timespec="seconds")

            cursor.execute(
                """
                UPDATE work_orders
                SET status = 'Completed',
                    resolution_notes = ?,
                    completed_at = ?
                WHERE id = ?
                """,
                (
                    resolution_notes.strip(),
                    now,
                    work_order_id,
                ),
            )

            cursor.execute(
                """
                UPDATE outages
                SET status = 'Resolved',
                    resolved_at = ?
                WHERE id = ?
                """,
                (
                    now,
                    outage_id,
                ),
            )

            cursor.execute(
                """
                INSERT INTO maintenance_activities (
                    work_order_id,
                    technician_id,
                    activity_description,
                    activity_date
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    work_order_id,
                    technician_id,
                    resolution_notes.strip(),
                    now,
                ),
            )

            cursor.execute(
                """
                INSERT INTO status_history (
                    outage_id,
                    work_order_id,
                    old_status,
                    new_status,
                    changed_by,
                    changed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    outage_id,
                    work_order_id,
                    "In Progress",
                    "Resolved",
                    technician_id,
                    now,
                ),
            )

            connection.commit()
