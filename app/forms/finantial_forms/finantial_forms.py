from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, DateField, IntegerField
from wtforms.validators import DataRequired

class FinantialForm(FlaskForm):
    periodo = DateField("perido", validators=[DataRequired()], format='%d/%m/%Y')
    dia_cobranca = SelectField("dia_cobranca", validators=[DataRequired()],
                                  choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                                           ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'),
                                           ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                                           ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'),
                                           ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'),
                                           ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')])