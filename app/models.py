from app import app, db

SEND_METHOD_EMAIL = 0
SEND_METHOD_SMS = 1
SEND_METHOD_APP = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(16))
    email_notification = db.Column(db.Boolean)
    sms_notification = db.Column(db.Boolean)
    app_notification = db.Column(db.Boolean)
    orders = db.relationship('Order', backref='user', lazy='dynamic')


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email_subject = db.Column(db.String(140))
    email = db.Column(db.String(1024))
    sms = db.Column(db.String(140))
    app = db.Column(db.String(140))
    logs = db.relationship('NotificationLog', backref='template',
            lazy='dynamic')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    logs = db.relationship('NotificationLog', backref='order',
            lazy='dynamic')


class NotificationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    method = db.Column(db.SmallInteger)
