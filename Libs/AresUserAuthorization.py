
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
# import mailer

# mailer._DEBUG = False
# mail_server = mailer.SMTPServer('smtp.gmail.com', 587)
# mail_server.connect(user='ares.pymailer@gmail.com', password='H3reCom3sAReS')
# mail_subject = 'Welcom To AReS - Your account has been created !'
# mail_content = """Hello,
# Your account has been created and you can now logon to AReS using simply your email address and the following token:
# %s.
# Enjoy !
# AReS Team"""

SALT = '3L!SeFr3D4!'
def encrypt_old(pwd, key):
  """ """
  iv = os.urandom(16)
  cipher = cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
  encryptor = cipher.encryptor()
  cipher_text = encryptor.update(bytes(pwd.encode('utf-8'))) + encryptor.finalize()
  return cipher_text, iv

def decrypt_old(cipher_text, key, iv):
  """ """
  cipher = cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
  decryptor = cipher.decryptor()
  return decryptor.update(cipher_text) + decryptor.finalize()

def encrypt(pwd, key):
  """ """
  print('1st --\n\n', bytes(SALT.encode('utf-8')))
  kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=bytes(SALT.encode('utf-8')), iterations=100000, backend=default_backend())
  encrypted_key = base64.urlsafe_b64encode(kdf.derive(bytes(key.encode('utf-8'))))
  f = Fernet(encrypted_key)
  return f.encrypt(bytes(pwd.encode('utf-8'))), SALT

def decrypt(cipher_txt, key, salt):
  encode_salt = bytes(salt.encode('utf-8'))
  print(encode_salt)
  kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=encode_salt, iterations=100000, backend=default_backend())
  encrypted_key = base64.urlsafe_b64encode(kdf.derive(bytes(key.encode('utf-8'))))
  f = Fernet(encrypted_key)
  return f.decrypt(cipher_txt).decode('utf-8')