import logging
import json
from datetime import datetime
import pymysql


class OcorrenciaModel(object):

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
        logging.info('Construtor do OcorrenciaModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_companies(self):
        try:
            self.cur.execute("SELECT e.id, e.empresa, e.created, u.nome, e.cnpj, e.ccm, e.endereco, e.bairro, e.cidade, e.estado FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE e.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_companies: ' + str(e) + '\n')