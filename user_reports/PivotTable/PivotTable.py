"""
"""

from utils import InFilePricesConfig

NAME = 'Pivot Table'
FILE_CONFIGS = [
    {'filename': 'data.txt', 'folder': 'outputs', 'parser': InFilePricesConfig.InFilePices},
    ]

def report(aresObj):
  """  """

  recordSet = []
  for rec in aresObj.files['data.txt']:
    recordSet.append(rec)
  print recordSet[0]
  pivotTable = aresObj.table(recordSet, InFilePricesConfig.InFilePices.getHeader())
  pivotTable.pivot(['TYPE', 'ISSUER'], ['TTTT'])

