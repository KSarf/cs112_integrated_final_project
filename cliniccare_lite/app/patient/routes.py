from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy import or_

from cliniccare_lite.app.extensions import db
from cliniccare_lite.app.models.announcement import (
    Announcement,
)
from cliniccare_lite.app.models.appointment import (
    Appointment,
)
from cliniccare_lite.app.models.notification import (
    Notification,
)
from cliniccare_lite.app.models.submission import (
    Submission,
)
from cliniccare_lite.app.models.task import Task
from cliniccare_lite.app.uploads.validators import (
    is_allowed_extension,
    sanitize_filename,
)

from .forms import SubmissionForm

patient_bp = Blueprint(
    "patient",
    __name__,
    template_folder="../templates",
)


@patient_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "patient":
        return redirect(url_for("clinician.dashboard"))

    tasks = Task.query.filter_by(patient_id=current_user.id).all()

    appointments = (
        Appointment.query.filter_by(patient_id=current_user.id)
        .order_by(Appointment.appointment_time.asc())
        .all()
    )

    submissions = (
        Submission.query.filter_by(patient_id=current_user.id)
        .order_by(Submission.submitted_at.desc())
        .all()
    )

    announcements = (
        Announcement.query.filter(
            or_(
                Announcement.expires_at.is_(None),
                Announcement.expires_at >= datetime.now(),
            )
        )
        .order_by(Announcement.published_at.desc())
        .all()
    )

    activity = {
        "tasks": len(tasks),
        "submissions": len(submissions),
        "appointments": len(appointments),
    }

    return render_template(
        "patient/dashboard.html",
        tasks=tasks,
        appointments=appointments,
        submissions=submissions,
        announcements=announcements,
        activity=activity,
    )


@patient_bp.route(
    "/tasks/<int:task_id>/submit",
    methods=["GET", "POST"],
)
@login_required
def submit_task(
    task_id,
):

    if current_user.role != "patient":
        return redirect(url_for("clinician.dashboard"))

    task = db.session.get(
        Task,
        task_id,
    )

    if task is None:

        flash(
            "Task not found.",
            "danger",
        )

        return redirect(url_for("patient.dashboard"))

    if task.patient_id != current_user.id:

        flash(
            "You cannot submit files for this task.",
            "danger",
        )

        return redirect(url_for("patient.dashboard"))

    if task.status not in (
        "Pending",
        "Needs Resubmission",
    ):

        flash(
            "This task is not currently open for submission.",
            "danger",
        )

        return redirect(url_for("patient.dashboard"))

    form = SubmissionForm()

    if form.validate_on_submit():

        uploaded_file = form.file.data

        if not is_allowed_extension(uploaded_file.filename):

            flash(
                "Only TXT, CSV and PDF files are allowed.",
                "danger",
            )

            return render_template(
                "patient/submit_task.html",
                form=form,
                task=task,
            )

        safe_name = sanitize_filename(uploaded_file.filename)

        if not safe_name:

            flash(
                "Invalid file name.",
                "danger",
            )

            return render_template(
                "patient/submit_task.html",
                form=form,
                task=task,
            )

        file_name = f"{current_user.id}_" f"{task.id}_" f"{uuid4().hex}_" f"{safe_name}"

        upload_folder = Path(current_app.config["UPLOAD_FOLDER"])

        upload_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = upload_folder / file_name

        uploaded_file.save(file_path)

        submission = Submission()

        submission.task_id = task.id
        submission.patient_id = current_user.id
        submission.file_name = file_name

        db.session.add(submission)

        task.status = "Submitted"

        notification = Notification()

        notification.user_id = task.clinician_id

        notification.message = f"New file submitted for task: " f"{task.title}."

        db.session.add(notification)

        db.session.commit()

        flash(
            "File submitted successfully.",
            "success",
        )

        return redirect(url_for("patient.dashboard"))

    return render_template(
        "patient/submit_task.html",
        form=form,
        task=task,
    )
