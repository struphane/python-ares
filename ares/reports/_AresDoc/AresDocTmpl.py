"""

"""

import collections
import os

NAME = 'Templates'
DOWNLOAD = None

def report(aresObj):
  """

  """
  aresObj.title("Report Template")
  aresObj.title2("Template for a report")
  tmpplPath = os.path.join(aresObj.http['DIRECTORY'], "..", "ares", "tmpl")
  reportTmpl = open(os.path.join(tmpplPath, "tmpl_report.py"))
  aresObj.preformat(aresObj.code(reportTmpl.read()))
  reportTmpl.close()

  aresObj.title2("Template for a Ajax Call")
  reportTmpl = open(os.path.join(tmpplPath, "tmpl_service.py"))
  aresObj.preformat(aresObj.code(reportTmpl.read()))
  reportTmpl.close()