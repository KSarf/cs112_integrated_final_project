from datetime import datetime
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)

from cliniccare_lite.app.analytics.operational_metrics import (
    get_operational_summary,
)
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
from cliniccare_lite.app.models.user import User

from .forms import (
    AnnouncementForm,
    AppointmentForm,
    ReviewSubmissionForm,
    TaskForm,
)

clinician_bp = Blueprint(
    "clinician",
    __name__,
    template_folder="../templates",
)


@clinician_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    tasks = Task.query.filter_by(clinician_id=current_user.id).all()

    task_ids = [task.id for task in tasks]

    submissions = []

    if task_ids:

        submissions = (
            Submission.query.filter(Submission.task_id.in_(task_ids))
            .order_by(Submission.submitted_at.desc())
            .all()
        )

    appointments = (
        Appointment.query.filter_by(clinician_id=current_user.id)
        .order_by(Appointment.appointment_time.asc())
        .all()
    )

    announcements = (
        Announcement.query.filter_by(clinician_id=current_user.id)
        .order_by(Announcement.published_at.desc())
        .all()
    )

    analytics = get_operational_summary(current_user.id)

    return render_template(
        "clinician/dashboard.html",
        tasks=tasks,
        submissions=submissions,
        appointments=appointments,
        announcements=announcements,
        analytics=analytics,
    )


@clinician_bp.route(
    "/tasks/create",
    methods=["GET", "POST"],
)
@login_required
def create_task():

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    form = TaskForm()

    if form.validate_on_submit():

        patient_username = form.patient_username.data.strip()

        patient = User.query.filter_by(
            username=patient_username,
            role="patient",
        ).first()

        if patient is None:

            flash(
                "Patient not found.",
                "danger",
            )

        else:

            task = Task()

            task.title = form.title.data
            task.instructions = form.instructions.data
            task.due_date = form.due_date.data
            task.patient_id = patient.id
            task.clinician_id = current_user.id

            db.session.add(task)

            notification = Notification()

            notification.user_id = patient.id
            notification.message = (
                f"New administrative task assigned: "
                f"{task.title}. "
                f"Due: {task.due_date:%Y-%m-%d}."
            )

            db.session.add(notification)

            db.session.commit()

            flash(
                "Task created successfully.",
                "success",
            )

            return redirect(url_for("clinician.dashboard"))

    return render_template(
        "clinician/create_task.html",
        form=form,
    )


@clinician_bp.route(
    "/announcements/create",
    methods=["GET", "POST"],
)
@login_required
def create_announcement():

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    form = AnnouncementForm()

    if form.validate_on_submit():

        announcement = Announcement()

        announcement.title = form.title.data.strip()
        announcement.body = form.body.data.strip()
        announcement.priority = form.priority.data
        announcement.expires_at = form.expires_at.data
        announcement.clinician_id = current_user.id

        db.session.add(announcement)

        patients = User.query.filter_by(role="patient").all()

        for patient in patients:

            notification = Notification()

            notification.user_id = patient.id
            notification.message = (
                f"New {announcement.priority.lower()} "
                f"clinic announcement: "
                f"{announcement.title}"
            )

            db.session.add(notification)

        db.session.commit()

        flash(
            "Announcement published.",
            "success",
        )

        return redirect(url_for("clinician.dashboard"))

    return render_template(
        "clinician/create_announcement.html",
        form=form,
    )


@clinician_bp.route(
    "/appointments/create",
    methods=["GET", "POST"],
)
@login_required
def create_appointment():

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    form = AppointmentForm()

    if form.validate_on_submit():

        patient_username = form.patient_username.data.strip()

        patient = User.query.filter_by(
            username=patient_username,
            role="patient",
        ).first()

        if patient is None:

            flash(
                "Patient not found.",
                "danger",
            )

        else:

            appointment = Appointment()

            appointment.patient_id = patient.id
            appointment.clinician_id = current_user.id
            appointment.summary = form.summary.data
            appointment.appointment_time = form.appointment_time.data

            db.session.add(appointment)

            notification = Notification()

            notification.user_id = patient.id
            notification.message = (
                "New appointment scheduled for "
                f"{appointment.appointment_time:%Y-%m-%d %H:%M}."
            )

            db.session.add(notification)

            db.session.commit()

            flash(
                "Appointment scheduled successfully.",
                "success",
            )

            return redirect(url_for("clinician.dashboard"))

    return render_template(
        "clinician/create_appointment.html",
        form=form,
    )


@clinician_bp.route(
    "/appointments/<int:appointment_id>/remind",
    methods=["POST"],
)
@login_required
def send_appointment_reminder(
    appointment_id,
):

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    appointment = db.session.get(
        Appointment,
        appointment_id,
    )

    if appointment is None:

        flash(
            "Appointment not found.",
            "danger",
        )

        return redirect(url_for("clinician.dashboard"))

    if appointment.clinician_id != current_user.id:

        flash(
            "You cannot manage this appointment.",
            "danger",
        )

        return redirect(url_for("clinician.dashboard"))

    notification = Notification()

    notification.user_id = appointment.patient_id

    notification.message = (
        "Appointment reminder: "
        f"{appointment.summary} on "
        f"{appointment.appointment_time:%Y-%m-%d at %H:%M}."
    )

    db.session.add(notification)
    db.session.commit()

    flash(
        "Appointment reminder sent.",
        "success",
    )

    return redirect(url_for("clinician.dashboard"))


@clinician_bp.route(
    "/submissions/<int:submission_id>/review",
    methods=["GET", "POST"],
)
@login_required
def review_submission(
    submission_id,
):

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    submission = db.session.get(
        Submission,
        submission_id,
    )

    if submission is None:

        flash(
            "Submission not found.",
            "danger",
        )

        return redirect(url_for("clinician.dashboard"))

    task = db.session.get(
        Task,
        submission.task_id,
    )

    if task is None:

        flash(
            "Task not found.",
            "danger",
        )

        return redirect(url_for("clinician.dashboard"))

    if task.clinician_id != current_user.id:

        flash(
            "You cannot review this submission.",
            "danger",
        )

        return redirect(url_for("clinician.dashboard"))

    form = ReviewSubmissionForm()

    if form.validate_on_submit():

        submission.status = form.status.data

        submission.review_notes = form.review_notes.data

        submission.reviewer_id = current_user.id

        submission.reviewed_at = datetime.now()

        task.status = form.status.data

        notification = Notification()

        notification.user_id = task.patient_id

        notification.message = (
            f"Review update for task: " f"{task.title}. " f"Status: {form.status.data}."
        )

        db.session.add(notification)

        db.session.commit()

        flash(
            "Submission review saved.",
            "success",
        )

        return redirect(url_for("clinician.dashboard"))

    return render_template(
        "clinician/review_submission.html",
        form=form,
        submission=submission,
        task=task,
    )


@clinician_bp.route("/submissions/<int:submission_id>/download")
@login_required
def download_submission(
    submission_id,
):

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    submission = db.session.get(
        Submission,
        submission_id,
    )

    if submission is None:

        flash(
            "Submission not found.",
            "danger",
        )

        return redirect(url_for("clinician.dashboard"))

    task = db.session.get(
        Task,
        submission.task_id,
    )

    if task is None:

        flash(
            "Task not found.",
            "danger",
        )

        return redirect(url_for("clinician.dashboard"))

    if task.clinician_id != current_user.id:

        flash(
            "You cannot access this file.",
            "danger",
        )

        return redirect(url_for("clinician.dashboard"))

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])

    return send_from_directory(
        upload_folder,
        submission.file_name,
        as_attachment=True,
    )
