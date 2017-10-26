import sqlite3
from flask import current_app
import config
import time
import os
from Libs import AresUserAuthorization

MAIN_TABLE = """ CREATE TABLE
IF NOT EXISTS main_usr_def (
email text NOT NULL UNIQUE,
random_nbr integer NOT NULL
);
"""

def launch_db(app_path):
  """ """
  main_db = AresSql.MainDB()
  main_db.modify(MAIN_TABLE)
  main_db.close()




