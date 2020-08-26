import ast
from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user
from flask_mail import Message
from application import mail, db
from application.forms import LoginForm, RegisterForm, ForgotForm
from application.models import User, Book

"""Logging in and out
        Login
        Logout
        Register
        Forgot Password"""


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
                # msg.body = f'You have successfully registered for Roy BookStore! Come and buy books,{user.firstname}!
                # '
                # mail.send(msg)
                return redirect(url_for('login'))
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
                    return redirect(next_page[0])
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
            msg = Message('Forgot Password?', sender='avik.royjan@gmail.com', recipients=[f'{email}'])
            msg.body = f"Username: {user.username} Password: {user.password}"
            mail.send(msg)
            return redirect(url_for('forgot_password_conformation'))
        else:
            flash('Email not registered! Please try again. Or register it in our registration form.')
    return render_template('forgot.html', form=form)


@app.route('/forgot_password/conformation')
def forgot_password_conformation():
    return render_template('forgot_confirm.html')


"""Account Information
        Account
        Cart"""


@app.route('/account_info/<name>')
def account(name):
    return render_template('account.html', name=name)


@app.route('/cart/<name>')
def cart(name):
    cookies = request.cookies
    if 'cart_cookie' not in cookies:
        return render_template('cart.html', check='cart_cookie' in cookies)
    else:
        cookie = cookies['cart_cookie']
        cart_cookie = ast.literal_eval(cookie)
        books = []
        number = []
        total = 0
        for book_id in cart_cookie:
            split_bookid = book_id.split('-')
            bookid_str, num_of_books = [split_bookid[i] for i in (0, 1)]
            book = Book.query.filter_by(name=bookid_str).first()
            books.append(book)
            number.append(num_of_books)
            price = book.price * int(num_of_books)
            total += price
        return render_template('cart.html', name=name, books=books, check='cart_cookie' in cookies,
                               cart_cookie=cart_cookie, number=number, index=books.index, total=total,
                               length=len(cart_cookie))
