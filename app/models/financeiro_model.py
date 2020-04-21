import logging
import json
from datetime import datetime
import pymysql


class FinanceiroModel(object):

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
        logging.info('Construtor do FinanceiroModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def get_companies(self, user_id):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa, e.cnpj FROM empresas e LEFT JOIN  usuarios u  ON u.id = e.id_responsavel  WHERE u.id = '{}' AND e.status = 'Ativo';".format(user_id))
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  FinanceiroModel, método get_companies: ' + str(e) + '\n')

    def get_levying(self, id_cobranca):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa, DATE_FORMAT(c.data, '%d/%m/%Y'), c.servico, c.valor, c.tipo_cobranca, c.id FROM empresas e LEFT JOIN  cobrancas c  ON e.id = "
                "c.id_empresa  WHERE c.id = '{}' AND c.status='Ativo' AND e.status = 'Ativo';".format(id_cobranca))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  FinanceiroModel, método get_levyings_sum: ' + str(e) + '\n')


    def get_levyings(self, id, mes):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa, DATE_FORMAT(c.data, '%d/%m/%Y'), c.servico, c.valor, c.id  FROM empresas e LEFT JOIN  cobrancas c  ON e.id = "
                "c.id_empresa  WHERE MONTH(data) = '{}' AND e.id = '{}' AND c.status='Ativo' AND e.status = 'Ativo';".format(mes, id))
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  FinanceiroModel, método get_levyings_sum: ' + str(e) + '\n')


    def get_levyings_sum(self, id, mes):
        try:
            self.cur.execute("SELECT SUM(c.valor)  FROM  empresas e LEFT JOIN  cobrancas c ON e.id = "
                             "c.id_empresa WHERE MONTH(data) = '{}'  AND  e.id = '{}' AND c.status='Ativo' AND e.status = 'Ativo';".format(mes, id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  FinanceiroModel, método get_levyings_sum: ' + str(e) + '\n')


    def insert_finantal_levying(self, id, data, servico, valor, tipo_cobranca):
        try:
            now = datetime.now()
            data1 = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (id, data, servico, valor, tipo_cobranca, data1, data1, 'Ativo')
            sql = "INSERT INTO cobrancas (id_empresa, data, servico, valor, tipo_cobranca, created, updated, " \
                  "status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s); "
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  FinanceiroModel, método insert_finantal_levy(: ' + str(e) + '\n')

    def update_finantal_levying(self, data, servico, valor, tipo_cobranca, id_cobranca):
        try:
            now = datetime.now()
            data1 = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute(
                "UPDATE cobrancas SET  data = '{}', servico = '{}', valor = '{}', tipo_cobranca = '{}', updated = '{}' WHERE id = '{}'".format(data, servico, valor, tipo_cobranca, data1, id_cobranca))
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  FinanceiroModel, método  update_finantal_levying: ' + str(e) + '\n')

    def update_status_levying(self, id_cobranca):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute("UPDATE cobrancas SET  status = '{}', updated = '{}' WHERE id = '{}'".format(
                    'Inativo', data, id_cobranca))
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  FinanceiroModel, método  update_finantal_levying: ' + str(e) + '\n')