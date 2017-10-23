import sqlite3
from flask import current_app
import config
import time
import os

MAIN_TABLE = """ CREATE TABLE
IF NOT EXISTS main_usr_def (
email text NOT NULL UNIQUE,
random_nbr integer NOT NULL
);
"""

def launch_db(app_path):
  """ """
  conn = sqlite3.connect(os.path.join(app_path, config.ARES_MAIN_DB_LOCATION))
  c = conn.cursor()
  c.execute(MAIN_TABLE)
  conn.commit()
  conn.close()
