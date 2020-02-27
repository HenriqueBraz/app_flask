from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, validators,  ValidationError
from wtforms.fields import DecimalField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
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


class ClientRegisterForm(FlaskForm):
    empresa = StringField("cliente", validators=[DataRequired()], render_kw={"placeholder": 'Empresa'})
    natureza_juridica = SelectField("natureza_juridica", render_kw={'readonly': True}, validators=[DataRequired()],
                                    choices=[('selecione', ' - selecione - '), ('1', '201-1 - Empresa Pública'),
                                             ('2', '203-8 - Sociedade de Economia Mista'),
                                             ('3', '204-6 - Sociedade Anônima Aberta'),
                                             ('4', '205-4 - Sociedade anônima Fechada'),
                                             ('5', '206-2 - Sociedade Empresária Limitada'),
                                             ('6', '207-0 - Sociedade Empresária em Nome Coletivo'),
                                             ('7', '208-9 - Sociedade Empresária em Comandita Simples'),
                                             ('8', '209-7 - Sociedade Empresária em Comandita por Ações'),
                                             ('9', '212-7 - Sociedade em Conta de participação'),
                                             ('10', '214-3 - Cooperativa'),
                                             ('11', '215-1 - Consórcio de Sociedades'),
                                             ('12', '216-0 - Grupo de sociedades'),
                                             ('13', '223-2 - Sociedade simples Pura'),
                                             ('14', '224-0 - Sociedade Simples Limitada'),
                                             ('15', '225-9 - Sociedade simples em Nome Coletivo'),
                                             ('16', '226-7 - Sociedade Simples em Comandita Simples'),
                                             ('17', '229-1 - Consórcio Simples'),
                                             ('18',
                                              '230-5 - Empresa Individual de Responsabilidade Limitada (de Natureza Empresária)'),
                                             ('19',
                                              '231-3 - Empresa Individual de Responsabilidade Limitada (de natureza Simples)'),
                                             ('20', '232-1 - Sociedade Unipessoal de Advogados'),
                                             ('21', '306-9 - Fundação Privada'),
                                             ('22', '322-0 - Organização Religiosa'),
                                             ('23', '330-1 - Organização Social(OS)'),
                                             ('24', '399-9 - Associação Privada'),
                                             ('25', '408-1 - Contribuínte Individual')])
    porte = SelectField("porte", render_kw={'readonly': True}, validators=[DataRequired()],
                        choices=[('1', 'LTDA'), ('2', 'EIRELI'), ('3', 'EMPRESÁRIO'), ('4', 'MEI'),
                                 ('5', 'S/S'), ('6', 'S/A'), ('7', 'ME'),
                                 ('8', 'EPP'), ('9', 'Normal')])
    endereco = StringField("endereco", validators=[DataRequired()], render_kw={"placeholder": 'Endereço'})
    cidade = StringField("cidade", validators=[DataRequired()], render_kw={"placeholder": 'Cidade'})
    bairro = StringField("bairro", validators=[DataRequired()], render_kw={"placeholder": 'Bairro'})
    estado = SelectField("estado", validators=[DataRequired()],
                         choices=[('ac', 'Acre'), ('al', 'Alagoas'), ('ap', 'Amapá'),
                                  ('am', 'Amazonas'), ('ba', 'Bahia'), ('ce', 'Ceara'),
                                  ('df', 'Distrito Federal'), ('es', 'Espírito Santo'),
                                  ('go', 'Goiás'), ('ma', 'Maranhão'),
                                  ('mt', 'Mato Grosso'), ('ms', 'Mato Grosso do Sul'),
                                  ('mg', 'Minas Gerais'), ('pa', 'Pará'),
                                  ('pb', 'Paraíba'), ('pr', 'Paraná'), ('pe', 'Pernambuco'),
                                  ('pi', 'Piauí'), ('rj', 'Rio de Janeiro'),
                                  ('rn', 'Rio Grande do Norte'),
                                  ('rs', 'Rio Grande do Sul'), ('ro', 'Rondônia'),
                                  ('rr', 'Roraima'),
                                  ('sc', 'Santa Catarina'), ('sp', 'São Paulo'),
                                  ('se', 'Sergipe'), ('to', 'Tocantins')])
    nome = StringField("nome", validators=[DataRequired()],  render_kw={"placeholder": 'Nome'})
    telefone = StringField("telefone", validators=[validate_phone(region='BR')], render_kw={"placeholder": '(dd)ddddd-dddd'})
    email = EmailField("email", validators=[Email(), DataRequired()], render_kw={"placeholder": 'Email'})
    capital_social = DecimalField(places=0, validators=[DataRequired()], render_kw={"placeholder": 'Capital Social'})
    nire = StringField("nire", validators=[DataRequired()], render_kw={"placeholder": 'NIRE'})
    cnpj = StringField("cnpj", validators=[DataRequired()], render_kw={"placeholder": 'CNPJ'})
    inscricao_estadual = StringField("inscricao_estadual", validators=[DataRequired()],
                                     render_kw={"placeholder": 'Inscrição Estadual'})
    ccm = StringField("ccm", validators=[DataRequired()], render_kw={"placeholder": 'CCM'})
    tributacao = SelectField("tributacao", validators=[DataRequired()],
                             choices=[('SIMPLES NACIONAL', 'Simples Nacional'), ('PRESUMIDO', 'Presumido'),
                                      ('REAL', 'Real')])
    cnae_principal = StringField("cnae_principal", validators=[DataRequired()],
                                 render_kw={"placeholder": 'cnae_principal'})
    cnae_secundaria = StringField("cnae_secundaria", validators=[DataRequired()],
                                  render_kw={"placeholder": 'cnae_secundaria'})
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
