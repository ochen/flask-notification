from flask.ext.mail import Message
from rq.decorators import job

from app import app, mail, q, redis_conn
from config import ADMINS

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

def send_sms(user, temp):
    """ Send SMS.

    :user: the user to send SMS to
    :temp: the template string to use as SMS body
    :returns: @todo

    """
    pass


def send_app_push(user, temp):
    """ Send SMS.

    :user: the user to send push notification to
    :temp: the template string to use as notification body
    :returns: @todo

    """
    pass
