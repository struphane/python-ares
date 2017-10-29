import datetime
import hashlib
import random
import sqlite3
import os
from Libs import AresSecurity
from ares.Lib import AresSql
import mailer

mailer._DEBUG = False
mail_server = mailer.SMTPServer('smtp.gmail.com', 587)
mail_server.connect(user='ares.pymailer@gmail.com', password='H3reCom3sAReS')
mail_subject = 'Welcom To AReS - Your account has been created !'
mail_content = """Hello,
Your account has been created and you can now logon to AReS using simply your email address and the following token:
%s.
Enjoy !
AReS Team"""


class AuthenticationBase(object):
  """ """

  __db = AresSql.MainDB()

  @classmethod
  def addUser(cls, email_addr):
    """ """
    if cls.user_exists(email_addr):
      return True, AresSecurity.generate_key(email_addr, result[0]['random_nbr'])

    ADD_USER = """ INSERT INTO main_usr_def (email, random_nbr) VALUES ('%s', '%s');"""
    random.seed(datetime.datetime.now())
    random_number = int(random.random() * 1000)
    cls.__db.modify(ADD_USER % (email_addr, random_number))
    # now return the salt from the random number
    token = AresSecurity.generate_key(email_addr, random_number)
    email = mailer.Email('ares.pymailer@gmail.com', [email_addr], mail_subject, mail_content % token)
    mail_server.sendmail(email)
    return True, token

  @classmethod
  def get_user_base(cls):
    """ """
    USER_BASE = """SELECT email FROM main_usr_def;"""
    return list(cls.__db.select(USER_BASE))

  @classmethod
  def user_exists(cls, email_addr):
    """ """
    result = list(cls.__db.select("""SELECT random_nbr FROM main_usr_def WHERE email = '%s'""" % email_addr))
    if result:
      return True

    return False


