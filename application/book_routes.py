import ast
import json
import random
from flask import current_app as app, make_response, render_template, request, redirect
from flask_login import current_user, login_required
import stripe
from application.forms import CheckoutForm
from application.models import Book


def duplicate(string):
    num = random.randint(1, 5)
    return f"{string}" * num


@app.route('/books/<topic>')
def books(topic):
    all_books = Book.query.filter_by(topic=topic).all()
    return render_template('books.html', books=all_books, Book=Book, topic=topic, duplicate=duplicate, app=app)


@app.route('/book_info/<book_name>')
def book_info(book_name):
    book = Book.query.filter_by(name=book_name).first()
    return render_template('book_info.html', book=book)


@app.route('/add_to_cart/<book_id>')
@login_required
def add_to_cart(book_id):
    incoming_cookies_dict = request.cookies
    resp = make_response(redirect(f'/cart/{current_user.firstname}'))
    updated_bookid_and_number = []
    book_ids = []
    if 'cart_cookie' in incoming_cookies_dict:
        cart_cookie_list = eval(incoming_cookies_dict['cart_cookie'])
        # entry of the list is : bookid-n where n is the number of books added
        for bookid_and_number in cart_cookie_list:
            bookid_str, number_of_books = bookid_and_number.split('-')
            book_ids.append(bookid_str)
            if bookid_str == book_id:
                book_num = int(number_of_books)
                book_num += 1
                number_of_books = str(book_num)
                updated_bookid_and_number.append(f'{bookid_str}-{number_of_books}')
            else:
                updated_bookid_and_number.append(f'{bookid_str}-{number_of_books}')

        if book_id not in book_ids:
            updated_bookid_and_number.append(f'{book_id}-1')
    else:
        # create a new list add the book id and '1' to that list
        # create a new cookie and add this list to the cookie value
        # put this new cookie into the response
        # bytes = json.dumps(book_id).encode('utf-8')
        updated_bookid_and_number.append(f'{book_id}-1')
    # add the updated list into the cookie and then in the response.
    book_list_bytes = json.dumps(updated_bookid_and_number).encode('utf-8')
    resp.set_cookie('cart_cookie', book_list_bytes)
    return resp


@app.route('/remove_from_cart/<book_id>')
@login_required
def remove_from_cart(book_id):
    resp = make_response(redirect(f'/cart/{current_user.firstname}'))
    cookies = request.cookies
    cart_cookie = ast.literal_eval(cookies['cart_cookie'])
    updated_bookid_and_number = []
    for bookid in cart_cookie:
        split_bookid = bookid.split('-')
        bookid_str, num_of_book = [split_bookid[i] for i in (0, 1)]
        if book_id == bookid_str:
            number = int(num_of_book)
            if number > 1:
                number -= 1
                updated_bookid_and_number.append(f'{bookid_str}-{number}')
            elif number == 1:
                number = 0
        else:
            updated_bookid_and_number.append(f'{bookid_str}-{num_of_book}')
    book_list_bytes = json.dumps(updated_bookid_and_number).encode('utf-8')
    resp.set_cookie('cart_cookie', book_list_bytes)
    return resp


@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    cookies = request.cookies
    checkoutform = CheckoutForm()
    addressform = checkoutform.AddressForm()
    deliveryform = checkoutform.DeliveryForm()
    payform = checkoutform.PaymentForm()
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
        return render_template('payment.html', books=books, number=number, index=books.index, total=total,
                               checkout=checkoutform, address=addressform, delivery=deliveryform, pay=payform)


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)