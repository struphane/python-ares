import Crypto.Random
from Crypto.Cipher import AES
import hashlib

# salt size in bytes
SALT_SIZE = 32

# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 20

# the size multiple required for AES
AES_MULTIPLE = 32


def generate_key(user_id, salt, iterations):
  """ Generate Key and iterate over"""
  if iterations <= 0:
    raise Exception("Number of iterations has to be greater than 0")

  key = user_id + salt
  for i in range(iterations):
    key = hashlib.sha256(key).digest()
  return key

def pad_text(text, multiple):
  """Add Padding """
  extra_bytes = len(text) % multiple
  padding_size = multiple - extra_bytes
  padding = chr(padding_size) * padding_size
  padded_text = text + padding
  return padded_text

def unpad_text(padded_text):
  """ Remove Padding"""
  padding_size = ord(padded_text[-1])
  text = padded_text[:-padding_size]
  return text

def encrypt(plaintext, password):
  """ """
  salt = Crypto.Random.get_random_bytes(SALT_SIZE)
  key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
  cipher = AES.new(key, AES.MODE_ECB)
  padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
  tempCipherTxt = cipher.encrypt(padded_plaintext)
  cipherTxt = salt + tempCipherTxt
  return cipherTxt

def decrypt(ciphertext, password):
  salt = ciphertext[0:SALT_SIZE]
  tmpCipherTxt = ciphertext[SALT_SIZE:]
  key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
  cipher = AES.new(key, AES.MODE_ECB)
  padded_plaintext = cipher.decrypt(tmpCipherTxt)
  plaintext = unpad_text(padded_plaintext)
  return plaintext