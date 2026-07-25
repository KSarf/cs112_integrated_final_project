"""Run ClinicCare-Lite application."""

from __future__ import annotations

import os

from cliniccare_lite.app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
