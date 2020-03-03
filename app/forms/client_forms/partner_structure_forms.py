from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators, DateField, IntegerField
from wtforms.validators import DataRequired



class PartnerForm(FlaskForm):

    nome = StringField("nome", validators=[DataRequired()], render_kw={"placeholder": 'Nome'})
    endereco = StringField("endereco", validators=[DataRequired()], render_kw={"placeholder": 'Endereço'})
    bairro = StringField("bairro", validators=[DataRequired()], render_kw={"placeholder": 'Bairro'})
    cidade = StringField("cidade", validators=[DataRequired()], render_kw={"placeholder": 'Cidade'})
    naturalidade = StringField("naturalidade", validators=[DataRequired()], render_kw={"placeholder": 'Naturalidade'})
    nacionalidade = StringField("nacionalidade", validators=[DataRequired()], render_kw={"placeholder": 'Nacionalidade'})
    estadoCivil = SelectField("estadoCivil", validators=[DataRequired()], choices=[('Solteiro(a)', 'Solteiro(a)'), ('Casado(a)', 'Casado(a)')])
    profissao = StringField("profissao", validators=[DataRequired()], render_kw={"placeholder": 'Profissao'})
    rg = StringField("rg", validators=[DataRequired()], render_kw={"placeholder": 'RG'})
    rgDataExpedicao = DateField("rgDataExpedicao", validators=[DataRequired(message="Você precisa entrar com uma data válida.")], format='%d/%m/%Y', render_kw={"placeholder": 'dd/mm/aaaa'})
    cpf = StringField("cpf", validators=[DataRequired()], render_kw={"placeholder": 'CPF'})
    dataNascimento = DateField("dataNascimento", validators=[DataRequired(message="Você precisa entrar com uma data válida.")], format='%d/%m/%Y', render_kw={"placeholder": 'dd/mm/aaaa'})
    nomeMae = StringField("nomeMae", validators=[DataRequired()], render_kw={"placeholder": 'Nome da Mãe'})
    nomePai = StringField("nomePai", validators=[DataRequired()], render_kw={"placeholder": 'Nome do Pai'})
    participacaoCapitalSocial = SelectField("participacaoCapitalSocial", validators=[DataRequired()], choices=[('Percentual', 'Percentual'), ('Cotas', 'Cotas')])
    socioAdministrador = SelectField("socioAdministrador", validators=[DataRequired()], choices=[('Sim', 'Sim'), ('Nao', 'Nao')])
    proLabore = SelectField(" proLabore", validators=[DataRequired()], choices=[('Sim', 'Sim'), ('Nao', 'Nao')])
    proLaboreValor = IntegerField('proLaboreValor', [validators.required(message='Somente números')], render_kw={"placeholder": 'Valor do Pro-labore'})
    reponsavelReceita = SelectField("reponsavelReceita ", validators=[DataRequired()], choices=[('Sim', 'Sim'), ('Nao', 'Nao')])
    pis = StringField("pis", validators=[DataRequired()], render_kw={"placeholder": 'PIS'})



