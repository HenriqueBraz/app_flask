from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired, InputRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    nome = StringField("nome", validators=[DataRequired()])
    email = EmailField("email", validators=[Email(), DataRequired()])
    password = PasswordField('password', [InputRequired(), EqualTo('confirm', message='Passwords must match'), Length(min=6, max=140)])
    confirm = PasswordField('repeat_password')
