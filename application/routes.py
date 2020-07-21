from flask import current_app as app
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user
from application.forms import LoginForm, RegisterForm, ForgotForm
from application.models import User
from application import email, mail
from flask_mail import Message


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome/user')
@login_required
def welcome(user):
    return render_template('welcome.html', user=user)


@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result1 = form.check_email(form.email)
        if not result1:
            result2 = form.check_username(form.username)
            if not result2:
                user = User(form.first_name.data, form.last_name.data, form.email.data, form.username.data,
                            form.password.data)
                msg = Message('Successful Register', sender=email, recipients=[user.email])
                msg.body(f'You have successfully registered for Roy Book Store! Come and buy books, {user.firstname}!')
                mail.send(msg)
                redirect(url_for(''))
            elif result2:
                flash('Username already registered!')
        elif result1:
            flash('Email already registered!')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.apssword.data
        result = form.checklogin(username, password)
        if result:
            return redirect('/welcome/result')
        else:
            flash('')
    return render_template('login.html', login_form=form)
