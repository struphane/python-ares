__author__ = 'HOME'


import ExAjaxQuery

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = ExAjaxQuery.getRecordSet(aresObj)
  table = aresObj.table(recordSet, [
                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                        {'key': 'CCY', 'colName': 'Currency'},
                                        {'key': 'VAL2', 'colName': 'Value 2'},
                                        {'key': 'VAL3', 'colName': 'Value 3'}
                        ],
                        'Test Table')
  table.filters(['Currency', 'Value 2'])
  table.contextMenu([('Ok', 'TestScript', ['CCY']), ('Test', 'TestScript', ['VAL2'])])

  pie = aresObj.bar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    'Graph')
  aresInput = aresObj.input("Report Name", '')
  button = aresObj.button("Refresh Data")
  button.click('ExAjaxQuery', '%s%s' % (table.jsUpdate(), pie.jsUpdate()), {'Ok': 1, 'deux': {'ddd': 'dsfdsf', 'input': aresInput}})
