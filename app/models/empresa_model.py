import logging
import json
from datetime import datetime
import pymysql


class EmpresaModel(object):

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
        logging.info('Construtor do EmpresaModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def insert_empresa(self, id_natureza_juridica, id_porte_empresa, id_responsavel, dataResponsavel, empresa, endereco,
                       bairro, cidade, estado, capitalSocial, nire, cnpj, ie, ccm, cnaePrincipal, cnaeSecundaria,
                       tributacao, diaFaturamento, folhaPagamento, certificadoDigital, observacoes, created, updated,
                       status):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (
                id_natureza_juridica, id_porte_empresa, id_responsavel, dataResponsavel, empresa, endereco, bairro,
                cidade, estado, capitalSocial, nire, cnpj, ie, ccm, cnaePrincipal, cnaeSecundaria, tributacao, diaFaturamento,
                folhaPagamento, certificadoDigital, observacoes, data, data, 'Ativo')
            sql = "INSERT INTO empresas ( id_natureza_juridica, id_porte_empresa, id_responsavel, dataResponsavel, " \
                  "empresa, endereco, bairro, cidade, estado, capitalSocial, nire, cnpj, ie, ccm, cnaePrincipal, " \
                  "cnaeSecundaria,tributacao, diaFaturamento, folhaPagamento, certificadoDigital, observacoes, " \
                  "created, updated,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return logging.info('empresa cadastrada com sucesso')

        except Exception as e:
            logging.error('Erro em EmpresaModel, método insert_user: ' + str(e) + '\n')
