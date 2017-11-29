import sqlite3
import config
import os
from flask import current_app

class SqliteDB(object):
  """ Class used to query the db within an environment
  !! SHOULD NOT BE USED IN LOCAL OR BY USERS - so the module should always be in the excluded list
  in pacakge
  This module doesn't access the sqlite db that is running at the app level
  """

  def __init__(self, report_name):
    """ """
    self.path = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db')
    self.conn = sqlite3.connect(self.path)
    self.cursor = self.conn.cursor()

  def modify(self, query):
    """ method used for update, insert, delete """
    self.cursor.executescript(query)
    self.conn.commit()

  def select(self, query):
    """ query used for selects - return an iterator """
    result = self.cursor.execute(query)
    header = [col[0] for col in self.cursor.description]
    for res in result:
      newRes = list(res)
      if None in newRes:
        for i, rec in enumerate(newRes):
          if rec is None:
            newRes[i] = ''
      yield dict(zip(header, list(newRes)))

  def close(self):
    """ """
    self.conn.close()

class MainDB(SqliteDB):
  """ """

  def __init__(self):
    self.path = os.path.join(current_app.config['ROOT_PATH'], config.ARES_MAIN_DB_LOCATION)
    self.conn = sqlite3.connect(self.path)
    self.cursor = self.conn.cursor()



