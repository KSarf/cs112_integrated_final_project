from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)

from cliniccare_lite.app.extensions import db
from cliniccare_lite.app.models.message import Message
from cliniccare_lite.app.models.notification import (
    Notification,
)
from cliniccare_lite.app.models.user import User

from .forms import MessageForm

messaging_bp = Blueprint(
    "messaging",
    __name__,
    template_folder="../templates",
)


@messaging_bp.route("/")
@login_required
def inbox():

    received_messages = (
        Message.query.filter_by(receiver_id=current_user.id)
        .order_by(Message.created_at.desc())
        .all()
    )

    sent_messages = (
        Message.query.filter_by(sender_id=current_user.id)
        .order_by(Message.created_at.desc())
        .all()
    )

    notifications = (
        Notification.query.filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    users = User.query.all()

    usernames = {user.id: user.username for user in users}

    return render_template(
        "messaging/inbox.html",
        received_messages=received_messages,
        sent_messages=sent_messages,
        notifications=notifications,
        usernames=usernames,
    )


@messaging_bp.route(
    "/send",
    methods=["GET", "POST"],
)
@login_required
def send_message():

    form = MessageForm()

    if form.validate_on_submit():

        username = form.recipient_username.data.strip()

        receiver = User.query.filter_by(username=username).first()

        if receiver is None:

            flash(
                "Recipient not found.",
                "danger",
            )

        elif receiver.id == current_user.id:

            flash(
                "You cannot send a message to yourself.",
                "danger",
            )

        else:

            message = Message()

            message.sender_id = current_user.id
            message.receiver_id = receiver.id
            message.body = form.body.data.strip()

            db.session.add(message)

            notification = Notification()

            notification.user_id = receiver.id
            notification.message = f"New message from " f"{current_user.username}"

            db.session.add(notification)

            db.session.commit()

            flash(
                "Message sent successfully.",
                "success",
            )

            return redirect(url_for("messaging.inbox"))

    return render_template(
        "messaging/send_message.html",
        form=form,
    )


@messaging_bp.route(
    "/messages/<int:message_id>/read",
    methods=["POST"],
)
@login_required
def mark_message_read(
    message_id,
):

    message = db.session.get(
        Message,
        message_id,
    )

    if message is None:

        flash(
            "Message not found.",
            "danger",
        )

        return redirect(url_for("messaging.inbox"))

    if message.receiver_id != current_user.id:

        flash(
            "You cannot access this message.",
            "danger",
        )

        return redirect(url_for("messaging.inbox"))

    message.is_read = True

    db.session.commit()

    return redirect(url_for("messaging.inbox"))


@messaging_bp.route(
    "/notifications/<int:notification_id>/read",
    methods=["POST"],
)
@login_required
def mark_notification_read(
    notification_id,
):

    notification = db.session.get(
        Notification,
        notification_id,
    )

    if notification is None:

        flash(
            "Notification not found.",
            "danger",
        )

        return redirect(url_for("messaging.inbox"))

    if notification.user_id != current_user.id:

        flash(
            "You cannot access this notification.",
            "danger",
        )

        return redirect(url_for("messaging.inbox"))

    notification.is_read = True

    db.session.commit()

    return redirect(url_for("messaging.inbox"))
