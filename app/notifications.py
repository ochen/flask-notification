from datetime import datetime

from flask.ext.mail import Message

from app import app, db, mail, q, redis_conn
from config import ADMINS
from .models import NotificationLog, SEND_METHOD_EMAIL, SEND_METHOD_SMS, \
    SEND_METHOD_APP


def send_notifications(order, template):
    """ Notify customer of an order by his registered notification
    methods, using the specified template.

    :order: the order which the notification is related to
    :template: the template to use

    """

    user = order.user

    if user.email_notification:
        # send email
        send_notification(order, template, SEND_METHOD_EMAIL)
    if user.sms_notification:
        # send sms
        send_notification(order, template, SEND_METHOD_SMS)
    if user.app_notification:
        # send app pushing
        send_notification(order, template, SEND_METHOD_APP)


def send_notification(order, template, method):
    """ Send notification by specified method

    :order: the order which the notification is related to
    :template: the template to use
    :method: send notification by which method

    """

    user = order.user
    order_info = dict(order_id=order.id, order_timestamp=order.timestamp,
            order_description=order.description, username=user.nickname)

    if method == SEND_METHOD_EMAIL:
        subject = template.email_subject.format(**order_info)
        body = template.email.format(**order_info)
        send_job = q.enqueue(send_email, user.email, subject, body)
    elif method == SEND_METHOD_SMS:
        send_job = q.enqueue(send_sms,
                user.mobile, template.sms.format(**order_info))
    elif method == SEND_METHOD_APP:
        send_job = q.enqueue(send_app_push,
                user, template.app.format(**order_info))

    # log after sending job done.
    q.enqueue_call(add_log, args=(order, template, method),
            depends_on=send_job)


def add_log(order, template, method):
    """ Add a log of notifications.
    
    :order: the order which the notification is related to
    :template: the template of the notifications
    :method: sent notification by which method
    :returns: @todo

    """
    log = NotificationLog(timestamp=datetime.utcnow(), order=order,
            template=template, method=method)
    db.session.add(log)
    db.session.commit()


def send_email(email, subject, body):
    """ Send an email.

    :email: email address of the recipient
    :subject: subject of email
    :body: body of email
    :returns: @todo

    """

    with app.app_context():
        msg = Message(subject, sender=ADMINS[0], recipients=[email])
        msg.body = body
        mail.send(msg)


def send_sms(number, body):
    """ Send SMS.

    :number: the number to send SMS to
    :body: the SMS body
    :returns: @todo

    """
    pass


def send_app_push(user, body):
    """ Push notification.

    :user: the user to push notification to
    :body: the notification body
    :returns: @todo

    """
    pass
