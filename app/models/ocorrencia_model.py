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

    def get_occurrences_sn(self, user_id):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa, e.cnpj, e.ccm, DATE_FORMAT(eo.updated, '%d/%m/%Y  %H:%m'), u.nome, eo.status, eo.id FROM usuarios u INNER JOIN empresas e ON u.id=e.id_responsavel  INNER JOIN empresas_ocorrencias eo WHERE e.id=eo.id_empresa AND e.tributacao = 'SIMPLES NACIONAL' AND eo.responsavel = {}  AND e.status='Ativo';".format(user_id))
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  OcorrenciaModel, método get_occurrences_sn: ' + str(e) + '\n')

    def get_occurrences_lp(self, user_id):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa, e.cnpj, e.ccm, DATE_FORMAT(eo.updated, '%d/%m/%Y  %H:%m'), u.nome, eo.status, eo.id FROM usuarios u INNER JOIN empresas e ON u.id=e.id_responsavel  INNER JOIN empresas_ocorrencias eo WHERE e.id=eo.id_empresa AND e.tributacao = 'PRESUMIDO' AND eo.responsavel = {}  AND e.status='Ativo';".format(user_id))
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  OcorrenciaModel, método get_occurrences_lp: ' + str(e) + '\n')

    def get_occurrences_r(self, user_id):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa, e.cnpj, e.ccm, DATE_FORMAT(eo.updated, '%d/%m/%Y  %H:%m'), u.nome, eo.status, eo.id FROM usuarios u INNER JOIN empresas e ON u.id=e.id_responsavel  INNER JOIN empresas_ocorrencias eo WHERE e.id=eo.id_empresa AND e.tributacao = 'REAL' AND eo.responsavel = {}  AND e.status='Ativo';".format(user_id))
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em  OcorrenciaModel, método get_occurrences_r: ' + str(e) + '\n')

    def insert_occurrence(self, id_cliente, responsavel, observacoes):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (id_cliente, responsavel, observacoes, data, data, 'Aberto')
            sql = "INSERT INTO empresas_ocorrencias (id_empresa, responsavel, descritivo, created, updated, " \
                  "status) VALUES (%s, %s, %s, %s, %s, %s); "
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return True
        except Exception as e:
            logging.error('Erro em  OcorrenciaModel, método insert_ocorrencia(: ' + str(e) + '\n')

    def get_occurrence(self, id_ocorrencia):
        try:
            self.cur.execute(
                "SELECT e.id, e.empresa, e.cnpj, e.ccm, DATE_FORMAT(eo.updated, '%d/%m/%Y  %H:%m'), eo.responsavel, eo.descritivo, eo.id FROM empresas e "
                "INNER JOIN empresas_ocorrencias eo WHERE e.id=eo.id_empresa AND eo.id = '{}';".format(id_ocorrencia))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  EmpresaModel, método get_occurrence: ' + str(e) + '\n')

    def get_occurrence_edit(self, id_ocorrencia):
        try:
            self.cur.execute(
                "SELECT eo.id_empresa, eo.responsavel, eo.descritivo, e.empresa, eo.id, eo.status  FROM empresas e INNER JOIN empresas_ocorrencias "
                "eo WHERE eo.id = '{}' AND eo.id_empresa=e.id;".format(id_ocorrencia))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em  OcorrenciaModel, método get_occurrence: ' + str(e) + '\n')

    def update_occurrence(self, id_cliente, responsavel, observacoes, id_ocorrencia, status):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute(
                "UPDATE empresas_ocorrencias SET id_empresa = '{}', responsavel = '{}', descritivo = '{}', updated = '{}', status = '{}' WHERE empresas_ocorrencias.id = {}".format(
                    id_cliente, responsavel, observacoes,  data, status, id_ocorrencia))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em OcorrenciaModel,  método update_occurrence' + str(e) + '\n')


    def update_status_partner(self, id):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute("UPDATE  empresas_ocorrencias  SET status = 'Fechado', updated = '{}'  WHERE empresas_ocorrencias.id = {}".format(data, id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em  SociosModel, método insert_partner ' + str(e) + '\n')



