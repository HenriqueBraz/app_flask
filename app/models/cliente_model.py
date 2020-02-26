import logging
import json
from datetime import datetime
import pymysql


class ClienteModel(object):

    def __init__(self):

        with open('config.json') as f:
            conf = json.load(f)

        self.host = conf['mysql']['host']
        self.port = conf['mysql']['port']
        self.user = conf['mysql']['user']
        self.schema = conf['mysql']['schema']
        self.bank_pass = conf['mysql']['bank_pass']

        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.bank_pass)
        self.cur = self.con.cursor()
        self.cur.execute("USE " + self.schema)

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
        logging.info('Construtor do ClienteModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_company(self, id):
        try:
            self.cur.execute("SELECT e.id, e.empresa, e.created, u.nome, e.endereco, e.bairro, e.cidade, e.estado FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE  e.id = '{}' AND e.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            print(result)
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_company(: ' + str(e) + '\n')

    def get_companies(self):
        try:
            self.cur.execute("SELECT e.id, e.empresa, e.created, u.nome, e.endereco, e.bairro, e.cidade, e.estado FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE e.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_companies: ' + str(e) + '\n')

    def insert_company(self, id_natureza_juridica, id_porte_empresa, id_responsavel, empresa, endereco,
                       bairro, cidade, estado, capitalSocial, nire, cnpj, ie, ccm, cnaePrincipal, cnaeSecundaria,
                       tributacao, diaFaturamento, folhaPagamento, certificadoDigital, observacoes):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (
                id_natureza_juridica, id_porte_empresa, id_responsavel, data, empresa, endereco, bairro,
                cidade, estado, capitalSocial, nire, cnpj, ie, ccm, cnaePrincipal, cnaeSecundaria, tributacao,
                diaFaturamento,
                folhaPagamento, certificadoDigital, observacoes, data, data, 'Ativo')
            sql = "INSERT INTO empresas ( id_natureza_juridica, id_porte_empresa, id_responsavel, dataResponsavel, " \
                  "empresa, endereco, bairro, cidade, estado, capitalSocial, nire, cnpj, ie, ccm, cnaePrincipal, " \
                  "cnaeSecundaria,tributacao, diaFaturamento, folhaPagamento, certificadoDigital, observacoes, " \
                  "created, updated,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            logging.info('cliente cadastrada com sucesso')
            return True

        except Exception as e:
            logging.error('Erro em  ClienteModel, método insert_company: ' + str(e) + '\n')

    def find_one_id(self, user_id):
        try:
            self.cur.execute("SELECT * FROM empresas WHERE id = '{}'  AND empresas.status = 'Ativo'".format(user_id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em ClienteModel, método find_one_id: ' + str(e) + '\n')

    def update_company(self, empresa, natureza_juridica, porte, endereco, cidade, bairro, estado, capital_social, nire,
                       cnpj, inscricao_estadual, ccm, tributacao, cnae_principal, cnae_secundaria, dia_faturamento,
                       folha_pagamento, certificado_digital, observacoes, id_responsavel, id):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute("UPDATE empresas SET  id_natureza_juridica = '{}', id_porte_empresa = '{}',  id_responsavel = '{}',  empresa = '{}', endereco = '{}', bairro = '{}', cidade = '{}', estado = '{}', capitalSocial = '{}', nire = '{}', cnpj = '{}', ie = '{}', ccm = '{}', cnaePrincipal = '{}', cnaeSecundaria = '{}',  tributacao = '{}', diaFaturamento = '{}', folhaPagamento = '{}', certificadoDigital = '{}', observacoes = '{}',  updated = '{}'  WHERE id = {}".format(natureza_juridica, porte, id_responsavel, empresa, endereco, bairro, cidade, estado, capital_social, nire, cnpj, inscricao_estadual, ccm, cnae_principal, cnae_secundaria, tributacao, dia_faturamento, folha_pagamento, certificado_digital, observacoes, data, id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em ClienteModel, método update_company ' + str(e) + '\n')

    def update_status_company(self, id):
        try:
            self.cur.execute("UPDATE empresas SET status = 'Inativo' WHERE id = {}".format(id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em ClienteModel, método update_status_company' + str(e) + '\n')



