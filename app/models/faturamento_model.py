import logging
import json
from datetime import datetime
import pymysql


class FaturamentoModel(object):

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
        logging.info('Construtor do FaturamentoModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_companies(self, letra, user_id, tipo):
        letra = letra + '%'
        if tipo == 'sn':
            tipo = 'SIMPLES NACIONAL'
        elif tipo == 'lp':
            tipo = 'PRESUMIDO'
        else:
            tipo = 'REAL'
        try:
            self.cur.execute("SELECT f.id, DATE_FORMAT(f.data, '%m/%Y'), e.empresa, e.cnpj, e.ccm, a.senhaprefeitura,"
                        "FORMAT(f.faturamento,2,'de_DE') FROM empresas e  LEFT JOIN faturamentos f ON "
                        "f.id_empresa=e.id LEFT JOIN acessos a  ON a.id_empresa = e.id  WHERE "
                        "e.id_responsavel = '{}' AND e.tributacao = '{}' AND e.status = 'Ativo'"
                        "AND e.empresa LIKE '{}';".format(user_id, tipo, letra))
            result = self.cur.fetchall()
            return result
        except Exception as e:
                logging.error('Erro em  EmpresaModel, método get_companies: ' + str(e) + '\n')



    def get_companies_sn(self):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa  FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE  "
                "e.tributacao = 'SIMPLES NACIONAL' AND  e.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_companies_sn: ' + str(e) + '\n')

    def get_companies_lp(self):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa  FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE  "
                "e.tributacao = 'PRESUMIDO' AND  e.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_companies_lp: ' + str(e) + '\n')


    def get_companies_r(self):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa  FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE  "
                "e.tributacao = 'REAL' AND  e.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_companies_r: ' + str(e) + '\n')