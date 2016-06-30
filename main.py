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
                 query=None,
                 db_port=None):
        if None in [db_user, db_pass, db_host, db_name, query, db_port]:
            logs.add('Fallo!', ERROR)
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.report_format = report_format
        self.query_set = query_set
        self.db_conn = None
        self.db_is_connected = False

    def create_db_conn(self):
        try:
            self.db_conn = psycopg2.connect(database=self.db_name,
                                            user=self.db_user,
                                            password=self.db_pass,
                                            host=self.db_host,
                                            port=self.db_port)
            self.db_is_connected = True
            return self.db_is_connected
        except Exception:
            return False

    def _run_query(self, query):
        q = self.db_conn.cursor()
        q.execute(query)
        response = []
        res = q.fetchall()
        column_names = [row[0] for row in q.description]
        response.append(column_names)
        for row in res:
            response.append(row)
        return response


def main():
    if COMMAND in COMMANDS:
        if COMAND == COMMANDS[TEST_ZIP]:
            sepa_db = SepaSB(db_user=my_conf.db_user,
                             db_pass=my_conf.db_port,
                             db_host=my_conf.db_port,
                             db_name=my_conf.db_port,
                             query=None,
                             db_port=my_conf.db_port)
    else:
        log.add('Comando no válido!', ERROR)

if __name__ == '__main__':
    main()
