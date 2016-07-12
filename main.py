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
import os
from os.path import *
from libs.configs import *
from subprocess import call, Popen
import re
"""

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

    def run_query(self, query, del_up=False):
        if not self.db_is_connected:
            logs.add('DB, no conectada, conectando...')
            logs.add(
                'Conenctado!' if self.create_db_conn() else 'Fallo!'
                )
        q = self.db_conn.cursor()
        q.execute(query)
        response = []
        if del_up:
            if 'DELETE' in q.statusmessage or 'UPDATE' in q.statusmessage:
                return True
            else:
                return False

        else:
            try:
                res = q.fetchall()
            except Exception:
                return False
        column_names = [row[0] for row in q.description]
        response.append(column_names)
        for row in res:
            response.append(row)
        return response


def run_my_etl(command):
    os.environ['PGPASSWORD'] = my_conf.db_pass
    os.environ['PGUSER'] = my_conf.db_user
    p = Popen(command.split())


class TestZip(object):
    def __init__(self, com_id, mail, db_instance, conf):
        self.com_id = com_id
        self.mail = mail
        self.db_instance = db_instance
        self.conf = conf

    def _exists_user(self, db_instance=None):
        db = self.db_instance if None in [db_instance] else db_instance
        q = self.conf.exists_user.format(cid=self.com_id)
        c = db.run_query(q)
        if not c:
            logs.add('Fallo query \"{q}\"'.format(q=q), ERROR)
            return False
        return c[1][0] == 1

    def _change_mail(self, mail):
        logs.add(
            'Cambiando e-mail de respuesta por: {mail}'.format(
                mail=mail['new_mail']))
        try:
            q = my_conf.set_response_mail.format(new_mail=mail['new_mail'],
                                                 cid=self.com_id)
            if not db.run_query(q, del_up=True):
                return False
            logs.add('Hecho!')
            return True
        except Exception, e:
            logs.add(
                'Fallo la actualizacion del e-mail'.format(m=mail), ERROR)
            return False

    def _prepare_test(self, db_instance=None):
        if not self._exists_user():
            logs.add('No existe el usuario con id=\"{cid}\"'.format(
                cid=self.com_id), FATAL_ERROR)
            return False
        if self.mail['enable'] and not self._change_mail(self.mail):
            return False
        return True

    def _set_active_user(self, db_instance=None):
        db = self.db_instance if None in [db_instance] else db_instance
        d = db.run_query(self.conf.set_active_user.format(cid=self.com_id),
                         del_up=True)
        a = db.run_query(self.conf.set_inactive_user.format(cid=self.com_id),
                         del_up=True)
        if False in [d, a]:
            return False
        return True

    def _run_etl(self):
        command = self.conf.run_etl.format(etl_run=1)
        logs.add('Lanzando preciosETL, comando: \"{cmd}\"'.format(cmd=command))
        try:
            run_my_etl(command)
        except Exception, e:
            print e
            return False
        return True

    def run_test(self):
        if self._prepare_test():
            logs.add('Test Inicializado correctamente')
            if self._set_active_user():
                logs.add('Comercio \"{cid}\" activado correctamente'.format(
                    cid=self.com_id))
                if self._run_etl():
                    return True
                else:
                    logs.add('Fallo lanzamiento de preciosETL', FATAL_ERROR)
                    raise Exception
            else:
                logs.add('Fallo la activacion del Comercio \"{cid}\"'.format(
                    cid=self.com_id), FATAL_ERROR)
                raise Exception
        else:
            raise Exception


def main():
    if COMMAND in COMMANDS:
        if COMMAND == COMMANDS[TEST_ZIP]:
            logs.add('Corriendo test. \"test.zip\"')
            try:
                logs.add('Inicializando DB..')
                db_instance = SepaSB(db_user=my_conf.db_user,
                                     db_pass=my_conf.db_pass,
                                     db_host=my_conf.db_host,
                                     db_name=my_conf.db_name)
                logs.add('Lanzando Test..')
                test = TestZip(COMERCIO_ID,
                               USE_OTHER_MAIL,
                               db_instance,
                               my_conf)
                if test.run_test():
                    logs.add('Test finalizado correctamente!')
                else:
                    logs.add('Fallo Test', ERROR)
                    exit(1)
            except Exception, e:
                logs.add('Fallo Test. Error:{e}'.format(e=e), ERROR)
                exit(1)
        else:
            logs.add('Funcion \"{f}\" no implementada aun.'.format(f=COMMAND),
                     FATAL_ERROR)
            exit(1)
    else:
        log.add('Comando no válido!', ERROR)

if __name__ == '__main__':
    main()
