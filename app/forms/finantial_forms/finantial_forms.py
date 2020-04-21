from flask_wtf import FlaskForm
from wtforms import validators, TextAreaField, DecimalField, SelectField
from wtforms.validators import DataRequired


class FinantialForms(FlaskForm):
    mes = SelectField("mes", validators=[DataRequired()],
                      choices=[('01', 'jan'), ('02', 'fev'), ('03', 'mar'), ('04', 'abr'), ('05', 'mai'), ('06', 'jun'),
                               ('07', 'jul'), ('08', 'ago'), ('09', 'set'), ('10', 'out'), ('11', 'nov'), ('12', 'dez')])
    servico = TextAreaField(u'descricao', [validators.length(min=0, max=1000), validators.DataRequired()])
    valor = DecimalField(render_kw={"placeholder": '0,00'}, validators=[DataRequired()])

