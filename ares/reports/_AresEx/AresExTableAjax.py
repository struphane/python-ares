__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  table = aresObj.table([], [
                              {'key': 'PTF', 'colName': 'Portfolio'},
                              {'key': 'CCY', 'colName': 'Currency'},
                              {'key': 'VAL2', 'colName': 'Value 2'},
                              {'key': 'VAL3', 'colName': 'Value 3'}
                        ],
                        'Test Table')
  aresObj.handleRequest(ExAjaxRec.call, {}, table.jsUpdate())
  button = aresObj.refresh("", [], 'ExAjaxRec')
  button.click('''
                  %s ;
               ''' % table.jsUpdate()
               )
