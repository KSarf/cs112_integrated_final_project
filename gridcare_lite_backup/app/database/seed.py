"""Import synthetic grid data into the GridCare-Lite database."""

from __future__ import annotations

import csv
from pathlib import Path

from .connection import get_connection


def seed_demo_data(database_path: Path) -> None:
    """Import substations and transmission lines from CSV files."""

    project_root = Path(__file__).resolve().parents[3]
    datasets_path = project_root / "Datasets"

    substations_file = datasets_path / "substations.csv"
    lines_file = datasets_path / "lines.csv"

    with get_connection(database_path) as connection:
        cursor = connection.cursor()

        # Import substations
        with substations_file.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO substations (
                        id,
                        name,
                        short_name,
                        region,
                        country,
                        latitude,
                        longitude,
                        voltage_kv,
                        capacity_mva,
                        commissioning_year,
                        type,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        int(row["Substation ID"]),
                        row["Name"],
                        row["Short Name"],
                        row["Region"],
                        row["Country"],
                        float(row["Latitude"]),
                        float(row["Longitude"]),
                        float(row["Voltage (kV)"]),
                        float(row["Capacity (MVA)"]),
                        int(row["Commissioning Year"]),
                        row["Type"],
                        row["Status"],
                    ),
                )

        # Import transmission lines
        with lines_file.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO lines (
                        id,
                        utility_id,
                        source_substation_id,
                        destination_substation_id,
                        voltage_kv,
                        length_km,
                        capacity_mva,
                        status,
                        line_type
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        int(row["Line ID"]),
                        int(row["Utility ID"]),
                        int(row["Source Substation ID"]),
                        int(row["Destination Substation ID"]),
                        float(row["Voltage (kV)"]),
                        float(row["Length (km)"]),
                        float(row["Capacity (MVA)"]),
                        row["Status"],
                        row["Line Type"],
                    ),
                )

        connection.commit()
