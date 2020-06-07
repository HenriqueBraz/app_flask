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
                        "FORMAT(f.faturamento,2,'de_DE'), e.id FROM empresas e  LEFT JOIN faturamentos f ON "
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


    def update_billing_company(self, username, name, email, password, group, id):
        try:
            self.cur.execute("UPDATE usuarios SET  username = '{}', nome = '{}',  email = '{}', passwd = '{}' WHERE id = {}".format(username, name, email, password, id))
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método update_billing_company: ' + str(e) + '\n')


    def update_faturamentos(self, id_empresa, faturamento):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d')
            data1 = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (id_empresa, faturamento, data, data1, data1, 'Ativo')
            sql = "INSERT INTO faturamentos (id_empresa, faturamento, data, created, updated, status) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE faturamento = '{}', updated = '{}';".format(faturamento, data1)
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em   EmpresaModel, método update_faturamentos(: ' + str(e) + '\n')

         # INSERT INTO customers(id, name) VALUES(5, 'André Marcos') ON DUPLICATE KEY UPDATE name = 'André Marcos';
        # FORMAT(c.valor,2,'de_DE')
