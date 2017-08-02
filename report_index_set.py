"""


"""

import os

def call(aresObj):
  """
  """
  path = os.path.join("user_reports", aresObj.http['POST']['report'])
  if not os.path.exists(path):
      os.makedirs(path)
      return '%s - Report created %s' % aresObj.http['POST']['report']

  else:
    return '%s - Already exist' % aresObj.http['POST']['report']