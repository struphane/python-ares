"""
"""

from utils import InFilePricesConfig

NAME = 'Pivot Table'
FILE_CONFIGS = [
    {'filename': 'data.txt', 'folder': 'outputs', 'parser': InFilePricesConfig.InFilePices},
    {'filename': 'country.txt', 'folder': 'static', 'parser': InFilePricesConfig.InFileCountry},
    ]

HTTP_PARAMS = [{'code': 'PERIMETER', 'dflt': ''},
               {'code': 'MULTIPLIER'}]

def params(aresObj):
  perimeter = aresObj.input()
  multiplier = aresObj.input()
  aresObj.internalLink('Run', aresObj.reportName, attrs={'perimeter': perimeter, 'multiplier': multiplier})

def report(aresObj):
  """  """
  print aresObj.http
  recordSet = []
  for rec in aresObj.files['data.txt']:
    recordSet.append(rec)

  pivotTable = aresObj.table(recordSet, InFilePricesConfig.InFilePices.getHeader(), dataFilters={'TYPE': ['Barrier Call']})
  pivotTable.callBackFooterSum([2, 4])
  #pivotTable.pivot(['TYPE', 'ISSUER'], ['TTTT'])

