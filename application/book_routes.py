import json
from flask import current_app as app, make_response, render_template, request, redirect
from flask_login import current_user

from application.models import Book, Cart


@app.route('/books/<topic>')
def books(topic):
    all_books = Book.query.filter_by(topic=topic).all()
    return render_template('books.html', all=all_books, Book=Book)


@app.route('/book_info/<book_name>')
def book_info(book_name):
    book = Book.query.filter_by(name=book_name).first()
    cookies = request.cookies
    resp = make_response()
    cart = Cart()
    cart_bytes = json.dumps(cart.books).encode('utf-8')
    resp.set_cookie('cart_cookie', cart_bytes)
    return render_template('book_info.html')


@app.route('/add_to_cart/<book_name>')
def add_to_cart(book_name):
    incoming_cookies_dict = request.cookies
    cart = eval(incoming_cookies_dict['cart_cookie'])
    cart[f'{book_name}'] = book_name
    return redirect(f'cart/{current_user.firstname}')
