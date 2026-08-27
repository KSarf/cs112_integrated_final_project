"""Database schema initialization for GridCare-Lite."""

from __future__ import annotations

from pathlib import Path

from .connection import get_connection


def initialize_database(database_path: Path) -> None:
    """Create all GridCare-Lite database tables."""

    with get_connection(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.cursor()

        # -------------------------
        # USERS
        # -------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (
                    role IN (
                        'Administrator',
                        'Engineer',
                        'Technician',
                        'Customer-service representative'
                    )
                )
            )
        """)

        # -------------------------
        # SUBSTATIONS
        # -------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS substations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                short_name TEXT,
                region TEXT,
                country TEXT,
                latitude REAL,
                longitude REAL,
                voltage_kv REAL,
                capacity_mva REAL,
                commissioning_year INTEGER,
                type TEXT,
                status TEXT
            )
        """)

        # -------------------------
        # TRANSMISSION LINES
        # -------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lines (
                id INTEGER PRIMARY KEY,
                utility_id INTEGER,
                source_substation_id INTEGER NOT NULL,
                destination_substation_id INTEGER NOT NULL,
                voltage_kv REAL,
                length_km REAL,
                capacity_mva REAL,
                status TEXT,
                line_type TEXT,

                FOREIGN KEY (source_substation_id)
                    REFERENCES substations(id),

                FOREIGN KEY (destination_substation_id)
                    REFERENCES substations(id)
            )
        """)

        # -------------------------
        # OUTAGES
        # -------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                substation_id INTEGER NOT NULL,
                severity TEXT NOT NULL CHECK (
                    severity IN ('Low', 'Medium', 'High', 'Critical')
                ),
                status TEXT NOT NULL DEFAULT 'Reported' CHECK (
                    status IN (
                        'Reported',
                        'Under Review',
                        'Assigned',
                        'In Progress',
                        'Resolved',
                        'Closed'
                    )
                ),
                reported_by INTEGER NOT NULL,
                reported_at TEXT NOT NULL,
                resolved_at TEXT,

                FOREIGN KEY (substation_id)
                    REFERENCES substations(id),

                FOREIGN KEY (reported_by)
                    REFERENCES users(id)
            )
        """)

        # -------------------------
        # WORK ORDERS
        # -------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                outage_id INTEGER NOT NULL,
                assigned_to INTEGER,
                scheduled_date TEXT,
                status TEXT NOT NULL DEFAULT 'Pending' CHECK (
                    status IN (
                        'Pending',
                        'Assigned',
                        'In Progress',
                        'Completed',
                        'Cancelled'
                    )
                ),
                instructions TEXT,
                resolution_notes TEXT,
                completed_at TEXT,

                FOREIGN KEY (outage_id)
                    REFERENCES outages(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (assigned_to)
                    REFERENCES users(id)
            )
        """)

        # -------------------------
        # COMPLAINTS
        # -------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                details TEXT NOT NULL,
                outage_id INTEGER,
                status TEXT NOT NULL DEFAULT 'Open' CHECK (
                    status IN (
                        'Open',
                        'In Progress',
                        'Resolved',
                        'Closed'
                    )
                ),
                created_at TEXT NOT NULL,

                FOREIGN KEY (outage_id)
                    REFERENCES outages(id)
                    ON DELETE SET NULL
            )
        """)

        # -------------------------
        # STATUS HISTORY
        # -------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS status_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                outage_id INTEGER,
                work_order_id INTEGER,
                old_status TEXT,
                new_status TEXT NOT NULL,
                changed_by INTEGER NOT NULL,
                changed_at TEXT NOT NULL,

                FOREIGN KEY (outage_id)
                    REFERENCES outages(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (work_order_id)
                    REFERENCES work_orders(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (changed_by)
                    REFERENCES users(id)
            )
        """)

        # -------------------------
        # MAINTENANCE ACTIVITIES
        # -------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS maintenance_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_order_id INTEGER NOT NULL,
                technician_id INTEGER NOT NULL,
                activity_description TEXT NOT NULL,
                activity_date TEXT NOT NULL,

                FOREIGN KEY (work_order_id)
                    REFERENCES work_orders(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (technician_id)
                    REFERENCES users(id)
            )
        """)

        # -------------------------
        # INDEXES
        # -------------------------
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_outages_substation
            ON outages(substation_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_outages_status
            ON outages(status)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_work_orders_status
            ON work_orders(status)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_work_orders_assigned_to
            ON work_orders(assigned_to)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_complaints_outage
            ON complaints(outage_id)
        """)

        connection.commit()
