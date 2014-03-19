from app import app, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(16))
    email_notification = db.Column(db.Boolean)
    sms_notification = db.Column(db.Boolean)
    app_notification = db.Column(db.Boolean)


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(1024))
    sms = db.Column(db.String(140))
    app = db.Column(db.String(140))

