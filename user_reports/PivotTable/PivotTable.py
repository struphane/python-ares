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
  popup = aresObj.modal('Report Parameters')
  popup.modal_header = "Report parameters"
  aresObj.jsOnLoadFnc.add("%s.modal('show'); " % popup.jqId)
  perimeter = aresObj.input('Perimeter')
  multiplier = aresObj.input('Multiplier')
  button = aresObj.internalLink('Run', aresObj.reportName, attrs={'perimeter': perimeter, 'multiplier': multiplier})
  aresObj.addTo(popup, perimeter)
  aresObj.addTo(popup, multiplier)
  aresObj.addTo(popup, button)

def report(aresObj):
  """  """
  recordSet = []
  for rec in aresObj.files['data.txt']:
    recordSet.append(rec)

  pivotTable = aresObj.table(recordSet, InFilePricesConfig.InFilePices.getHeader(), dataFilters={'TYPE': ['Barrier Call']})
  pivotTable.callBackFooterSum([2, 4])
  #pivotTable.pivot(['TYPE', 'ISSUER'], ['TTTT'])

