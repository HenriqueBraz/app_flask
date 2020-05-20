from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, validators, ValidationError
from wtforms.fields import DecimalField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
import phonenumbers


def validate_phone(message='Invalid phone number.', region=None):
    """ This validates the phone number using the phonenumbers package.
    Make sure to select a default region in order to validate numbers
    that do not follow the international format.
    """

    def _validate_phone(form, field):
        try:
            input_number = phonenumbers.parse(field.data, region)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError(message)
        except:
            raise ValidationError(message)

    return _validate_phone


class ClientForm(FlaskForm):
    nome_responsavel = SelectField("nome_responsavel", coerce=int, render_kw={'readonly': True}, choices=[])
    empresa = StringField("cliente", validators=[DataRequired()], render_kw={"placeholder": 'Empresa'})
    natureza_juridica = SelectField("natureza_juridica", coerce=int, render_kw={'readonly': True}, choices=[])
    porte = SelectField("porte", coerce=int, render_kw={'readonly': True}, choices=[])
    endereco = StringField("endereco", validators=[DataRequired()], render_kw={"placeholder": 'Endereço'})
    cidade = StringField("cidade", validators=[DataRequired()], render_kw={"placeholder": 'Cidade'})
    bairro = StringField("bairro", validators=[DataRequired()], render_kw={"placeholder": 'Bairro'})
    estado = SelectField("estado", validators=[DataRequired()],
                         choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
                                  ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceara'),
                                  ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                                  ('GO', 'Goiás'), ('MA', 'Maranhão'),
                                  ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
                                  ('MG', 'Minas Gerais'), ('PA', 'Pará'),
                                  ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'),
                                  ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                                  ('RN', 'Rio Grande do Norte'),
                                  ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),
                                  ('RR', 'Roraima'),
                                  ('SC', 'Santa Catarina'), ('SP', 'São Paulo'),
                                  ('SE', 'Sergipe'), ('TO', 'Tocantins')])
    nome = StringField("nome", validators=[DataRequired()], render_kw={"placeholder": 'Nome'})
    telefone = StringField("telefone", validators=[validate_phone(region='BR', message="Você precisa entrar com uma telefone válido.")],render_kw={"placeholder": 'Telefone'})
    celular = StringField("celular", validators=[validate_phone(region='BR', message="Você precisa entrar com uma telefone válido.")],render_kw={"placeholder": 'Celular'})
    email = EmailField("email", validators=[Email(), DataRequired()], render_kw={"placeholder": 'Digite o Email'})
    capital_social = StringField("capital_social", validators=[DataRequired()], render_kw={"placeholder": 'Digite o Capital Social'})
    nire = StringField("nire", validators=[DataRequired()], render_kw={"placeholder": 'Digite o NIRE'})
    cnpj = StringField("cnpj", validators=[DataRequired()], render_kw={"placeholder": 'Digite o CNPJ'})
    inscricao_estadual = StringField("inscricao_estadual", validators=[DataRequired()],
                                     render_kw={"placeholder": 'Inscrição Estadual'})
    ccm = StringField("ccm", validators=[DataRequired()], render_kw={"placeholder": 'Digite o CCM'})
    tributacao = SelectField("tributacao", validators=[DataRequired()],
                             choices=[('SIMPLES NACIONAL', 'Simples Nacional'), ('PRESUMIDO', 'Presumido'),
                                      ('REAL', 'Real')])
    cnae_principal = StringField("cnae_principal", validators=[DataRequired()], render_kw={"placeholder": 'Digite o CNAE principal'})
    cnae_secundaria = StringField("cnae_secundaria", render_kw={"placeholder": 'Digite o CNAE secundario'})
    dia_faturamento = SelectField("dia_faturamento", validators=[DataRequired()],
                                  choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                                           ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'),
                                           ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                                           ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'),
                                           ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'),
                                           ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')])
    folha_pagamento = SelectField("folha_pagamento", validators=[DataRequired()],
                                  choices=[('sim', 'Sim'), ('nao', 'Não')])
    certificado_digital = SelectField("folha_pagamento", validators=[DataRequired()],
                                      choices=[('sim', 'Sim'), ('nao', 'Não')])
    observacoes = TextAreaField(u'observacoes', [validators.length(min=0, max=200)])


class AnexoForm(FlaskForm):
    titulo = StringField(u'titulo', [validators.length(min=0, max=50), validators.DataRequired()])
