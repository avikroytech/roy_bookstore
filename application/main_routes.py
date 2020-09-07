import os
import stripe
from flask import current_app as app, jsonify, flash, redirect, request, make_response
from flask_login import current_user
from flask import render_template
from application import db
from application.bookinfo import books
from application.models import Book, User

for topic in books:
    for book in topic:
        if Book.query.filter_by(name=book["Name"]).first():
            continue
        else:
            databook = Book(book["Name"], book["Author"], book["Summary"], book["Price"], book["Topic"], book["Image"])
            db.session.add(databook)
            db.session.commit()

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}

stripe.api_key = stripe_keys["secret_key"]


@app.route('/')
def home():
    return render_template('home.html', app=app)


@app.errorhandler(404)
def error(e):
    return render_template('404error.html'), 404


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        list_of_books = []
        cart_cookie = eval(request.cookies['cart_cookie'])
        for book_id in cart_cookie:
            bookid_str, num = book_id.split('-')
            book_ob = Book.query.filter_by(name=bookid_str).first()
            # price1, price2 = str(book_ob.price).split('.')
            price = int((book_ob.price * 1.05) * 100)
            dictionary = {'name': book_ob.name, 'quantity': int(num), 'amount': f'{int(price)}', 'currency': 'cad'}
            print(dictionary)
            list_of_books.append(dictionary)

        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=list_of_books
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/success")
def success():
    flash('Transaction succeeded')
    resp = make_response(redirect(f'/cart/{current_user.firstname}'))
    resp.delete_cookie('cart_cookie')
    return resp


@app.route("/cancelled")
def cancelled():
    flash('Transaction cancelled')
    return redirect(f'/cart/{current_user.firstname}')


@app.route('/delete')
def delete():
    vivek = User.query.filter_by(username='vivek').first()
    db.session.delete(vivek)
    db.session.commit()
    return str(vivek)
