"""
"""

from utils import InFilePricesConfig

NAME = 'Pivot Table'
FILE_CONFIGS = [
    {'filename': 'data.txt', 'folder': 'outputs', 'parser': InFilePricesConfig.InFilePices},
    {'filename': 'country.txt', 'folder': 'static', 'parser': InFilePricesConfig.InFileCountry},
    ]

def report(aresObj):
  """  """

  recordSet = []
  for rec in aresObj.files['data.txt']:
    recordSet.append(rec)

  pivotTable = aresObj.table(recordSet, InFilePricesConfig.InFilePices.getHeader(), dataFilters={'TYPE': ['Barrier Call']})
  #pivotTable.pivot(['TYPE', 'ISSUER'], ['TTTT'])

