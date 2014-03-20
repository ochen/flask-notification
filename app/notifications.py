from flask.ext.mail import Message
from rq.decorators import job

from app import mail, q, redis_conn
from config import ADMINS

def send_notifications(user, template):
    """ Notify user by registered methods, using the specified template.

    :user: the user to notify
    :template: the template to use
    :returns: @todo

    """

    if user.email_notification:
        send_email(user, template.email_subject, template.email)
    if user.sms_notification:
        send_sms(user, template.sms)
    if user.app_notification:
        send_app_push(user, template.app)


def send_email(user, subject_temp, body_temp):
    """ Send an email.

    :user: the user to send email to
    :subject_temp: the template string to use as email subject
    :body_temp: the template string to use as email body
    :returns: @todo

    """

    msg = Message(subject_temp, sender=ADMINS[0], recipients=[user.email])
    msg.body = body_temp
    q.enqueue(send_email_func, msg)


def send_email_func(msg):
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
