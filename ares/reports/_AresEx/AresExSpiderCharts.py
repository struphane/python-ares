__author__ = 'HOME'


import ExAjaxRec

NAME = 'Reports Definition'
DOWNLOAD = 'SCRIPT'

def report(aresObj):
  spider = aresObj.spider([], [], headerBox='Pie Chart Example', mockData=True)
  