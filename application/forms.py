from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField
from application.models import User


class RegisterForm(FlaskForm):
    first_name = StringField('First Name: ', validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name: ', validators=[DataRequired()], render_kw={"placeholder": "Last name"})
    email = EmailField('Email: ', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    username = StringField('Username: ', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password: ', validators=[DataRequired()], render_kw={"placeholder": "Password"})
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


class ForgotForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return True
        else:
            return False
