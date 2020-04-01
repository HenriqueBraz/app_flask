from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, DateField, IntegerField
from wtforms.validators import DataRequired

class FinantialForm(FlaskForm):
    periodo = DateField("data_nascimento", validators=[DataRequired()], format='%d/%m/%Y')