import decimal
from flask_wtf import FlaskForm
from wtforms import validators, TextAreaField, DecimalField, RadioField
from wtforms.validators import DataRequired


class FinantialForms(FlaskForm):
    servico = TextAreaField(u'descricao', [validators.length(min=0, max=1000), validators.DataRequired()])
    valor = DecimalField(render_kw={"placeholder": '0.00'}, validators=[DataRequired()])

