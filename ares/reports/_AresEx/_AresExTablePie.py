__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'

def report(aresObj):

# Write your report here
  recordSet = ExAjaxRec.getRecordSet()
  table = aresObj.table(recordSet, [
                                    [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                     {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
                                     {'key': 'VAL', 'colName': 'Value', 'colspan': 2}],

                                     [{'key': 'PTF3', 'colName': 'Portfolio 3'},
                                      {'key': 'PTF2', 'colName': 'Portfolio 2', 'colspan': 1},
                                      {'key': 'VAL1', 'colName': 'Value 1', 'colspan': 1}],

                                    {'key': 'PTF', 'colName': 'Portfolio'},
                                        {'key': 'CCY', 'colName': 'Currency'},
                                        {'key': 'VAL2', 'colName': 'Value 2'},
                                        {'key': 'VAL3', 'colName': 'Value 3'}
                        ],
                        'Test Table')
  table.filters(['Currency', 'Value 2'])
  table.contextMenu([('Ok', 'TestScript', 'CCY'), ('Test', 'TestScript', 'VAL2')])

  pie = aresObj.bar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                    'Graph')

  button = aresObj.refresh("", recordSet, 'ajaxUpdate')
  button.click('''
                  %s ;
                  %s ;
               ''' % (table.jsUpdate(), pie.jsUpdate())
               )