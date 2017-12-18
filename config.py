""" Global Configuration for Ares

"""

import os
import logging

ARES_FOLDER = 'ares'
ARES_USERS_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_reports')
#USERS_ENV_LOCATION = os.path.dirname(os.path.abspath(__file__)'E:\GitHub\Ares\user_reports'
ARES_USERS_DELETED_FOLDERS = 'user_deleted_reports'
ARES_SQLITE_FILES_LOCATION = 'static/sql_config'
ARES_MODE = 'local'
WORK_PATH = os.path.join('E:/', 'GitHub', 'scripts')

COMPANY = "your company"

LOG_LEVEL = logging.INFO
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=LOG_LEVEL)

