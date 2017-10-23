import hashlib

SALT_COMPLEMENT = 'egoB397$Fr3d4L-El!$3#f4mgEW'

def generate_key(user_id, salt):
  """ """
  md5_salt = hashlib.md5(bytes(str(salt).encode('utf-8'))).hexdigest()
  key = user_id + md5_salt + SALT_COMPLEMENT
  return hashlib.sha256(bytes(key.encode('utf-8'))).hexdigest()

