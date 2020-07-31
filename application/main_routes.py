import json

from flask import current_app as app
from flask import render_template
from application.models import Book
from application import db
from application.bookinfo import books

for topic in books:
    for book in topic:
        if Book.query.filter_by(name=book["Name"]).first():
            continue
        else:
            databook = Book(book["Name"], book["Author"], book["Summary"], book["Price"], book["Topic"], book["Image"])
            db.session.add(databook)
            db.session.commit()


@app.route('/')
def home():
    return render_template('home.html')
