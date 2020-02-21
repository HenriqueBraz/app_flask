from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()], widget=PasswordInput(hide_value=False))
