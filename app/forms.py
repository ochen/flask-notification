from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField
from wtforms import validators

class AddUserForm(Form):
    nickname = TextField('User name', [validators.Required()])
    email = TextField('Email', validators=[validators.Length(min=6,
        max=35)])
    mobile = TextField('Mobile', validators=[validators.Length(min=11,
        max=16)])
    email_notification = BooleanField('Notify by email')
    sms_notification = BooleanField('Notify by SMS')
    app_notification = BooleanField('Notify by app push notification')


class EditUserForm(Form):
    email = TextField('Email', validators=[validators.Length(min=6,
        max=35)])
    mobile = TextField('Mobile', validators=[validators.Length(min=11,
        max=16)])
    email_notification = BooleanField('Notify by email')
    sms_notification = BooleanField('Notify by SMS')
    app_notification = BooleanField('Notify by app push notification')

