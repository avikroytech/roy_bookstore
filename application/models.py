import random
from application import db, login_manager
from flask_login import UserMixin


class Book(db.Model):
    __tablename__ = 'Book_Information'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), index=True, nullable=False)
    topic = db.Column(db.String(64), index=True, nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)
    summary = db.Column(db.String(1000), index=True, nullable=False)
    image = db.Column(db.String(1000), index=True, nullable=False)
    # users = db.Column(db.String(20), db.ForeignKey('User_Information.name'), index=True, nullable=True)
    price = db.Column(db.Float(3), index=True, nullable=False)

    def __init__(self, name, author, summary, price, topic, image):
        self.name = name
        self.author = author
        self.summary = summary
        self.price = price
        self.topic = topic
        self.image = image


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'User_Information'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), index=True, nullable=False)

    def __init__(self, first, last, email, username, password):
        self.firstname = first
        self.lastname = last
        self.email = email
        self.username = username
        self.password = password

    def check_password(self, password):
        if password == self.password:
            return True
        else:
            return False


class Cart:
    def __init__(self):
        self.cart_id = random.randint(0, 10000)
        self.books = {}

    def add_book(self, book_id):
        self.books[f'{book_id}'] = book_id

    def remove_book(self, book_id):
        del self.books[f'{book_id}']
