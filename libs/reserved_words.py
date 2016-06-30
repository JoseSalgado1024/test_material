#!/usr/bin/python
# encoding: utf-8

# ERROR TYPES
INFO = 0
WARNING = 2
ERROR = 3
FATAL_ERROR = 4

# PRINT LOGS LEVEL
FULL_LOG = 0
ONLY_ERRORS_AND_WARNINGS = 1
ONLY_ERRRORS = 2

# ERRORS OUTPUT
SCREEN_AND_FILE = 0
ONLY_LOG_FILE = 1
ONLY_SCREEN_PRINTS = 2


# TABLE NAMES
COMERCIO_ID = 0
FILENAME = 1
FULL_PATH_FILE = 2
DATE = 3
TIMESTAMP = 4
ETL_RUN = 5

# POSIBLE COMMANDS
TEST_ZIP = 0
COMMANDS = ['TEST_ZIP', ]

INIT_MGS = '\n'\
           '###############################################\n'\
           '#                                             #\n'\
           '#                TEST \"test.zip\"              #\n'\
           '#                  BOOTING...                 #\n'\
           '#                                             #\n'\
           '###############################################\n'
