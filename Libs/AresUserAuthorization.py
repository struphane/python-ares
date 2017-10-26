import datetime
import hashlib
import random
import sqlite3
import os
from Libs import AresSecurity
from ares.Lib import AresSql


class AuthenticationBase(object):
  """ """

  __db = AresSql.MainDB()

  @classmethod
  def addUser(cls, email):
    """ """
    result = list(cls.__db.select("""SELECT random_nbr FROM main_usr_def WHERE email = '%s'""" % email))
    if result:
      return True, AresSecurity.generate_key(email, result[0]['random_nbr'])

    ADD_USER = """ INSERT INTO main_usr_def (email, random_nbr) VALUES ('%s', '%s');"""
    random.seed(datetime.datetime.now())
    random_number = int(random.random() * 1000)
    cls.__db.modify(ADD_USER % (email, random_number))
    # now return the salt from the random number
    return True, AresSecurity.generate_key(email, random_number)

  @classmethod
  def get_user_base(cls):
    """ """
    USER_BASE = """SELECT email FROM main_usr_def;"""
    return list(cls.__db.select(USER_BASE))


