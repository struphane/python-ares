"""
"""

from utils import InFilePricesConfig
from threading import Thread

import AresFileParser

import sys
import random
import time


NAME = 'Pivot Table'
FILE_CONFIGS = [
    {'filename': 'data.txt', 'folder': 'data', 'parser': InFilePricesConfig.InFilePices},
    {'filename': 'filterTable_mytable.txt', 'folder': 'static', 'parser': AresFileParser.FilePivot},
    {'filename': 'country.txt', 'folder': 'static', 'parser': InFilePricesConfig.InFileCountry},
    ]

HTTP_PARAMS = [{'code': 'perimeter', 'dflt': ''},
               {'code': 'multiplier', 'dflt': 1},
               {'code': 'countrows', 'dflt': 10}]


class Afficheur(Thread):
    def __init__(self, lettre):
        Thread.__init__(self)
        self.lettre = lettre

    def run(self):
        i = 0
        while i < 20:
            sys.stdout.write(self.lettre)
            sys.stdout.flush()
            attente = 0.2
            attente += random.randint(1, 60) / 100
            time.sleep(attente)
            i += 1

def params(aresObj):
  popup = aresObj.modal('Report Parameters')
  popup.modal_header = "Report parameters"
  aresObj.jsOnLoadFnc.add("%s.modal('show'); " % popup.jqId)
  perimeter = aresObj.input('Perimeter')
  coutRow = aresObj.inputInt('Count Table')
  coutRow.addVal(10)
  multiplier = aresObj.input('Multiplier')
  button = aresObj.internalLink('Run', aresObj.reportName, attrs={'perimeter': perimeter, 'multiplier': multiplier, 'countrows': coutRow})
  aresObj.addTo(popup, perimeter)
  aresObj.addTo(popup, multiplier)
  aresObj.addTo(popup, coutRow)
  aresObj.addTo(popup, button)

def report(aresObj):
  """  """
  recordSet = []
  for rec in aresObj.files['data.txt']:
    recordSet.append(rec)

  pivotTable = aresObj.table(recordSet, InFilePricesConfig.InFilePices.getHeader(), headerBox="Youpi", cssAttr={'width': '500px'}, globalSortBy=('TTTT', 'asc', int(aresObj.http['countrows'])))
  pivotTable.addPivotFilter('filterTable_mytable.txt', 'filterTable_mytable.txt')
  pivotTable.agg(['TYPE', 'ISSUER'], ['TTTT'])
  pivotTable.buttonExport()
  pivotTable.addCols(['Aurelie'], ['Youpi'])
  pivotTable.callBackSumFooter()
  #pivotTable.addRow()

  #pivotTable.callBackFooterSum([2, 4])
  #pivotTable.callBackHeaderColumns()
  #pivotTable.callBackNumHeatMap('TTTT', 2)

  #thread_1 = Afficheur("1")
  #thread_2 = Afficheur("2")

  #thread_1.start()
  #thread_2.start()

  #thread_1.join()
  #thread_2.join()




