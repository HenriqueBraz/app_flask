from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, validators, StringField
from wtforms.validators import DataRequired


class OccurrencesRegisterForm(FlaskForm):
    cliente = SelectField("cliente", coerce=int, render_kw={'readonly': True}, choices=[])
    observacoes = TextAreaField(u'observacoes', [validators.length(min=0, max=500, message='O campo precisa ser menor que 500 caracteres')])
    status = SelectField("cliente", coerce=int, render_kw={'readonly': True}, choices=[])

class OccurrencesViewForm(FlaskForm):
    cliente = StringField("cliente", render_kw={'readonly': True}, validators=[DataRequired()])
    observacoes = TextAreaField(u'observacoes', render_kw={'readonly': True})
    status = StringField(u'status', render_kw={'readonly': True})

class OccurrencesEditForm(FlaskForm):
    cliente = StringField("cliente", render_kw={'readonly': True}, validators=[DataRequired()])
    observacoes = TextAreaField(u'observacoes', [validators.length(min=0, max=500, message='O campo precisa ser menor que 500 caracteres')])
    status = SelectField("status", validators=[DataRequired()],
                                      choices=[('Aberto', 'Aberto'), ('Fechado', 'Fechado'), ('Andamento', 'Andamento')])




