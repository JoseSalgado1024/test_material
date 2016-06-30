#!/usr/bin/python
# encoding: utf-8

import time
import datetime
import sys
from reserved_words import *
from errHandling import *
import platform
import os


class Log(object):
    def __init__(self,
                 log_file_sufix='',
                 log_file_prefix='',
                 log_file_ext='log',
                 use_date=True,
                 log_file_path='.',
                 log_output=SCREEN_AND_FILE,
                 log_level=FULL_LOG):
        self._file_sufix = log_file_sufix
        self._file_prefix = log_file_prefix
        self._log_file_path = log_file_path
        self._use_date_in_names = use_date
        self._log_output = log_output
        self._log_level = log_level
        self._log_file_ext = log_file_ext

        # Linux cmd Line Palette:
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
        ts = ''
        if self._use_date_in_names:
            t = time.time()
            date_pattern = '%Y-%m-%dT%H_%M_%S'
            ts = datetime.datetime.fromtimestamp(t).strftime(date_pattern)
        self._SESSION_TIME = ts
        if log_output not in [SCREEN_AND_FILE,
                              ONLY_LOG_FILE,
                              ONLY_SCREEN_PRINTS]:
            raise LogsNoOutputMode
        if log_level not in [FULL_LOG,
                             ONLY_ERRORS_AND_WARNINGS,
                             ONLY_ERRRORS]:
            raise LogsNoLevelMode
        os_type = platform.system()
        if log_output in [SCREEN_AND_FILE, ONLY_SCREEN_PRINTS]:
            if os_type != 'windows':
                setattr(Log, '_STR_SCREEN', {
                    INFO: '{date}:\033[92m[INFO]\033[0m {msg}\n',
                    WARNING: '{date}:\033[93m[WARNING]\033[0m {msg}\n',
                    ERROR: '{date}:\033[91m[ERROR]\033[0m {msg}\n',
                    FATAL_ERROR: '{date}:\033[91m[FATAL ERROR]\033[0m {msg}\n'
                })
            else:
                setattr(Log, '_STR_SCREEN', {
                    INFO: '{date}: [INFO] {msg}\n',
                    WARNING: '{date}: [WARNING] {msg}\n',
                    ERROR: '{date}: [ERROR] {msg}\n',
                    FATAL_ERROR: '{date}: [FATAL_ERROR] {msg}\n'
                })
        if log_output in [SCREEN_AND_FILE, ONLY_LOG_FILE]:
            if type(log_output) is None:
                raise LogFilePathFail
            if not os.path.exists(self._log_file_path):
                try:
                    os.makedirs(self._log_file_path)
                except IOError as e:
                    raise IOError

            tmp = '{prefix}logs_{date}{sufix}.{ext}'
            tmp = tmp.format(sufix=self._file_sufix,
                             prefix=self._file_prefix,
                             date=self._SESSION_TIME,
                             ext=self._log_file_ext)
            temp_filename = os.path.join(self._log_file_path, tmp)
            with open(temp_filename, 'w') as lf:
                lf.write('Logs File: {d}\n'.format(d=self._SESSION_TIME))
                lf.close()
            setattr(Log, '_log_file', temp_filename)
            setattr(Log, '_log_file_name', temp_filename)
            setattr(Log, '_STR_FILE', {
                INFO: '{date}: [INFO] {msg}\n',
                WARNING: '{date}: [WARNING] {msg}\n',
                ERROR: '{date}: [ERROR] {msg}\n',
                FATAL_ERROR: '{date}: [FATAL_ERROR] {msg}\n'
            })

    def _print_log_in_file(self, msg, date, type_error=INFO):
        try:
            with open(self._log_file, 'a') as f:
                f.write(
                    self._STR_FILE[type_error].format(date=date,
                                                      msg=msg))
                f.close()
        except Exception:
            return False

    def _print_log_in_screen(self, msg, date, type_error=INFO):
        try:
            sys.stdout.write(
                self._STR_SCREEN[type_error].format(date=date,
                                                    msg=msg))
            return True
        except Exception:
            return False

    def add(self, msg, error_type=INFO):
        n = time.time()
        d_pattern = '%Y-%m-%dT%H:%M:%S-03:00'
        now = datetime.datetime.fromtimestamp(n).strftime(d_pattern)
        if self._log_level == ONLY_LOG_FILE:
            if error_type >= self._log_level:
                writefile = self._print_log_in_screen(msg, now, error_type)
                return writefile
        elif self._log_level == ONLY_SCREEN_PRINTS:
            if error_type >= self._log_level:
                screen = self._print_log_in_file(msg, now, error_type)
                return screen
        else:
            if error_type >= self._log_level:
                screen = self._print_log_in_file(msg, now, error_type)
                writefile = self._print_log_in_screen(msg, now, error_type)
                if screen and writefile:
                    return True
                else:
                    return False
