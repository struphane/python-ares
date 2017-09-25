"""


"""

NAME = 'Table Link CCY and PTF'
DOWNLOAD = 'SCRIPT'

def report(aresObj):
  """
  """
  aresObj.title(NAME)
  aresObj.code("Portfolio = %s" % aresObj.http["VAR0"])
  aresObj.code("Currency = %s" % aresObj.http["VAR1"])