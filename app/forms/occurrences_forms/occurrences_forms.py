from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, validators


class OccurrencesRegisterForm(FlaskForm):
    cliente = SelectField("cliente", coerce=int, render_kw={'readonly': True}, choices=[])
    observacoes = TextAreaField(u'observacoes', [validators.length(min=0, max=200)])
