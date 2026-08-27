from cliniccare_lite.app import create_app
from cliniccare_lite.app.extensions import db
from cliniccare_lite.app.models.user import User

app = create_app()


with app.app_context():
    patient = User.query.filter_by(username="patient1").first()

    if patient is None:
        patient = User()
        patient.username = "patient1"
        patient.role = "patient"
        patient.set_password("Patient123!")
        db.session.add(patient)

    clinician = User.query.filter_by(username="clinician1").first()

    if clinician is None:
        clinician = User()
        clinician.username = "clinician1"
        clinician.role = "clinician"
        clinician.set_password("Clinician123!")
        db.session.add(clinician)

    db.session.commit()

    print("Demo users created.")
