from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired


class ClientRegisterForm(FlaskForm):
    empresa = StringField("empresa", validators=[DataRequired()], render_kw={"placeholder": 'Empresa'})
    natureza_juridica = SelectField("natureza_juridica", render_kw={'readonly': True}, validators=[DataRequired()],
                                    choices=[('selecione', ' - selecione - '), ('201-1', '201-1 - Empresa Pública'),
                                             ('203-8', '203-8 - Sociedade de Economia Mista'),
                                             ('204-6', '204-6 - Sociedade Anônima Aberta'),
                                             ('205-4', '205-4 - Sociedade anônima Fechada'),
                                             ('206-2', '206-2 - Sociedade Empresária Limitada'),
                                             ('207-0', '207-0 - Sociedade Empresária em Nome Coletivo'),
                                             ('208-9', '208-9 - Sociedade Empresária em Comandita Simples'),
                                             ('209-7', '209-7 - Sociedade Empresária em Comandita por Ações'),
                                             ('212-7', '212-7 - Sociedade em Conta de participação'),
                                             ('214-3', '214-3 - Cooperativa'),
                                             ('215-1', '215-1 - Consórcio de Sociedades'),
                                             ('216-0', '216-0 - Grupo de sociedades'),
                                             ('223-2', '223-2 - Sociedade simples Pura'),
                                             ('224-0', '224-0 - Sociedade Simples Limitada'),
                                             ('225-9', '225-9 - Sociedade simples em Nome Coletivo'),
                                             ('226-7', '226-7 - Sociedade Simples em Comandita Simples'),
                                             ('229-1', '229-1 - Consórcio Simples'),
                                             ('230-5',
                                              '230-5 - Empresa Individual de Responsabilidade Limitada (de Natureza Empresária)'),
                                             ('231-3',
                                              '231-3 - Empresa Individual de Responsabilidade Limitada (de natureza Simples)'),
                                             ('232-1', '232-1 - Sociedade Unipessoal de Advogados'),
                                             ('306-9', '306-9 - Fundação Privada'),
                                             ('322-0', '322-0 - Organização Religiosa'),
                                             ('330-1', '330-1 - Organização Social(OS)'),
                                             ('399-9', '399-9 - Associação Privada'),
                                             ('408-1', '408-1 - Contribuínte Individual')])
    porte = SelectField("porte", render_kw={'readonly': True}, validators=[DataRequired()],
                        choices=[('ltda', 'LTDA'), ('eireli', 'EIRELI'), ('empresario', 'EMPRESÁRIO'), ('mei', 'MEI'),
                                 ('s/s', 'S/S'), ('s/a', 'S/A'), ('me', 'ME'),
                                 ('epp', 'EPP'), ('normal', 'Normal')])
    endereco = StringField("endereco", validators=[DataRequired()], render_kw={"placeholder": 'Endereço'})
    cidade = StringField("cidade", validators=[DataRequired()], render_kw={"placeholder": 'Cidade'})
    bairro = StringField("bairro", validators=[DataRequired()], render_kw={"placeholder": 'Bairro'})
    estado = SelectField("estado", validators=[DataRequired()],
                         choices=[('acre', 'Acre'), ('alagoas', 'Alagoas'), ('amapa', 'Amapá'),
                                  ('amazonas', 'Amazonas'), ('bahia', 'Bahia'), ('ceara', 'Ceara'),
                                  ('distrito_federal', 'Distrito Federal'), ('espírito_santo', 'Espírito Santo'),
                                  ('goias', 'Goiás'), ('maranhao', 'Maranhão'),
                                  ('mato_grosso', 'Mato Grosso'), ('mato_grosso_do_sul', 'Mato Grosso do Sul'),
                                  ('minas_gerais', 'Minas Gerais'), ('para', 'Pará'),
                                  ('paraiba', 'Paraíba'), ('parana', 'Paraná'), ('pernambuco', 'Pernambuco'),
                                  ('piaui', 'Piauí'), ('rio_de_janeiro', 'Rio de Janeiro'),
                                  ('rio_grande_do_norte', 'Rio Grande do Norte'),
                                  ('rio_grande_do_sul', 'Rio Grande do Sul'), ('rondonia', 'Rondônia'),
                                  ('roraima', 'Roraima'),
                                  ('santa_catarina', 'Santa Catarina'), ('sao_paulo', 'São Paulo'),
                                  ('sergipe', 'Sergipe'), ('tocantins', 'Tocantins')])
    capital_social = StringField("capital_social", validators=[DataRequired()], render_kw={"placeholder": 'Capital Social'})
    nire = StringField("nire", validators=[DataRequired()], render_kw={"placeholder": 'NIRE'})
    cnpj = StringField("cnpj", validators=[DataRequired()], render_kw={"placeholder": 'CNPJ'})
    inscricao_estadual = StringField("inscricao_estadual", validators=[DataRequired()], render_kw={"placeholder": 'Inscrição Estadual'})
    ccm = StringField("ccm", validators=[DataRequired()], render_kw={"placeholder": 'CCM'})
    tributacao = SelectField("tributacao", validators=[DataRequired()],
                             choices=[('simples_nacional', 'Simples Nacional'), ('presumido', 'Presumido'),
                                      ('real', 'Real')])
    cnae_principal = StringField("cnae_principal", validators=[DataRequired()], render_kw={"placeholder": 'cnae_principal'})
    cnae_secundaria = StringField("cnae_secundaria", validators=[DataRequired()], render_kw={"placeholder": 'cnae_secundaria'})
    dia_faturamento = SelectField("dia_faturamento", validators=[DataRequired()],
                                  choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                                           ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'),
                                           ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'),
                                           ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'),
                                           ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'),
                                           ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')])
    folha_pagamento = SelectField("folha_pagamento", validators=[DataRequired()], choices=[('sim', 'Sim'), ('nao', 'Não')])
    certificado_digital = SelectField("folha_pagamento", validators=[DataRequired()],choices=[('sim', 'Sim'), ('nao', 'Não')])
    observacoes = TextAreaField(u'observacoes', [validators.length(min=10, max=200)])
    submit = SubmitField('Submit')



