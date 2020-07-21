from application import db, login_manager
from flask_login import UserMixin


class Book(db.Model):
    __tablename__ = 'Book_Information'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    summary = db.Column(db.String(1000), index=True)
    price = db.Column(db.Float(3), index=True)

    def __init__(self, name, author, summary, price):
        self.name = name
        self.author = author
        self.summary = summary
        self.price = price


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'User_Information'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128), index=True)

    def __init__(self, first, last, email, username, password):
        self.firstname = first
        self.lastname = last
        self.email = email
        self.username = username
        self.password = password

    def checkusername(self, username):
        if username == self.username:
            return True
        else:
            return False

    def checkpassword(self, password):
        if password == self.password:
            return True
        else:
            return False