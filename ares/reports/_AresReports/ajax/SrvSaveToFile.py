
import re
import collections
from Libs import AresFileParser

def call(aresObj):
  """

  """
  tableAlias = 'datatable'
  pattern = re.compile("%s\[([0-9]*)\]\[([0-9a-zA-Z_]*)\]" % tableAlias)
  recordSet = collections.defaultdict(dict)
  for key, val in aresObj.http.items():
    if key.startswith(tableAlias):
      match = re.search(pattern, key)
      if match:
        recordSet[int(match.group(1))][match.group(2)] = val
  AresFileParser.saveFile(aresObj, recordSet, ['CCY', 'COB'], 'test.dat')
  return 'Youpi'