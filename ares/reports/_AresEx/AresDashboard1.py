"""


"""


import ExAjaxRec

DOWNLOAD = 'SCRIPT'

def report(aresObj):
  """ Dummy report """

  # This will extract the data from the recordSet
  recordSet = ExAjaxRec.getRecordSet(aresObj)

  # This will create a horizontal bar chart on the page display
  # It will use the key of the recordSet and the colName will represent the values
  hbar = aresObj.horizBarChart(recordSet, [{'key': 'CCY', 'colName': 'Currency'},
                                           {'key': 'VAL', 'colName': 'Value', 'type': 'number'},
                                           {'key': 'PTF', 'colName': 'Portfolio', 'type': 'series'}
                                          ], headerBox='Per Currency')

  hbar.delAttr('xAxis', 'tickFormat')
  hbar.addStyle({'showControls': 'true'})

  # This will create a Bar chart on the page display
  # It will use the key of the recordSet and the colName will represent the values
  bar = aresObj.bar(recordSet, [
                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                    {'key': 'VAL', 'colName': 'Value', 'type': 'number'},
                                 ], headerBox='Concentration per Portfolio')

  # This will create a Pie chart on the page display
  # It will use the key of the recordSet and the colName will represent the values
  pie = aresObj.pie(recordSet, [
                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                    {'key': 'VAL', 'colName': 'Value', 'type': 'number'},
                                 ], headerBox='Concentration per Portfolio')

  # Special container to display all the chart on the same page
  aresObj.row([pie, bar])

  # Display the recordSet as a tab;e
  # Same concept the columns to be displayed are selected by using the key
  newRecordSet = []
  for rec in recordSet:
    if rec['VAL'] < 20:
      rec['TICK'] = aresObj.tick(False)
    else:
      rec['TICK'] = aresObj.tick(True)
    newRecordSet.append(rec)
  aresObj.table(newRecordSet, [{'key': 'PTF', 'colName': 'Portfolio'},
                                {'key': 'CCY', 'colName': 'Currency'},
                                {'key': 'CATEGORY', 'colName': 'Product'},
                                {'key': 'VAL', 'colName': 'Value'},
                                {'key': 'TICK', 'colName': 'Type', 'type': 'object'},
                                ], headerBox='Population')