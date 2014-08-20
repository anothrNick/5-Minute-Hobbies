__author__ = 'Nick'
from flask_wtf import Form
from wtforms import TextField, PasswordField, ValidationError
from wtforms.validators import DataRequired
from model import User

class RegisterForm(Form):
    fname = TextField("firstname", validators=[DataRequired("Please enter your first name.")])
    lname = TextField("lastname", validators=[DataRequired("Please enter your last name.")])
    username = TextField("username", validators=[DataRequired("Please enter a username.")])
    email = TextField("email", validators=[DataRequired("Please enter an email.")])
    password = PasswordField("password", validators=[DataRequired("Please enter a password.")])

    def validate_username(form, field):
        cnt = User.select().where(User.username == field.data).count()

        if cnt:
            raise ValidationError("This username is already in use.")

    def validate_email(form, field):
        cnt = User.select().where(User.email == field.data).count()

        if cnt:
            raise ValidationError("This email is already in use.")

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired("Please enter a username.")])
    password = PasswordField('password', validators=[DataRequired("Please enter a password.")])
