__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = ExAjaxRec.getRecordSet(aresObj)
  table = aresObj.table(recordSet, [
                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                    {'key': 'CCY', 'colName': 'Currency'},
                                    {'key': 'VAL2', 'colName': 'Value 2'},
                                    {'key': 'VAL3', 'colName': 'Value 3'}
                        ],
                        'Test Table')
  button = aresObj.refresh("", recordSet, 'ExAjaxRec')
  button.click('''
                  %s ;
               ''' % table.jsUpdate()
               )