import logging
import json
from datetime import datetime
import pymysql


class ContabilidadeModel(object):

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
        logging.info('Construtor do ContabilidadeModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_accounting(self, id):
        try:
            self.cur.execute(
                "SELECT * FROM empresas_contabilidade_anterior eca  WHERE  eca.id_empresa = '{}' AND eca.status = 'Ativo';".format(
                    id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  ContabilidadeModel, método get_accounting(: ' + str(e) + '\n')

    def insert_accounting(self, id, contabilidade, nome, telefone, email, dataEntrada):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (id, contabilidade, nome, telefone, email, dataEntrada, data, data, 'Ativo')
            sql = "INSERT INTO empresas_contabilidade_anterior (id_empresa, contabilidade, nome, telefone, email, " \
                  "dataEntrada, created, updated, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  ContabilidadeModel, método insert_accounting(: ' + str(e) + '\n')

    def update_accounting(self, id, contabilidade, nome, telefone, email, dataEntrada):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute(
                "UPDATE empresas_contabilidade_anterior SET  contabilidade = '{}', nome = '{}', telefone = '{}', "
                "email = '{}', dataEntrada = '{}', updated = '{}' WHERE id = {}".format(
                    contabilidade, nome, telefone, email, dataEntrada, data, id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em ContabilidadeModel,  método update_accounting ' + str(e) + '\n')


    def update_status_accounting(self, id):
        try:
            self.cur.execute("UPDATE empresas_contabilidade_anterior SET status = 'Inativo' WHERE id = {}".format(id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em ContabilidadeModel, método update_status_accounting' + str(e) + '\n')