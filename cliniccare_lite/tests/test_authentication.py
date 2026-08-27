"""Authentication tests for ClinicCare-Lite."""

from cliniccare_lite.app.extensions import db
from cliniccare_lite.app.models.user import User


def create_test_user(
    app,
    username: str,
    password: str,
    role: str
) -> None:

    with app.app_context():

        user = User()

        user.username = username
        user.role = role
        user.set_password(password)

        db.session.add(user)
        db.session.commit()


def test_public_pages_respond(client):

    assert client.get("/").status_code == 200
    assert client.get("/login").status_code == 200


def test_dashboards_require_login(client):

    clinician_response = client.get(
        "/clinician/dashboard"
    )

    patient_response = client.get(
        "/patient/dashboard"
    )

    assert clinician_response.status_code == 302
    assert patient_response.status_code == 302


def test_patient_login(app, client):

    create_test_user(
        app,
        "testpatient",
        "Patient123!",
        "patient"
    )

    response = client.post(
        "/login",
        data={
            "username": "testpatient",
            "password": "Patient123!",
        }
    )

    assert response.status_code == 302
    assert "/patient/dashboard" in response.location


def test_clinician_login(app, client):

    create_test_user(
        app,
        "testclinician",
        "Clinician123!",
        "clinician"
    )

    response = client.post(
        "/login",
        data={
            "username": "testclinician",
            "password": "Clinician123!",
        }
    )

    assert response.status_code == 302
    assert "/clinician/dashboard" in response.location


def test_wrong_password_does_not_login(
    app,
    client
):

    create_test_user(
        app,
        "testpatient",
        "Patient123!",
        "patient"
    )

    response = client.post(
        "/login",
        data={
            "username": "testpatient",
            "password": "wrongpassword",
        }
    )

    assert response.status_code == 200

    assert (
        b"Invalid username or password"
        in response.data
    )