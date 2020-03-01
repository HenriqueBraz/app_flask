from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired

from app.forms.client_forms.client_form import validate_phone


class RegisterFormAccouting(FlaskForm):
    contabilidade = StringField("contabilidade", validators=[DataRequired()])
    nome = StringField("nome", validators=[DataRequired()], render_kw={"placeholder": 'Nome'})
    telefone = StringField("telefone", validators=[validate_phone(region='BR', message="Você precisa entrar com uma telefone válido.")], render_kw={"placeholder": '(dd)ddddd-dddd'})
    email = EmailField("email", validators=[Email(), DataRequired()], render_kw={"placeholder": 'Email'})
    dataEntrada = DateField("dataEntrada", validators=[DataRequired(message="Você precisa entrar com uma data válida.")], format='%d/%m/%Y', render_kw={"placeholder": 'dd/mm/aaaa'})
