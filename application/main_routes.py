import os
import stripe
from flask import current_app as app
from flask import render_template
from application import db
from application.bookinfo import books
from application.models import Book

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
