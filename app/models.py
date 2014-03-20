from app import app, db

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


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
