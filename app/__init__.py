from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from redis import Redis
from rq import Queue

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

mail = Mail(app)

redis_conn = Redis()
q = Queue(connection=redis_conn)

from . import views, models
