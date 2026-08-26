from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from cliniccare_lite.app.extensions import db
from cliniccare_lite.app.models.task import Task
from cliniccare_lite.app.models.user import User

from .forms import TaskForm


clinician_bp = Blueprint(
    "clinician",
    __name__,
    template_folder="../templates"
)


@clinician_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    tasks = Task.query.filter_by(
        clinician_id=current_user.id
    ).all()

    return render_template(
        "clinician/dashboard.html",
        tasks=tasks
    )


@clinician_bp.route("/tasks/create", methods=["GET", "POST"])
@login_required
def create_task():

    if current_user.role != "clinician":
        return redirect(url_for("patient.dashboard"))

    form = TaskForm()

    if form.validate_on_submit():

        patient = User.query.filter_by(
            username=form.patient_username.data,
            role="patient"
        ).first()

        if patient is None:
            flash("Patient not found.", "danger")

        else:
            task = Task()
            task.title = form.title.data
            task.instructions = form.instructions.data
            task.patient_id = patient.id
            task.clinician_id = current_user.id
            db.session.add(task)
            db.session.commit()

            flash("Task created successfully.", "success")

            return redirect(url_for("clinician.dashboard"))

    return render_template(
        "clinician/create_task.html",
        form=form
    )