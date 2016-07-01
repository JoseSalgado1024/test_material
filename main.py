#!/usr/bin/python
# encoding: utf-8
"""

        .-.
       /_ _\
       |o^o|
       \ _ /
      .-'-'-.
    /`)  .  (`\
   / /|.-'-.|\ \
   \ \| (_) |/ /  .-""-.
    \_\'-.-'/_/  /[] _ _\
    /_/ \_/ \_\ _|_o_LII|_
      |'._.'|  / | ==== | \
      |  |  |  |_| ==== |_|
       \_|_/    ||" ||  ||
       |-|-|    ||LI  o ||
   joe |_|_|    ||'----'||
      /_/ \_\  /__|    |__\
"""
import psycopg2
from libs import configs
from os.path import *
from libs.configs import *
import re
"""
SEPA_HOST=test-sepa-api-dev.c2setm4u4yff.us-east-1.rds.amazonaws.com
SEPA_DATABASE=test_sepa_etl_dev
SEPA_PORT=5432
SEPA_USER=gobiernoabierto
SEPA_PASS=Encrypted 2be98afc86aa7958ba918ac79db80bbd5
"""
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


class SepaSB(object):
    def __init__(self,
                 db_user=None,
                 db_pass=None,
                 db_host=None,
                 db_name=None,
                 query=None):
        if None in [db_user, db_pass, db_host, db_name]:
            logs.add('Fallo! los parametros provistos no son correctos',
                     ERROR)
            exit(1)
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_name = db_name
        self.db_conn = None
        self.db_is_connected = False

    def create_db_conn(self):
        try:
            self.db_conn = psycopg2.connect(database=self.db_name,
                                            user=self.db_user,
                                            password=self.db_pass,
                                            host=self.db_host)
            self.db_is_connected = True
            return self.db_is_connected
        except Exception:
            return False

    def run_query(self, query):
        if not self.db_is_connected:
            logs.add('DB, no conectada, conectando...')
            logs.add(
                'Conenctado!' if self.create_db_conn() else 'Fallo!'
                )
        q = self.db_conn.cursor()
        q.execute(query)
        response = []
        res = q.fetchall()
        column_names = [row[0] for row in q.description]
        response.append(column_names)
        for row in res:
            response.append(row)
        return response


class TestZip(object):
    def __init__(self, com_id, mail, db_instance, conf):
        self.com_id = com_id
        self.mail = mail
        self.db_instance = db_instance
        self.conf = conf

    def _exists_user(self, db_instance=None):
        db = self.db_instance if None in [db_instance] else db_instance
        c = db.run_query(
            self.conf.exists_user.format(cid=self.com_id))[1]
        return str(c[0]) == '(1L,)'

    def _change_mail(self, mail):
        logs.add(
            'Cambiando e-mail de respuesta por: {mail}'.format(
                mail=mail['new_mail']))
        try:
            q = my_conf.set_response_mail.format(new_mail=mail['new_mail'],
                                                 cid=self.com_id)
            db.run_query(q)
            logs.add('Hecho!')
            return True
        except Exception, e:
            logs.add(
                'Fallo la actualizacion del e-mail'.format(m=mail), ERROR)
            return False

    def _prepare_test(self, db_instance=None):
        if not self._exists_user():
            return False
        if self.mail['enable'] and not self._change_mail(self.mail):
            return False

    def run_test(self):
        self._prepare_test()


def main():
    if COMMAND in COMMANDS:
        if COMMAND == COMMANDS[TEST_ZIP]:
            try:
                logs.add('Corriendo test. \"test.zip\"')
                db_instance = SepaSB(db_user=my_conf.db_user,
                                     db_pass=my_conf.db_pass,
                                     db_host=my_conf.db_host,
                                     db_name=my_conf.db_name)
                test = TestZip(COMERCIO_ID,
                               USE_OTHER_MAIL,
                               db_instance,
                               my_conf)
                test.run_test()
                logs.add('Test finalizado correctamente!')
            except Exception, e:
                logs.add('Fallo Test. Error:{e}'.format(e=e), ERROR)
                exit(1)
        else:
            logs.add('Funcion \"{f}\" no implementada aun.'.format(f=COMMAND),
                     FATAL_ERROR)
    else:
        log.add('Comando no válido!', ERROR)

if __name__ == '__main__':
    main()
