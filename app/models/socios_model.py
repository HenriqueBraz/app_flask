import logging
import json
from datetime import datetime
import pymysql


class SociosModel(object):

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
        logging.info('Construtor do SociosModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_partner(self, id):
        try:
            self.cur.execute("SELECT * FROM empresas_socios es LEFT JOIN  empresas e ON e.id = es.id_empresa  WHERE  1=1 AND  es.id = '{}' AND  e.status = 'Ativo' AND es.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  SociosModel, método get_partner: ' + str(e) + '\n')

    def get_id_company(self, id):
        try:
            self.cur.execute("SELECT e.id FROM  empresas e LEFT JOIN  empresas_socios  es  ON e.id = es.id_empresa  WHERE  1=1 AND  es.id = '{}' AND  e.status = 'Ativo' AND es.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  SociosModel, método get_partner: ' + str(e) + '\n')

    def get_partners(self, id):
        try:
            self.cur.execute("SELECT  es.id, es.nome, es.cpf, es.participacaoCapitalSocial FROM empresas_socios es LEFT JOIN  empresas e ON  e.id = '{}' AND  e.id = es.id_empresa  WHERE e.status = 'Ativo' AND es.status = 'Ativo';".format(id))
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  SociosModel, método get_partners: ' + str(e) + '\n')


    def insert_partner(self, id, nome, endereco, bairro, cidade, naturalidade, nacionalidade, estadoCivil, profissao,
                       rg, rgDataExpedicao, cpf, dataNascimento, nomeMae, nomePai, participacaoCapitalSocial,
                       socioAdministrador, proLabore, proLaboreValor, reponsavelReceita, pis):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (id, nome, endereco, bairro, cidade, naturalidade, nacionalidade, estadoCivil, profissao, rg,
                        rgDataExpedicao, cpf, dataNascimento, nomeMae, nomePai, participacaoCapitalSocial,
                        socioAdministrador, proLabore, proLaboreValor, reponsavelReceita, pis, data, data)
            sql = "INSERT INTO empresas_socios (id_empresa, nome, endereco, bairro, cidade, naturalidade, nacionalidade, estadoCivil, profissao, rg, rgDataExpedicao, cpf, dataNascimento, nomeMae, nomePai, participacaoCapitalSocial, socioAdministrador, proLabore, proLaboreValor, reponsavelReceita, pis, created, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  SociosModel, método  insert_partner ' + str(e) + '\n')

    def select_partner(self, id):
        try:
            self.cur.execute( "SELECT  es.id, es.nome, es.cpf, es.participacaoCapitalSocial, e.id FROM empresas_socios es LEFT JOIN  empresas e ON  e.id = es.id_empresa  WHERE es.id = '{}' AND e.status = 'Ativo' AND es.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  SociosModel, método select_partner: ' + str(e) + '\n')

    def update_status_partner(self, id):
        try:
            self.cur.execute("UPDATE  empresas_socios  SET status = 'Inativo' WHERE empresas_socios.id = {}".format(id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em  SociosModel, método insert_partner ' + str(e) + '\n')
