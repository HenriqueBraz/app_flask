import logging
import json
from datetime import datetime
import pymysql


class GraficoModel(object):

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
        logging.info('Construtor do GraficoModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_tributacao(self, tributacao1, tributacao2, tributacao3, user_id):
        result = []
        try:
<<<<<<< HEAD
            self.cur.execute(
                "SELECT COUNT(e.id) FROM empresas e  WHERE e.tributacao = '{}' AND e.status = 'Ativo';".format(
                    tributacao1))
            result += self.cur.fetchone()
            self.cur.execute(
                "SELECT COUNT(e.id) FROM empresas e  WHERE e.tributacao = '{}' AND e.status = 'Ativo';".format(
                    tributacao2))
            result += self.cur.fetchone()
            self.cur.execute(
                "SELECT COUNT(e.id) FROM empresas e  WHERE e.tributacao = '{}' AND e.status = 'Ativo';".format(
                    tributacao3))
=======
            self.cur.execute("SELECT COUNT(e.id) FROM empresas e  WHERE e.tributacao = '{}' AND e.id_responsavel = '{}' AND e.status = 'Ativo';".format(tributacao1, user_id))
            result += self.cur.fetchone()
            self.cur.execute("SELECT COUNT(e.id) FROM empresas e  WHERE e.tributacao = '{}' AND e.id_responsavel = '{}' AND e.status = 'Ativo';".format(tributacao2, user_id))
            result += self.cur.fetchone()
            self.cur.execute("SELECT COUNT(e.id) FROM empresas e  WHERE e.tributacao = '{}' AND e.id_responsavel = '{}' AND e.status = 'Ativo';".format(tributacao3, user_id))
>>>>>>> front-end
            result += self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  GraficoModel, método get_pizza: ' + str(e) + '\n')

    def get_ocorrencias(self, user_name):
        result = []
        try:
            self.cur.execute("SELECT COUNT(eo.id_empresa) FROM empresas_ocorrencias eo  WHERE eo.responsavel = '{}' AND eo.status = 'Aberto';".format(user_name))
            result += self.cur.fetchone()
            self.cur.execute("SELECT COUNT(eo.id_empresa) FROM empresas_ocorrencias eo  WHERE eo.responsavel = '{}' AND eo.status = 'Fechado';".format(user_name))
            result += self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  GraficoModel, método get_pizza: ' + str(e) + '\n')

    def get_cobrancas(self, tipo):
        now = datetime.now()
        ano = now.strftime('%Y')
        result = []
        try:
            for i in range(1, 13):
                self.cur.execute(
                    "SELECT COUNT(c.tipo_cobranca ) FROM cobrancas c WHERE  DATE_FORMAT(c.data, '%m') = {} AND DATE_FORMAT(c.created, '%Y') = {} AND c.tipo_cobranca = '{}' ".format(
                        i, ano, tipo))
                result += self.cur.fetchone()

            return result
        except Exception as e:
            logging.error('Erro em  GraficoModel, método get_pizza: ' + str(e) + '\n')
