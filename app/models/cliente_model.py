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

    def get_nj_porte_nome(self, id):
        try:
            self.cur.execute(
                "SELECT inj.nome, ip.porte, u.nome FROM empresas e INNER JOIN info_natureza_juridica inj ON  inj.id=e.id_natureza_juridica INNER JOIN info_porte ip ON  ip.id=e.id_porte_empresa INNER JOIN usuarios u ON u.id=e.id_responsavel WHERE 1=1 AND e.id = '{}'".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_info_nj(: ' + str(e) + '\n')

    def get_info_nj(self):
        try:
            self.cur.execute("SELECT  inf.id, inf.codigo, inf.nome, inf.descricao FROM info_natureza_juridica inf  WHERE  inf.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_info_nj(: ' + str(e) + '\n')

    def get_info_porte(self):
        try:
            self.cur.execute("SELECT  ip.id, ip.porte, ip.nome FROM info_porte ip  WHERE  ip.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_info_porte(: ' + str(e) + '\n')

    def get_company(self, id):
        try:
            self.cur.execute("SELECT e.id, e.empresa, e.created, u.nome, e.endereco, e.bairro, e.cidade, e.estado FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE  e.id = '{}' AND e.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_company(: ' + str(e) + '\n')

    def get_companies(self):
        try:
            self.cur.execute("SELECT e.id, e.empresa, e.created, u.nome, e.cnpj, e.ccm, e.endereco, e.bairro, e.cidade, e.estado FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE e.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_companies: ' + str(e) + '\n')

    def insert_company(self, nome_responsavel, id_natureza_juridica, id_porte_empresa, id_responsavel, empresa, endereco,
                       bairro, cidade, estado, capitalSocial, nire, cnpj, ie, ccm, cnaePrincipal, cnaeSecundaria,
                       tributacao, diaFaturamento, folhaPagamento, certificadoDigital, observacoes, nome, telefone, email, path, filename, descricao, size, type, md5, flag):
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
            self.cur.execute("SELECT MAX(id) FROM empresas;")
            result = self.cur.fetchone()
            sql_data = (result, nome, telefone, email, data, data, 'Ativo')
            sql = "INSERT INTO empresas_contato (id_empresa, nome, telefone, email, created, updated, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            sql_data = (result, nome_responsavel, data, data, 'Ativo')
            sql = "INSERT INTO empresas_responsavel (id_empresa, id_usuario, created, updated, status) VALUES (%s, %s, %s, %s, %s)"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            if flag:
                sql_data = (result, path, filename, descricao, size, type, md5, data, data)
                sql = "INSERT INTO anexos (id_empresa, path, filename, descricao, size, type, md5, created, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                self.cur.execute(sql, sql_data)
                self.con.commit()
            logging.info('cliente cadastrado com sucesso')
            return True

        except Exception as e:
            logging.error('Erro em  ClienteModel, método insert_company: ' + str(e) + '\n')

    def find_one_id(self, user_id):
        try:
            self.cur.execute("SELECT e.*, ec.nome, ec.telefone, ec.email  FROM empresas e LEFT JOIN  empresas_contato ec  ON  e.id = ec.id_empresa WHERE e.id = '{}'  AND e.status = 'Ativo'".format(user_id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em ClienteModel, método find_one_id: ' + str(e) + '\n')

    def update_company(self, empresa, natureza_juridica, porte, endereco, cidade, bairro, estado, capital_social, nire,
                       cnpj, inscricao_estadual, ccm, tributacao, cnae_principal, cnae_secundaria, dia_faturamento,
                       folha_pagamento, certificado_digital, observacoes, id_responsavel, id, nome, telefone, email):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute("UPDATE empresas SET  id_natureza_juridica = '{}', id_porte_empresa = '{}',  id_responsavel = '{}',  empresa = '{}', endereco = '{}', bairro = '{}', cidade = '{}', estado = '{}', capitalSocial = '{}', nire = '{}', cnpj = '{}', ie = '{}', ccm = '{}', cnaePrincipal = '{}', cnaeSecundaria = '{}',  tributacao = '{}', diaFaturamento = '{}', folhaPagamento = '{}', certificadoDigital = '{}', observacoes = '{}',  updated = '{}'  WHERE id = {}".format(natureza_juridica, porte, id_responsavel, empresa, endereco, bairro, cidade, estado, capital_social, nire, cnpj, inscricao_estadual, ccm, cnae_principal, cnae_secundaria, tributacao, dia_faturamento, folha_pagamento, certificado_digital, observacoes, data, id))
            self.con.commit()
            self.cur.execute("UPDATE empresas_contato SET  nome = '{}', telefone = '{}', email = '{}', updated = '{}' WHERE id_empresa = '{}'".format(nome, telefone, email, data, id))
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



