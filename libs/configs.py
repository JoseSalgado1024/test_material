#!/usr/bin/python
# encoding: utf-8

import os
import ConfigParser
from screen_prints import *
from logme import *
from errHandling import *
from reserved_words import *

import argparse


def get_args():
    """TODO."""
    parser = argparse.ArgumentParser(
        description='#####| TEST test.zip help |#####')

    parser.add_argument('-id',
                        '--id',
                        type=str,
                        help='ID del comercio a chequear',
                        required=True)

    parser.add_argument('-m',
                        '--mail',
                        type=str,
                        help='e-mail para envio de resultados del test.',
                        required=False)

    parser.add_argument('-c',
                        '--cmd',
                        type=str,
                        help='Tipo de test.',
                        required=False)

    parser.add_argument('-C',
                        '--conf',
                        type=str,
                        help='Archivo de configuracion externa.',
                        required=False)

    parser.add_argument('--log',
                        dest='log',
                        action='store_true',
                        help='Activar el uso de logs.')
    parser.add_argument('--no-log',
                        dest='log',
                        action='store_false',
                        help='Desactivar el uso de logs.')
    parser.set_defaults(log=False)
    args = parser.parse_args()
    mail = args.mail
    uid = args.id
    config = args.conf
    command = args.cmd
    log = args.log
    return mail, uid, config, log, command


USE_OTHER_MAIL = {'enable': False,
                  'new_mail': None}

COMMAND_TO_RUN = COMMANDS[TEST_ZIP]

RES_MAIL, COMERCIO_ID, CONFIG_FILE, USE_LOGS, COMMAND = get_args()
print INIT_MGS
print 'Chequeando \"mail\"...'
if None not in [RES_MAIL]:
    USE_OTHER_MAIL = {'enable': True,
                      'new_mail': RES_MAIL}
print 'Chequeando \"comando activo\"...'
if None in [COMMAND]:
    COMMAND = COMMANDS[TEST_ZIP]
else:
    if COMMAND not in COMMANDS:
        exit(1)
print 'chaqueando \"config.file\"...'
if None in [CONFIG_FILE]:
    CONFIG_FILE = '.app.cfg'
log_level = FULL_LOG
print 'chaqueando \"logs\"...'
if not USE_LOGS:
    log_level = ONLY_ERRRORS


CONFIG_FILE = os.path.join(os.path.dirname(__file__), CONFIG_FILE)

my_conf = None
logs = None


class MyConf(object):
    def __init__(self,
                 filename=None,
                 logs_inst=None,
                 extra_values=None):
        if None not in [extra_values] and type(extra_values) is dict:
            for key, value in extra_values:
                setattr(MyConf, key, value)
        self.logs = logs_inst
        self._CFG_FILE = filename
        self._Config = ConfigParser.ConfigParser()

    def _load_file(self):
        self.logs.add(mensages.LOADING_CONF.format(f=self._CFG_FILE), INFO)
        try:
            self._Config.read(self._CFG_FILE)
            self.logs.add(mensages.FILE_LOAD_OK.format(f=self._CFG_FILE), INFO)
        except IOError:
            m = mensages.CONF_FILE_LOAD_FAIL
            self.logs.add(m.format(f=self._CFG_FILE), ERROR)
            raise IOError

    def _configSectionMap(self, section):
        dict1 = {}
        options = self._Config.options(section)
        for option in options:
            try:
                dict1[option] = self._Config.get(section, option)
                if dict1[option] == -1:
                    self.logs.add("skip: {opt}".format(opt=option), INFO)
            except:
                self.logs.add("exception on {opt}!".format(opt=option), ERROR)
                dict1[option] = None
        return dict1

    def loadConfFile(self):
        try:
            self._load_file()
        except IOError:
            raise IOError
        except Exception:
            raise UnknowError
        try:
            sections = self._Config.sections()
            for section in sections:
                self.logs.add('loading conf for {sec}'.format(sec=section),
                              INFO)
                options = self._Config.options(section)
                if len(options) == 0 or type(options) is None:
                    raise ConfigEmptySeccion
                for option in options:
                    self.logs.add('Conf property: {property}'
                                  ''.format(property=option), INFO)
                    setattr(MyConf,
                            option,
                            self._configSectionMap(section)[option.lower()])
        except AttributeError:
            raise ConfigSectionsError
        except Exception:
            raise UnknowError

try:
    logs = Log(log_level=log_level)
    logs.add('App iniciada...')
except Exception as e:
    print 'Fallo el inicio de logs...'
    exit(1)

try:
    my_conf = MyConf(CONFIG_FILE, logs)
    my_conf.loadConfFile()
    logs.add('Configuracion cargada correctamente...')
except Exception:
    logs.add('Oops!', ERROR)
    exit(1)
