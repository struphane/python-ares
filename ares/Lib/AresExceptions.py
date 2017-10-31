class AuthException(Exception):
  """ Special class for handling authentication exceptions"""
  def __init__(self, message):
    Exception.__init__(self, message)

class EnvException(AuthException):
  """ """