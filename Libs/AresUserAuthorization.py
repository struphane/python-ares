import datetime
import hashlib
import random
import sqlite3
from flask import current_app
import config
import os
from Libs import AresSecurity


class MainDB(object):
  """ """

  __conn = sqlite3.connect(os.path.join(current_app.config['ROOT_PATH'], config.ARES_MAIN_DB_LOCATION))
  __cursor = conn.cursor()

  @classmethod
  def addUser(cls, email):
    """ """
    __cursor.execute("""SELECT random_nbr FROM main_usr_def WHERE email = '%s'""" % email)
    res = __cursor.fetchall()
    if res:
      return True, AresSecurity.generate_key(email, res[0])

    ADD_USER = """ INSERT INTO main_usr_def (email, random_nbr) VALUES ('%s', '%s');"""
    random.seed(datetime.datetime.now())
    random_number = int(random.random() * 1000)
    c.execute(ADD_USER % (email, random_number))
    __conn.commit()

    # now return the salt from the random number
    return True, AresSecurity.generate_key(email, random_number)

