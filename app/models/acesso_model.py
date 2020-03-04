import logging
import json
from datetime import datetime
import pymysql


class AcessoModel(object):

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
        logging.info('Construtor do AcessoModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def check_accounting(self, id):
        try:
            self.cur.execute(
                "SELECT a.id FROM acessos a WHERE  a.id_empresa = '{}' AND a.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  AcessoModel, método check_accounting(: ' + str(e) + '\n')


    def insert_accounting(self, id, codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS, responsavelReceita):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (id, codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS, responsavelReceita, data, data, 'Ativo')
            sql = "INSERT INTO acessos (id_empresa, codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS, responsavelReceita, created, updated, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  AcessoModel, método insert_accounting(: ' + str(e) + '\n')


    def get_accounting(self, id):
        try:
            self.cur.execute(
                "SELECT * FROM acessos a  WHERE  a.id_empresa = '{}' AND a.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  AcessoModel, método get_accounting(: ' + str(e) + '\n')


    def update_accounting(self, id, codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS, responsavelReceita):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute(
                "UPDATE acessos SET  codigoAcessoSimples = '{}', AcessoECAC = '{}', usernamePF = '{}', "
                "senhaPF = '{}', senhaPrefeitura = '{}', senhaINSS = '{}', responsavelReceita = '{}', updated = '{}' WHERE id_empresa = {}".format(
                    codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS, responsavelReceita, data, id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em AcessoModel,  método update_accounting ' + str(e) + '\n')