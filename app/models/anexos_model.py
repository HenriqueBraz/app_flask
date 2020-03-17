import logging
import json
from datetime import datetime
import pymysql


class AnexoModel(object):

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
        logging.info('Construtor do AnexoModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_anexos(self, id):
        try:
            self.cur.execute(
                "SELECT e.id, a.id,  a.filename, a.descricao, a.type, a.created, a.updated, e.empresa  FROM anexos a  LEFT "
                "JOIN  empresas e ON e.id = a.id_empresa  WHERE  1=1 AND "
                "a.id_empresa = '{}' AND  a.status = 'Ativo' AND e.status = 'Ativo';".format(id))
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  AnexosModel, método get_anexos: ' + str(e) + '\n')

    def get_anexo(self, id_anexo):
        try:
            self.cur.execute(
                "SELECT a.path, a.filename FROM anexos a WHERE  a.id = '{}' AND  a.status = 'Ativo';".format(id_anexo))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  AnexosModel, método get_anexo: ' + str(e) + '\n')


    def update_status_anexo(self, id):
        try:
            self.cur.execute("UPDATE  anexos  SET status = 'Inativo' WHERE anexos.id = {}".format(id))
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  AnexosModel, método update_status_anexo: ' + str(e) + '\n')


    def get_company_name(self, id):
        try:
            self.cur.execute("SELECT e.empresa FROM empresas e LEFT JOIN  anexos a  ON e.id = a.id_empresa  WHERE  e.id = '{}' AND e.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_company_name(: ' + str(e) + '\n')


    def insert_anexo(self,id_empresa, path, filename, descricao, size, type, md5) :
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (id_empresa, path, filename, descricao, size, type, md5, data, data)
            sql = "INSERT INTO anexos (id_empresa, path, filename, descricao, size, type, md5, created, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  AnexoModel, método  insert_anexo(: ' + str(e) + '\n')