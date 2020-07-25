from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user
from application.forms import LoginForm, RegisterForm, ForgotForm
from application.models import User
from application import mail, db
from flask_mail import Message


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')


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
                # msg = Message('Successful Register', sender='avik.royjan@gmail.com', recipients=[user.email])
                # msg.body = f'You have successfully registered for Roy Book Store! Come and buy books,{user.firstname}!
                # '
                # mail.send(msg)
                redirect(url_for('home'))
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
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page is not None or type(next_page) == "<class 'list'>":
                if next_page[0] != '/':
                    return redirect(next_page)
            else:
                return redirect(url_for('welcome'))
        else:
            flash('Username or password incorrect')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('home'))


@app.route('/forgot_password/form', methods=['GET', 'POST'])
def forgot_password_form():
    form = ForgotForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            msg = Message(subject='Forgot Password?', sender='avik.royjan@gmail.com', recipients=[email])
            msg.body = f"""Username: {user.username}
Password: {user.password}"""
            mail.send(msg)
            return redirect(url_for('forgot_password_conformation'))
        else:
            flash('Email not registered! Please try again.')
    return render_template('forgot.html', form=form)


@app.route('/forgot_password/conformation')
def forgot_password_conformation():
    return render_template('forgot_confirm.html')


@app.route('/account_info/<name>')
def account(name):
    return render_template('account.html', name=name)
