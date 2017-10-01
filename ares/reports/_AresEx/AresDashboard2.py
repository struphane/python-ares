import ExAjaxRec

DOWNLOAD = 'SCRIPT'

def report(aresObj):
  recordSet = ExAjaxRec.getRecordSet(aresObj)
  mapObj = aresObj.map()
  areasCfg = {}
  for rec in recordSet:
    areasCfg[rec["CTY"]] = areasCfg.get(rec["CTY"], 0) + rec["VAL"]
  mapObj.update_areas(areasCfg)

  pieObj = aresObj.pie( recordSet
                      , [ {'key': 'CTY', 'colName': 'Portfolio'}
                        , {'key': 'VAL', 'colName': 'Value', 'type': 'number'}
                        ,
                        ]
                      , headerBox='Concentration per Country')
  aresObj.row([mapObj, pieObj])

  tableObj = aresObj.table( recordSet
                          , [ {'key': 'PTF', 'colName': 'Portfolio'}
                            , {'key': 'CTY', 'colName': 'Country'}
                            , {'key': 'CATEGORY', 'colName': 'Product'}
                            , {'key': 'VAL', 'colName': 'Value'}
                            , {'key': 'VAL2', 'colName': 'Value 2'}
                            , {'key': 'VAL3', 'colName': 'Value 3'}
                            ]
                          , headerBox='Population')
