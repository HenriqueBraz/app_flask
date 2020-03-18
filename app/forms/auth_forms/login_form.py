from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))


class LoginFormForgotPass(FlaskForm):
    email = EmailField("email", validators=[Email(message='Email inválido!'), DataRequired()])
