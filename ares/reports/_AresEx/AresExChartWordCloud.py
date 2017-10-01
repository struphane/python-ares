


import ExAjaxQuery

NAME = 'Reports Data Extract'
DOWNLOAD = 'SCRIPT'

def report(aresObj):
  """
  """
  recordSet = ExAjaxQuery.getRecordSet(aresObj.http['DIRECTORY'], n=300)
  cloud = aresObj.cloud(recordSet, [{'key': 'CCY', 'colName': 'Currency'},
                                    {'key': 'CATEGORY', 'colName': 'Category'},
                                    {'key': 'PTF', 'colName': 'Portfolio'}
                                    ], headerBox="Currency")
  button = aresObj.button("Refresh Data")
  button.click('ExAjaxQuery', cloud.jsUpdate(), {'Ok': 1, 'deux': {'ddd': 'dsfdsf'}})


