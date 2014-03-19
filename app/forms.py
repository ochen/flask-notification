from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField
from wtforms import validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Template


class RequiredIf(validators.Required):
    """ Make a field required if another field has a truthy value. """

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('No field named "{}" in form'.format(
                self.other_field_name))
        if other_field.data:
            super(RequiredIf, self).__call__(form, field)


class AddUserForm(Form):
    nickname = TextField('User name', [validators.Required()])
    email = TextField('Email', validators=[RequiredIf('email_notification')])
    mobile = TextField('Mobile', validators=[RequiredIf('sms_notification')])
    email_notification = BooleanField('Notify by email')
    sms_notification = BooleanField('Notify by SMS')
    app_notification = BooleanField('Notify by app push notification')


class EditUserForm(Form):
    email = TextField('Email', validators=[RequiredIf('email_notification')])
    mobile = TextField('Mobile', validators=[RequiredIf('sms_notification')])
    email_notification = BooleanField('Notify by email')
    sms_notification = BooleanField('Notify by SMS')
    app_notification = BooleanField('Notify by app push notification')


class AddTemplateForm(Form):
    name = TextField('Notification type', [validators.Required()])
    email = TextAreaField('Email template', [validators.Required()])
    sms = TextAreaField('SMS template', [validators.Required()])
    app = TextAreaField('APP push notification template', [validators.Required()])


class EditTemplateForm(Form):
    email = TextAreaField('Email template', [validators.Required()])
    sms = TextAreaField('SMS template', [validators.Required()])
    app = TextAreaField('APP push notification template', [validators.Required()])


class NotifyForm(Form):
    nickname = TextField('User name', [validators.Required()])
    notification_type = QuerySelectField('Notification type', get_label='name',
            query_factory=lambda: Template.query.all())
