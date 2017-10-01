import ExAjaxRec

DOWNLOAD = 'SCRIPT'

def report(aresObj):
  recordSet = ExAjaxRec.getRecordSet(aresObj, n=200)
  cloud = aresObj.cloud(recordSet, [{'key': 'CCY', 'colName': 'Currency'},
                                    {'key': 'CATEGORY', 'colName': 'Category'},
                                    {'key': 'PTF', 'colName': 'Portfolio'}
                                    ], headerBox="Currency")

  pieObj = aresObj.pie( recordSet
                      , [ {'key': 'CTY', 'colName': 'Portfolio'}
                        , {'key': 'VAL', 'colName': 'Value', 'type': 'number'}
                        ,
                        ]
                      , headerBox='Concentration per Country')
  aresObj.row([cloud, pieObj])

  tableObj = aresObj.table( recordSet
                          , [ {'key': 'PTF', 'colName': 'Portfolio'}
                            , {'key': 'CTY', 'colName': 'Country'}
                            , {'key': 'CATEGORY', 'colName': 'Product'}
                            , {'key': 'VAL', 'colName': 'Value'}
                            , {'key': 'VAL2', 'colName': 'Value 2'}
                            , {'key': 'VAL3', 'colName': 'Value 3'}
                            ]
                          , headerBox='Population')
