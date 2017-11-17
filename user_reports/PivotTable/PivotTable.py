"""
"""

from utils import InFilePricesConfig

import AresFileParser

NAME = 'Pivot Table'
FILE_CONFIGS = [
    {'filename': 'data.txt', 'folder': 'data', 'parser': InFilePricesConfig.InFilePices},
    {'filename': 'filterTable_mytable.txt', 'folder': 'static', 'parser': AresFileParser.FilePivot},
    {'filename': 'country.txt', 'folder': 'static', 'parser': InFilePricesConfig.InFileCountry},
    ]

HTTP_PARAMS = [{'code': 'perimeter', 'dflt': ''},
               {'code': 'multiplier'}]

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

  pivotTable = aresObj.table(recordSet, InFilePricesConfig.InFilePices.getHeader(), headerBox="Youpi")
  pivotTable.addPivotFilter('filterTable_mytable.txt')
  pivotTable.agg(['TYPE', 'ISSUER'], ['TTTT'])
  pivotTable.addRow()

  #pivotTable.callBackFooterSum([2, 4])
  #pivotTable.callBackHeaderColumns()
  pivotTable.callBackNumHeatMap('TTTT', 2)

