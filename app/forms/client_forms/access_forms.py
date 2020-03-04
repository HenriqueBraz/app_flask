from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, DateField, IntegerField
from wtforms.validators import DataRequired


class AccessForm(FlaskForm):

    codigoAcessoSimples = StringField("codigoAcessoSimples", validators=[DataRequired(message='Campo Obrigatório')], render_kw={"placeholder": 'Código'})
    AcessoECAC = StringField("AcessoECAC", validators=[DataRequired(message='Campo Obrigatório')], render_kw={"placeholder": 'Acesso E-CAC'})
    usernamePF = StringField("usernamePF", validators=[DataRequired(message='Campo Obrigatório')], render_kw={"placeholder": 'Username Posto Fiscal'})
    senhaPF = StringField("senhaPF ", validators=[DataRequired(message='Campo Obrigatório')], render_kw={"placeholder": 'Senha Posto Fiscal'})
    senhaPrefeitura = StringField("senhaPrefeitura", validators=[DataRequired(message='Campo Obrigatório')], render_kw={"placeholder": 'Senha Prefeitura'})
    senhaINSS = StringField("senhaINSS", render_kw={"placeholder": 'Senha INSS'})
    responsavelReceita = StringField("responsavelReceita", validators=[DataRequired(message='Campo Obrigatório')], render_kw={"placeholder": 'Responsável Receita'})
