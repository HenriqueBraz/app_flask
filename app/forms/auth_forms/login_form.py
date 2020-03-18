from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    email = EmailField("email", validators=[Email()])
