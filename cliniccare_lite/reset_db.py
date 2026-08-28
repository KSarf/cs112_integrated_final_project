from cliniccare_lite.app import create_app
from cliniccare_lite.app.extensions import db

app = create_app()


with app.app_context():
    print("Resetting ClinicCare database...")

    db.drop_all()
    db.create_all()

    print("Database recreated successfully.")
