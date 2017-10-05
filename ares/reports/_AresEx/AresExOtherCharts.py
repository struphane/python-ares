__author__ = 'HOME'

import random
import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

# Write your report here
  recordSet = ExAjaxRec.getRecordSet(aresObj, n=1000)
  mapObj = aresObj.map()
  areasCfg = {}
  for rec in recordSet:
    areasCfg[rec["CTY"]] = areasCfg.get(rec["CTY"], 0) + rec["VAL"]
  mapObj.update_areas(areasCfg)
  meter = aresObj.meter(random.randint(0, 100) / 100.0, headerBox='Percentage Completion')
  cloud = aresObj.cloud(recordSet, [{'key': 'CCY', 'colName': 'Currency'},
                                    {'key': 'CATEGORY', 'colName': 'Category'},
                                    {'key': 'PTF', 'colName': 'Portfolio'}
                                    ], headerBox="Currency")
  aresObj.row([mapObj, meter])
  cloud