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
    self.__conn = sqlite3.connect(self.path)
    self.__cursor = self.__conn.cursor()

  def modify(self, query):
    """ method used for update, insert, delete """
    self.__cursor.execute(query)
    self.__conn.commit()

  def select(self, query):
    print(query)
    """ query used for selects - return an iterator """
    result = self.__cursor.execute(query)
    header = [col[0] for col in self.__cursor.description]
    for res in result:
      yield dict(zip(header, list(res)))

