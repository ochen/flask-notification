from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, abort

from app import app, db
from .models import User, Template, Order
from .forms import AddUserForm, EditUserForm, AddTemplateForm, \
    EditTemplateForm, NotifyForm, NewOrderForm
from .notifications import send_notifications


@app.route('/')
def index():
    return "Hello"

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        nickname = form.nickname.data
        user = User.query.filter_by(nickname=nickname).first()
        if user is not None:
            flash("User name not available.")
            return render_template('add_user.html', form=form)
        user = User(nickname=nickname, email=form.email.data,
                mobile=form.mobile.data,
                email_notification=form.email_notification.data,
                sms_notification=form.sms_notification.data,
                app_notification=form.app_notification.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} added.'.format(nickname))
        return redirect(url_for('add_user'))
    return render_template('add_user.html', form=form)


@app.route('/user/<nickname>/edit', methods=['GET', 'POST'])
def edit_user(nickname):
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


@app.route('/user/<nickname>/neworder', methods=['GET', 'POST'])
def new_order(nickname):
    form = NewOrderForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=nickname).first()
        order = Order(description=form.description.data,
                timestamp=datetime.utcnow(), user=user)
        db.session.add(order)
        db.session.commit()
        flash('New order added.')
        return redirect(url_for('new_order', nickname=nickname))

    return render_template('new_order.html', form=form)


@app.route('/user/<nickname>')
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    orders = user.orders.all()
    return render_template('user.html', user=user, orders=orders)


@app.route('/template/<name>/edit', methods=['GET', 'POST'])
def edit_template(name):
    form = EditTemplateForm()
    template = Template.query.filter_by(name=name).first()
    if request.method == 'POST':
        if form.validate():
            template.email_subject = form.email_subject.data
            template.email = form.email.data
            template.sms = form.sms.data
            template.app = form.app.data
            db.session.add(template)
            db.session.commit()
            flash('Changes for {} have been saved.'.format(nickname))
            return redirect(url_for('index'))
        else:
            render_template('edit_template.html', form=form)
    else:
        form.email_subject.data = template.email_subject
        form.email.data = template.email
        form.sms.data = template.sms
        form.app.data = template.app
    return render_template('edit_template.html', form=form)


@app.route('/template/add', methods=['GET', 'POST'])
def add_template():
    form = AddTemplateForm()
    if form.validate_on_submit():
        template = Template.query.filter_by(name=form.name.data).first()
        if template is not None:
            flash("There is already a template for this notification type.")
            return render_template('add_template.html', form=form)

        name = form.name.data
        template = Template(name=name, email_subject=form.email_subject.data,
                email=form.email.data, sms=form.sms.data, app=form.app.data)
        db.session.add(template)
        db.session.commit()
        flash('Template for notification type {} added.'.format(name))
        return redirect(url_for('index'))

    return render_template('add_template.html', form=form)


@app.route('/<order_id>/notify', methods=['GET', 'POST'])
def notify(order_id):
    form = NotifyForm()
    order = Order.query.filter_by(id=order_id).first()
    if form.validate_on_submit():
        if order is None:
            abort(404)
        template = form.notification_type.data
        send_notifications(order, template)
        flash("Sending notifications.")
        return redirect(url_for('user', nickname=order.user.nickname))

    return render_template('notify.html', form=form, order=order)
