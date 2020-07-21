from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
from application.models import User


class RegisterForm(FlaskForm):
    first_name = StringField('First Name: ', validators=[DataRequired()])
    last_name = StringField('Last Name: ', validators=[DataRequired()])
    email = EmailField('Email: ', validators=[DataRequired(), Email()])
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), EqualTo('confirm', 'Fields have to be exact.')])
    confirm = PasswordField('Confirm Password: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return False
        else:
            return True

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            return False
        else:
            return True


class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def checklogin(self, username, password):
        user = User.query.get(username=username).first()
        if user:
            if user.password == password:
                return user
            else:
                return False
        else:
            return False


class ForgotForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
