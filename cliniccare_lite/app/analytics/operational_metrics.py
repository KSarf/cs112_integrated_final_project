"""Operational analytics for ClinicCare-Lite."""

from datetime import date

from cliniccare_lite.app.models.announcement import (
    Announcement,
)
from cliniccare_lite.app.models.appointment import (
    Appointment,
)
from cliniccare_lite.app.models.submission import (
    Submission,
)
from cliniccare_lite.app.models.task import Task


def get_operational_summary(
    clinician_id: int,
) -> dict[str, int]:
    """Return non-diagnostic administrative statistics."""

    tasks = Task.query.filter_by(clinician_id=clinician_id).all()

    total_tasks = len(tasks)

    pending_tasks = sum(task.status == "Pending" for task in tasks)

    submitted_tasks = sum(task.status == "Submitted" for task in tasks)

    reviewed_tasks = sum(
        task.status
        in {
            "Reviewed",
            "Needs Follow-up",
            "Escalated",
        }
        for task in tasks
    )

    resubmission_tasks = sum(task.status == "Needs Resubmission" for task in tasks)

    overdue_tasks = sum(
        task.due_date is not None
        and task.due_date < date.today()
        and task.status
        in {
            "Pending",
            "Needs Resubmission",
        }
        for task in tasks
    )

    task_ids = [task.id for task in tasks]

    total_submissions = 0
    pending_reviews = 0

    if task_ids:

        total_submissions = Submission.query.filter(
            Submission.task_id.in_(task_ids)
        ).count()

        pending_reviews = Submission.query.filter(
            Submission.task_id.in_(task_ids),
            Submission.status == "Submitted",
        ).count()

    total_appointments = Appointment.query.filter_by(clinician_id=clinician_id).count()

    total_announcements = Announcement.query.filter_by(
        clinician_id=clinician_id
    ).count()

    return {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "submitted_tasks": submitted_tasks,
        "reviewed_tasks": reviewed_tasks,
        "resubmission_tasks": resubmission_tasks,
        "overdue_tasks": overdue_tasks,
        "total_submissions": total_submissions,
        "pending_reviews": pending_reviews,
        "total_appointments": total_appointments,
        "total_announcements": total_announcements,
    }
