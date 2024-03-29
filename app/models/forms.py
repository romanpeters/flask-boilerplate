from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm password")
    submit = SubmitField("Submit")
