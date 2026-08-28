"""Workflow tests for GridCare-Lite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from gridcare_lite.app.database.schema import initialize_database
from gridcare_lite.app.services.outage_service import OutageService
from gridcare_lite.app.services.work_order_service import WorkOrderService


def prepare_test_database(database_path: Path) -> None:
    """Create a small database for workflow testing."""

    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?)
            """,
            (
                "engineer_test",
                "test-hash",
                "Engineer",
            ),
        )

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?)
            """,
            (
                "admin_test",
                "test-hash",
                "Administrator",
            ),
        )

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?)
            """,
            (
                "technician_test",
                "test-hash",
                "Technician",
            ),
        )

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?)
            """,
            (
                "other_technician",
                "test-hash",
                "Technician",
            ),
        )

        cursor.execute(
            """
            INSERT INTO substations (
                id,
                name,
                region,
                country,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                1,
                "Test Substation",
                "Greater Accra",
                "Ghana",
                "Active",
            ),
        )

        connection.commit()


def get_user_id(
    database_path: Path,
    username: str,
) -> int:
    """Return the ID for a test user."""

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        row = cursor.fetchone()

    return int(row[0])


def test_complete_outage_workflow(tmp_path: Path) -> None:
    """Test outage creation through final resolution."""

    database_path = tmp_path / "gridcare_test.db"
    prepare_test_database(database_path)

    engineer_id = get_user_id(
        database_path,
        "engineer_test",
    )

    admin_id = get_user_id(
        database_path,
        "admin_test",
    )

    technician_id = get_user_id(
        database_path,
        "technician_test",
    )

    outage_service = OutageService(database_path)
    work_order_service = WorkOrderService(database_path)

    outage_id = outage_service.create_outage(
        title="Test Power Outage",
        description="Power failure at test substation.",
        substation_id=1,
        severity="High",
        reported_at="2026-08-28T10:00:00",
        reported_by=engineer_id,
    )

    with sqlite3.connect(database_path) as connection:
        status = connection.execute(
            """
            SELECT status
            FROM outages
            WHERE id = ?
            """,
            (outage_id,),
        ).fetchone()[0]

    assert status == "Reported"

    outage_service.review_outage(
        outage_id=outage_id,
        changed_by=admin_id,
        changed_at="2026-08-28T10:15:00",
    )

    with sqlite3.connect(database_path) as connection:
        status = connection.execute(
            """
            SELECT status
            FROM outages
            WHERE id = ?
            """,
            (outage_id,),
        ).fetchone()[0]

    assert status == "Under Review"

    work_order_id = work_order_service.create_work_order(
        outage_id=outage_id,
        technician_id=technician_id,
        scheduled_date="2026-08-28",
        instructions="Inspect equipment and restore service.",
        changed_by=admin_id,
    )

    with sqlite3.connect(database_path) as connection:
        work_status = connection.execute(
            """
            SELECT status
            FROM work_orders
            WHERE id = ?
            """,
            (work_order_id,),
        ).fetchone()[0]

        outage_status = connection.execute(
            """
            SELECT status
            FROM outages
            WHERE id = ?
            """,
            (outage_id,),
        ).fetchone()[0]

    assert work_status == "Assigned"
    assert outage_status == "Assigned"

    work_order_service.start_work(
        work_order_id=work_order_id,
        technician_id=technician_id,
    )

    with sqlite3.connect(database_path) as connection:
        work_status = connection.execute(
            """
            SELECT status
            FROM work_orders
            WHERE id = ?
            """,
            (work_order_id,),
        ).fetchone()[0]

        outage_status = connection.execute(
            """
            SELECT status
            FROM outages
            WHERE id = ?
            """,
            (outage_id,),
        ).fetchone()[0]

    assert work_status == "In Progress"
    assert outage_status == "In Progress"

    work_order_service.complete_work(
        work_order_id=work_order_id,
        technician_id=technician_id,
        resolution_notes="Fault repaired and power restored.",
    )

    with sqlite3.connect(database_path) as connection:
        work_order = connection.execute(
            """
            SELECT
                status,
                resolution_notes,
                completed_at
            FROM work_orders
            WHERE id = ?
            """,
            (work_order_id,),
        ).fetchone()

        outage = connection.execute(
            """
            SELECT
                status,
                resolved_at
            FROM outages
            WHERE id = ?
            """,
            (outage_id,),
        ).fetchone()

        maintenance_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM maintenance_activities
            WHERE work_order_id = ?
            """,
            (work_order_id,),
        ).fetchone()[0]

    assert work_order[0] == "Completed"
    assert work_order[1] == "Fault repaired and power restored."
    assert work_order[2] is not None

    assert outage[0] == "Resolved"
    assert outage[1] is not None

    assert maintenance_count == 1


def test_invalid_substation_is_rejected(tmp_path: Path) -> None:
    """An outage cannot use a substation that does not exist."""

    database_path = tmp_path / "gridcare_test.db"
    prepare_test_database(database_path)

    engineer_id = get_user_id(
        database_path,
        "engineer_test",
    )

    service = OutageService(database_path)

    with pytest.raises(
        ValueError,
        match="Selected substation does not exist",
    ):
        service.create_outage(
            title="Invalid Outage",
            description="Testing invalid substation.",
            substation_id=999,
            severity="High",
            reported_at="2026-08-28T10:00:00",
            reported_by=engineer_id,
        )


def test_duplicate_active_outage_is_rejected(
    tmp_path: Path,
) -> None:
    """A matching active outage should not be created twice."""

    database_path = tmp_path / "gridcare_test.db"
    prepare_test_database(database_path)

    engineer_id = get_user_id(
        database_path,
        "engineer_test",
    )

    service = OutageService(database_path)

    service.create_outage(
        title="Repeated Outage",
        description="First report.",
        substation_id=1,
        severity="Medium",
        reported_at="2026-08-28T10:00:00",
        reported_by=engineer_id,
    )

    with pytest.raises(
        ValueError,
        match="matching active outage",
    ):
        service.create_outage(
            title="Repeated Outage",
            description="Second report.",
            substation_id=1,
            severity="Medium",
            reported_at="2026-08-28T10:05:00",
            reported_by=engineer_id,
        )


def test_wrong_technician_cannot_start_work(
    tmp_path: Path,
) -> None:
    """A technician cannot start another technician's work order."""

    database_path = tmp_path / "gridcare_test.db"
    prepare_test_database(database_path)

    engineer_id = get_user_id(
        database_path,
        "engineer_test",
    )

    admin_id = get_user_id(
        database_path,
        "admin_test",
    )

    technician_id = get_user_id(
        database_path,
        "technician_test",
    )

    other_technician_id = get_user_id(
        database_path,
        "other_technician",
    )

    outage_service = OutageService(database_path)
    work_order_service = WorkOrderService(database_path)

    outage_id = outage_service.create_outage(
        title="Technician Test",
        description="Testing work-order ownership.",
        substation_id=1,
        severity="Low",
        reported_at="2026-08-28T10:00:00",
        reported_by=engineer_id,
    )

    outage_service.review_outage(
        outage_id=outage_id,
        changed_by=admin_id,
        changed_at="2026-08-28T10:10:00",
    )

    work_order_id = work_order_service.create_work_order(
        outage_id=outage_id,
        technician_id=technician_id,
        scheduled_date="2026-08-28",
        instructions="Inspect the outage.",
        changed_by=admin_id,
    )

    with pytest.raises(
        PermissionError,
        match="not assigned to you",
    ):
        work_order_service.start_work(
            work_order_id=work_order_id,
            technician_id=other_technician_id,
        )


def test_resolution_notes_are_required(
    tmp_path: Path,
) -> None:
    """A work order cannot be completed without resolution notes."""

    database_path = tmp_path / "gridcare_test.db"
    prepare_test_database(database_path)

    engineer_id = get_user_id(
        database_path,
        "engineer_test",
    )

    admin_id = get_user_id(
        database_path,
        "admin_test",
    )

    technician_id = get_user_id(
        database_path,
        "technician_test",
    )

    outage_service = OutageService(database_path)
    work_order_service = WorkOrderService(database_path)

    outage_id = outage_service.create_outage(
        title="Resolution Test",
        description="Testing required resolution notes.",
        substation_id=1,
        severity="Critical",
        reported_at="2026-08-28T10:00:00",
        reported_by=engineer_id,
    )

    outage_service.review_outage(
        outage_id=outage_id,
        changed_by=admin_id,
        changed_at="2026-08-28T10:10:00",
    )

    work_order_id = work_order_service.create_work_order(
        outage_id=outage_id,
        technician_id=technician_id,
        scheduled_date="2026-08-28",
        instructions="Repair the fault.",
        changed_by=admin_id,
    )

    work_order_service.start_work(
        work_order_id=work_order_id,
        technician_id=technician_id,
    )

    with pytest.raises(
        ValueError,
        match="Resolution notes are required",
    ):
        work_order_service.complete_work(
            work_order_id=work_order_id,
            technician_id=technician_id,
            resolution_notes="",
        )
