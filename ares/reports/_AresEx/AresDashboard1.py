"""


"""


import ExAjaxRec

def report(aresObj):
  """
  """

  recordSet = ExAjaxRec.getRecordSet(aresObj)

  table = aresObj.table(recordSet, [{'key': 'PTF', 'colName': 'Portfolio'},
                                    {'key': 'CCY', 'colName': 'Currency'},
                                    {'key': 'CATEGORY', 'colName': 'Product'},
                                    {'key': 'VAL', 'colName': 'Value'},
                                    ], headerBox='Population')
  table.pageLength = 6
  pie = aresObj.pie(recordSet, [
                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                    {'key': 'VAL', 'colName': 'Value', 'type': 'number'},
                                 ], headerBox='Concentration per Portfolio')
  bar = aresObj.bar(recordSet, [
                                    {'key': 'CATEGORY', 'colName': 'Product'},
                                    {'key': 'VAL', 'colName': 'Value', 'type': 'number'},
                                 ], headerBox='Concentration per Portfolio')

  aresObj.row([table, pie, bar])