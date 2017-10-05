__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):

  # Write your report here
  recordSet = ExAjaxRec.getRecordSet(aresObj)

  pie = aresObj.pie(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}])

  donut = aresObj.donut(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                    {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}])

  aresObj.row([pie, donut])
  #button = aresObj.refresh("", recordSet, 'ExAjaxRec')
  #button.click('''
  #                %s ;
  #                %s ;
  #             ''' % (donut.jsUpdate(), pie.jsUpdate())
  #             )