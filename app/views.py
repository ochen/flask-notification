from flask import render_template, flash, redirect, url_for

from app import app, db
from .models import User, Template
from .forms import AddUserForm, EditUserForm


@app.route('/')
def index():
    return "Hello"

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        nickname = form.nickname.data
        user = User(nickname=nickname, email=form.email.data,
                mobile=form.mobile.data,
                email_notification=form.email_notification.data,
                sms_notification=form.sms_notification.data,
                app_notification=form.app_notification.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} added.'.format(nickname))
        return redirect(url_for('index'))
    return render_template('add_user.html', form=form)


@app.route('/user/<nickname>/edit', methods=['GET', 'POST'])
def edit(nickname):
    form = EditUserForm()
    user = User.query.filter_by(nickname=nickname).first()
    if form.validate_on_submit():
        user.email = form.email.data
        user.mobile = form.mobile.data
        user.email_notification = form.email_notification.data
        user.sms_notification = form.sms_notification.data
        user.app_notification = form.app_notification.data
        db.session.add(user)
        db.session.commit()
        flash('Changes for {} have been saved.'.format(nickname))
        return redirect(url_for('index'))
    else:
        form.email.data = user.email
        form.mobile.data = user.mobile
        form.email_notification.data = user.email_notification
        form.sms_notification.data = user.sms_notification
        form.app_notification.data = user.app_notification
    return render_template('edit_user.html', form=form)


@app.route('/template/<name>/edit', methods=['GET', 'POST'])
def edit_template(name):
    pass


@app.route('/template/add', methods=['GET', 'POST'])
def add_template():
    pass
