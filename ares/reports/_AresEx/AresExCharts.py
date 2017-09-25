__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

# Write your report here
  recordSet = ExAjaxRec.getRecordSet(aresObj)
  print recordSet
  pie = aresObj.bar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL6', 'colName': 'Teest', 'type': 'object'},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    'Graph')

  button = aresObj.refresh("", recordSet, 'ExAjaxRec')
  button.click('''
                  %s ;
               ''' % pie.jsUpdate()
               )