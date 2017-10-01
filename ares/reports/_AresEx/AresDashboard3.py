
import ExAjaxRec
import random

DOWNLOAD = 'SCRIPT'

def report(aresObj):
  recordSet = ExAjaxRec.getRecordSet(aresObj, n=1000)
  cloud = aresObj.cloud(recordSet, [{'key': 'CCY', 'colName': 'Currency'},
                                    {'key': 'CATEGORY', 'colName': 'Category'},
                                    {'key': 'PTF', 'colName': 'Portfolio'}
                                    ], headerBox="Currency")

  meter = aresObj.meter(random.randint(0, 100) / 100.0, headerBox='Percentage Completion')
  cols = aresObj.col([meter, aresObj.vignet('Current Value and evolution', 'The value has decreased from yesterday', aresObj.updown(random.randint(1000, 1000), random.randint(-10, 10)))])
  aresObj.row([cloud, cols])

  tableObj = aresObj.table( recordSet
                          , [ {'key': 'PTF', 'colName': 'Portfolio'}
                            , {'key': 'CTY', 'colName': 'Country'}
                            , {'key': 'CATEGORY', 'colName': 'Product'}
                            , {'key': 'VAL', 'colName': 'Value'}
                            , {'key': 'VAL2', 'colName': 'Value 2'}
                            , {'key': 'VAL3', 'colName': 'Value 3'}
                            ]
                          , headerBox='Population')
  tableObj.pageLength = 10
