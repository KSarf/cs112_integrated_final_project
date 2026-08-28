"""Privacy and ownership tests for ClinicCare-Lite."""

from cliniccare_lite.app.extensions import db
from cliniccare_lite.app.models.submission import Submission
from cliniccare_lite.app.models.task import Task
from cliniccare_lite.app.models.user import User


def create_user(
    app,
    username: str,
    password: str,
    role: str,
) -> int:
    """Create a test user and return the user ID."""

    with app.app_context():
        user = User()

        user.username = username
        user.role = role
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user.id


def login(
    client,
    username: str,
    password: str,
):
    """Log a test user into ClinicCare-Lite."""

    return client.post(
        "/login",
        data={
            "username": username,
            "password": password,
        },
    )


def test_patient_only_sees_own_tasks(
    app,
    client,
):
    patient_one_id = create_user(
        app,
        "patient_one",
        "Patient123!",
        "patient",
    )

    patient_two_id = create_user(
        app,
        "patient_two",
        "Patient123!",
        "patient",
    )

    clinician_id = create_user(
        app,
        "clinician_one",
        "Clinician123!",
        "clinician",
    )

    with app.app_context():
        patient_one_task = Task()

        patient_one_task.title = "Patient One Task"
        patient_one_task.instructions = "Upload administrative document."
        patient_one_task.patient_id = patient_one_id
        patient_one_task.clinician_id = clinician_id

        patient_two_task = Task()

        patient_two_task.title = "Patient Two Private Task"
        patient_two_task.instructions = "Upload private administrative file."
        patient_two_task.patient_id = patient_two_id
        patient_two_task.clinician_id = clinician_id

        db.session.add(patient_one_task)
        db.session.add(patient_two_task)
        db.session.commit()

    login(
        client,
        "patient_one",
        "Patient123!",
    )

    response = client.get("/patient/dashboard")

    assert response.status_code == 200

    assert b"Patient One Task" in response.data

    assert b"Patient Two Private Task" not in response.data


def test_patient_cannot_submit_to_another_patient_task(
    app,
    client,
):
    create_user(
        app,
        "patient_one",
        "Patient123!",
        "patient",
    )

    patient_two_id = create_user(
        app,
        "patient_two",
        "Patient123!",
        "patient",
    )

    clinician_id = create_user(
        app,
        "clinician_one",
        "Clinician123!",
        "clinician",
    )

    with app.app_context():
        task = Task()

        task.title = "Private Task"
        task.instructions = "Private administrative task."
        task.patient_id = patient_two_id
        task.clinician_id = clinician_id

        db.session.add(task)
        db.session.commit()

        task_id = task.id

    login(
        client,
        "patient_one",
        "Patient123!",
    )

    response = client.get(f"/patient/tasks/{task_id}/submit")

    assert response.status_code == 302

    assert "/patient/dashboard" in response.location

    with app.app_context():
        submission_count = Submission.query.filter_by(task_id=task_id).count()

        assert submission_count == 0


def test_clinician_cannot_review_another_clinicians_submission(
    app,
    client,
):
    patient_id = create_user(
        app,
        "patient_one",
        "Patient123!",
        "patient",
    )

    create_user(
        app,
        "clinician_one",
        "Clinician123!",
        "clinician",
    )

    clinician_two_id = create_user(
        app,
        "clinician_two",
        "Clinician123!",
        "clinician",
    )

    with app.app_context():
        task = Task()

        task.title = "Clinician Two Task"
        task.instructions = "Administrative document review."
        task.patient_id = patient_id
        task.clinician_id = clinician_two_id
        task.status = "Submitted"

        db.session.add(task)
        db.session.commit()

        submission = Submission()

        submission.task_id = task.id
        submission.patient_id = patient_id
        submission.file_name = "private.pdf"

        db.session.add(submission)
        db.session.commit()

        submission_id = submission.id

    login(
        client,
        "clinician_one",
        "Clinician123!",
    )

    response = client.get(f"/clinician/submissions/" f"{submission_id}/review")

    assert response.status_code == 302

    assert "/clinician/dashboard" in response.location


def test_clinician_cannot_download_another_clinicians_submission(
    app,
    client,
):
    patient_id = create_user(
        app,
        "patient_one",
        "Patient123!",
        "patient",
    )

    create_user(
        app,
        "clinician_one",
        "Clinician123!",
        "clinician",
    )

    clinician_two_id = create_user(
        app,
        "clinician_two",
        "Clinician123!",
        "clinician",
    )

    with app.app_context():
        task = Task()

        task.title = "Private Submission"
        task.instructions = "Administrative upload."
        task.patient_id = patient_id
        task.clinician_id = clinician_two_id
        task.status = "Submitted"

        db.session.add(task)
        db.session.commit()

        submission = Submission()

        submission.task_id = task.id
        submission.patient_id = patient_id
        submission.file_name = "private.pdf"

        db.session.add(submission)
        db.session.commit()

        submission_id = submission.id

    login(
        client,
        "clinician_one",
        "Clinician123!",
    )

    response = client.get(f"/clinician/submissions/" f"{submission_id}/download")

    assert response.status_code == 302

    assert "/clinician/dashboard" in response.location
