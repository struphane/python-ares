

import string
import random
import json

import ajax.ajaxUpdate

NAME = 'Javascript Test'
SHORTCUTS = [('Other Links',
                [('Youpi', 'TestScript')
                 ]

              )
            ]

def report(aresObj):
  # Write your report here
  recordSet = ajax.ajaxUpdate.getRecordSet()
  multibar = aresObj.multiBarChart(recordSet, [{'key': 'Date', 'colName': 'Date', 'type': 'string'},
                                               {'key': 'Value', 'colName': 'Value', 'type': 'number'},
                                               {'key': 'category', 'colName': 'Series', 'type': 'series'}], 'Graph')


  # pie = aresObj.bar(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
  #                               {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
  #                   'Graph')
  #
  # button = aresObj.refresh("", recordSet, 'ajaxUpdate')
  # button.click('''
  #                 %s ;
  #                 %s ;
  #              ''' % (table.jsUpdate(), pie.jsUpdate())
  #              )
  return aresObj

