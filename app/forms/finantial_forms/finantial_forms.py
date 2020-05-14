from flask_wtf import FlaskForm
from wtforms import validators, TextAreaField, SelectField
from wtforms.validators import DataRequired


class FinantialForms(FlaskForm):
    mes = SelectField("mes", validators=[DataRequired()],
                      choices=[('01', 'jan'), ('02', 'fev'), ('03', 'mar'), ('04', 'abr'), ('05', 'mai'), ('06', 'jun'),
                               ('07', 'jul'), ('08', 'ago'), ('09', 'set'), ('10', 'out'), ('11', 'nov'), ('12', 'dez')])
    servico = TextAreaField(u'descricao', [validators.length(min=0, max=1000), validators.DataRequired()])

    letra = SelectField("letra", validators=[DataRequired()],
                        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'),
                                 ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'),
                                 ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'),
                                 ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'),
                                 ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                                 ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')])