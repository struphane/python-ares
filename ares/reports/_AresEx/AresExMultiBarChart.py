

import string
import random
import json

import ExAjaxRec

NAME = 'Javascript Test'

def report(aresObj):
  # Write your report here
  recordSet = ExAjaxRec.getRecordSet(aresObj.http['DIRECTORY'])
  multibar = aresObj.multiBarChart(recordSet, [{'key': 'Date', 'colName': 'Date', 'type': 'string'},
                                               {'key': 'VAL', 'colName': 'Value', 'type': 'number'},
                                               {'key': 'CATEGORY', 'colName': 'Series', 'type': 'series'}], 'Graph')

  return aresObj

