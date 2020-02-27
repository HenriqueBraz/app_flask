import logging
import json
from datetime import datetime
import pymysql


class UsuarioModel(object):

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
        logging.info('Construtor do UsuarioModel chamado com sucesso\n')
        logging.disable(logging.DEBUG)

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_users(self):
        try:
            self.cur.execute("SELECT u.id, u.username, u.nome,u.email, u.created, u.updated, g.grupo FROM usuarios u LEFT JOIN grupos g ON u.id = g.id_usuario WHERE u.status = 'Ativo';")
            result = self.cur.fetchall()
            return result
        except Exception as e:
            logging.error('Erro em Usuario_Model, método get_users: ' + str(e) + '\n')

    def get_user(self, id):
        try:
            self.cur.execute("SELECT u.id, u.username, u.nome,u.email, u.created, u.updated, g.grupo FROM usuarios u LEFT JOIN grupos g ON u.id = g.id_usuario  WHERE u.id = '{}' and u.status = 'Ativo';".format(id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em Usuario_Model, método get_user: ' + str(e) + '\n')

    def find_username(self, username):
        try:
            self.cur.execute("SELECT id FROM usuarios WHERE username = '{}';".format(username))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em Usuario_Model, método find_username: ' + str(e) + '\n')

    def find_all_username(self, username):
        try:
            self.cur.execute("SELECT u.*, g.grupo FROM usuarios u LEFT JOIN grupos g ON u.id = g.id_usuario  WHERE u.username = '{}';".format(username))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em Usuario_Model, método find_all_username: ' + str(e) + '\n')

    def find_one_id(self, user_id):
        try:
            self.cur.execute(
                "SELECT u.username, u.nome, u.email, u.passwd,  g.grupo FROM usuarios u LEFT JOIN grupos g ON u.id = g.id_usuario  WHERE  u.id = '{}';".format(user_id))
            result = self.cur.fetchone()
            return result
        except Exception as e:
            logging.error('Erro em Usuario_Model, método find_one_id: ' + str(e) + '\n')

    def insert_user(self, username, password, name, email):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            sql_data = (username, password, name, email, 'Não', data, data, 'Ativo')
            sql = "INSERT INTO usuarios (username, passwd , nome, email, developer, created, updated, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            self.cur.execute("SELECT id FROM usuarios WHERE username = '{}';".format(username))
            id_usuario = self.cur.fetchone()
            sql_data = (id_usuario, 'Usuario')
            sql = "INSERT INTO grupos (id_usuario, grupo) VALUES ( %s, %s )"
            self.cur.execute(sql, sql_data)
            self.con.commit()
            return logging.info('usuário cadastrado com sucesso')

        except Exception as e:
            logging.error('Erro em Usuario_Model, método insert_user: ' + str(e) + '\n')

    def update_user(self, username, name, email, password, group, id):
        try:
            now = datetime.now()
            data = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute("UPDATE usuarios SET  username = '{}', nome = '{}',  email = '{}', passwd = '{}' WHERE id = {}".format(username, name, email, password, id))
            self.con.commit()
            self.cur.execute("UPDATE grupos SET  grupo = '{}'  WHERE id_usuario = {}".format(group, id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em UsuarioModel, método update_user ' + str(e) + '\n')

    def update_status_user(self, id):
        try:
            self.cur.execute("UPDATE usuarios SET status = 'Inativo' WHERE id = {}".format(id))
            self.con.commit()
            return True

        except Exception as e:
            logging.error('Erro em UsuarioModel, método update_status_user ' + str(e) + '\n')
