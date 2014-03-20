from datetime import datetime

from flask.ext.mail import Message

from app import app, db, mail, q, redis_conn
from config import ADMINS
from .models import NotificationLog


def send_notifications(order, template):
    """ Notify customer of an order by his registered notification
    methods, using the specified template.

    :order: the order which the notification is related to
    :template: the template to use
    :returns: @todo

    """

    user = order.user
    order_info = dict(order_id=order.id, order_timestamp=order.timestamp,
            order_description=order.description, username=user.nickname)

    if user.email_notification:
        send_email(user.email, template.email_subject.format(**order_info),
                template.email.format(**order_info))
    if user.sms_notification:
        send_sms(user.mobile, template.sms.format(**order_info))
    if user.app_notification:
        send_app_push(user, template.app.format(**order_info))
    
    add_log(order, template)


def add_log(order, template):
    """ Add a log of notifications.
    
    :order: the order which the notification is related to
    :template: the template of the notifications
    :returns: @todo

    """
    log = NotificationLog(timestamp=datetime.utcnow(), order=order,
            template=template)
    db.session.add(log)
    db.session.commit()


def send_email(email, subject, body):
    """ Send an email.

    :email: email address of the recipient
    :subject: subject of email
    :body: body of email
    :returns: @todo

    """

    msg = Message(subject, sender=ADMINS[0], recipients=[email])
    msg.body = body
    q.enqueue(send_email_func, msg)


def send_email_func(msg):
    with app.app_context():
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
