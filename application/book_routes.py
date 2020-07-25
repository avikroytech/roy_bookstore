from flask import current_app as app
from flask import render_template
from application.models import Book


@app.route('/books/<topic>')
def books(topic):
    all_books = Book.query.filter_by(topic=topic).all()
    return render_template('books.html', all=all_books, Book=Book)


@app.route('/book_info/<book_name>')
def book_info(book_name):
    book = Book.query.filter_by(name=book_name).first()
    return render_template('book_info.html', book=book)
