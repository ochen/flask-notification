import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

CSRF_ENABLED = True
SECRET_KEY = 'helloworld'

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'ccl333'
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

# administrator list
ADMINS = ['ccl333@gmail.com']
