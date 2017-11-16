"""
"""

import os
import re
import sys
import re
import collections

regex = re.compile('[^a-zA-Z0-9_]')

from Libs import AresFileParser

def call(aresObj):
  """

  """
  tableAlias = 'datatable'
  pattern = re.compile("%s\[([0-9]*)\]\[([0-9a-zA-Z_]*)\]" % tableAlias)
  resultObj = collections.defaultdict(dict)
  for key, val in aresObj.http.items():
    if key.startswith(tableAlias):
      match = re.search(pattern, key)
      if match:
        resultObj[int(match.group(1))][match.group(2)] = val
  moduleName, className = aresObj.http['parserModule'].split(".")

  reportPath = os.path.join(aresObj.http['DIRECTORY'], aresObj.http['reportName'])
  sys.path.append(reportPath)

  __import__(aresObj.http['reportName'])
  mod = __import__("utils.%s" % moduleName)
  ajaxMod = getattr(getattr(mod, moduleName), className)
  recordSet = []
  if ajaxMod.hdrLines != 0:
    recordSet.append(dict([(col.get('key', regex.sub('', col['colName'])), col['colName']) for col in ajaxMod.cols]))
  rowNumers = max(resultObj.keys())
  for colIndex in range(rowNumers+1):
    recordSet.append(resultObj[colIndex])
  AresFileParser.saveFile(aresObj, aresObj.http['reportName'], recordSet, [col.get('key', regex.sub('', col['colName'])) for col in ajaxMod.cols], ajaxMod.delimiter, aresObj.http['fileName'])
  return 'File - %s - updated' % aresObj.http['fileName']