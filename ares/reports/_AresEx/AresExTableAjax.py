__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'


def MyCall(params):
  return [{"ID": "ZQE12P", "PTF": 541, "PTF2": 952, "CATEGORY": "Index", "VAL2": 81.07010355086975, "VAL3": 101.87727730826197, "VAL": 16.154792322896572, "CCY": "GBP"}, {"ID": "873NSB", "PTF": 417, "PTF2": 1005, "CATEGORY": "TRS", "VAL2": 7.386721932681928, "VAL3": 220.78701478268923, "VAL": 48.81165139956292, "CCY": "EUR"}, {"ID": "WU73YR", "PTF": 381, "PTF2": 911, "CATEGORY": "Bond", "VAL2": 47.16860795423494, "VAL3": 184.56143688336448, "VAL": 82.505660714631, "CCY": "EUR"}, {"ID": "FMUOGE", "PTF": 705, "PTF2": 964, "CATEGORY": "Index", "VAL2": 19.014504330592054, "VAL3": 298.4775283966462, "VAL": 34.61584120194053, "CCY": "GBP"}, {"ID": "G17LB8", "PTF": 617, "PTF2": 919, "CATEGORY": "Option", "VAL2": 64.03404540638323, "VAL3": 61.74960436798685, "VAL": 0.6227023236766938, "CCY": "EUR"}]

def report(aresObj):

  # Write your report here
  #recordSet = ExAjaxRec.getRecordSet(aresObj)
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
