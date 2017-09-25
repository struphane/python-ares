__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = ExAjaxRec.getRecordSet()
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

  button = aresObj.refresh("", recordSet, 'ExAjaxRec')
  button.click('''
                  %s ;
                  %s ;
               ''' % (table.jsUpdate(), pie.jsUpdate())
               )