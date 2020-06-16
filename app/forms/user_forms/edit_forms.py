from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired, EqualTo


class EditFormUser(FlaskForm):
    username = StringField("username", render_kw={'readonly': True}, validators=[DataRequired()])
    nome = StringField("nome", render_kw={'readonly': True}, validators=[DataRequired()])
    email = EmailField("email", validators=[Email()])
    password = PasswordField('password', [EqualTo('confirm', message='Senhas precisam ser iguais!')])
    confirm = PasswordField('repeat_password')
    group = SelectField("grupo", render_kw={'readonly': True},  validators=[DataRequired()],choices=[('Usuario','Usuário')])


class EditFormAdmin(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    nome = StringField("nome", validators=[DataRequired()])
    email = EmailField("email", validators=[Email()])
    password = PasswordField('password', [EqualTo('confirm', message='Senhas precisam ser iguais!')])
    confirm = PasswordField('repeat_password')
    group = SelectField("grupo", validators=[DataRequired()],choices=[('Usuario','Usuário'), ('Administrador','Administrador')])