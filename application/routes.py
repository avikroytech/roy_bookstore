from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user
from application.forms import LoginForm, RegisterForm, ForgotForm
from application.models import User
from application import email, mail, db
from flask_mail import Message


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome(user):
    return render_template('welcome.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result1 = form.check_email(form.email)
        if result1:
            result2 = form.check_username(form.username)
            if result2:
                user = User(first=form.first_name.data, last=form.last_name.data, email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)
                db.session.add(user)
                db.session.commit()
                msg = Message('Successful Register', sender=email, recipients=[user.email])
                msg.body(f'You have successfully registered for Roy Book Store! Come and buy books, {user}!')
                mail.send(msg)
                redirect(url_for('welcome'))
            elif not result2:
                flash('Username already registered!')
        elif not result1:
            flash('Email already registered!')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username)
        if user.check_passsword(password) and user is not None:
            login_user(user)
            next_page = request.args.get('next')
            if next_page is not None or next_page[0] != '/':
                return redirect(next_page)
            return redirect('/welcome/user')
        else:
            flash('Username or password incorrect')
    return render_template('login.html', login_form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('home'))
