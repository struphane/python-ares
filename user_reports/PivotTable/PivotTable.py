"""
"""

from utils import InFilePricesConfig
from threading import Thread

import AresFileParser

import sys
import random
import time


NAME = 'Pivot Table'
FILE_CONFIGS = [
    {'filename': 'data.txt', 'folder': 'data', 'parser': InFilePricesConfig.InFilePices},
    {'filename': 'filterTable_mytable.txt', 'folder': 'static', 'parser': AresFileParser.FilePivot},
    {'filename': 'country.txt', 'folder': 'static', 'parser': InFilePricesConfig.InFileCountry},
    ]

HTTP_PARAMS = [{'code': 'perimeter', 'dflt': ''},
               {'code': 'multiplier', 'dflt': 1},
               {'code': 'countrows', 'dflt': 10}]


class Afficheur(Thread):
    def __init__(self, lettre):
        Thread.__init__(self)
        self.lettre = lettre

    def run(self):
        i = 0
        while i < 20:
            sys.stdout.write(self.lettre)
            sys.stdout.flush()
            attente = 0.2
            attente += random.randint(1, 60) / 100
            time.sleep(attente)
            i += 1

#def envParams(modalObj):
#  modalObj.date('Super')
#  modalObj.inputInt('Count Table', 'test_count', dflt=10)

def params(modalObj):
  modalObj.input('Perimeter', 'perimeter')
  modalObj.inputInt('Count Table', 'countrows', dflt=10)
  modalObj.inputInt('Multiplier', 'multiplier', dflt=10)

def report(aresObj):
  """  """
  recordSet = []
  for rec in aresObj.files['data.txt']:
    recordSet.append(rec)
  # recordSet = [
  #             {'date': "2011-11-14T16:17:54Z", 'quantity': 2, 'total': 190, 'tip': 100, 'type': "tab"},
  #             {'date': "2011-11-14T16:20:19Z", 'quantity': 2, 'total': 190, 'tip': 100, 'type': "tab"},
  #             {'date': "2011-11-14T16:28:54Z", 'quantity': 1, 'total': 300, 'tip': 200, 'type': "visa"},
  #             {'date': "2011-11-14T16:30:43Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
  #             {'date': "2011-11-14T16:48:46Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
  #             {'date': "2011-11-14T16:53:41Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
  #             {'date': "2011-11-14T16:54:06Z", 'quantity': 1, 'total': 100, 'tip': 0, 'type': "cash"},
  #             {'date': "2011-11-14T16:58:03Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
  #             {'date': "2011-11-14T17:07:21Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
  #             {'date': "2011-11-14T17:22:59Z", 'quantity': 2, 'total': 90, 'tip': 0, 'type': "tab"},
  #             {'date': "2011-11-14T17:25:45Z", 'quantity': 2, 'total': 200, 'tip': 0, 'type': "cash"},
  #             {'date': "2011-11-14T17:29:52Z", 'quantity': 1, 'total': 200, 'tip': 100, 'type': "visa"}
  #           ]

  data = aresObj.crossFilterData(recordSet, [])
  groupVar = data.group('TYPE', 'TTTT')
  groupVar2 = data.group('ISSUER', 'ISSUED_M')
  data.addFilter('TYPE', 'Filter on the type')
  data.addFilter('ISSUER', 'Filter on the type')

  pie = aresObj.xpie(groupVar)
  bar = aresObj.xbar(groupVar2)
  # recordSet = []
  # for rec in aresObj.files['data.txt']:
  #   recordSet.append(rec)
  #
  # header = [[{'colName': '', 'key': 'type'},
  #            {'colName': '', 'key': 'category'},
  #
  #            {'colName': 'D1', 'key': 'd1', 'classname': 'rotate-451'},
  #            {'colName': '', 'key': 'type'},
  #            {'colName': '', 'key': 'type'},
  #            {'colName': '', 'key': 'type'},
  #            {'colName': '', 'key': 'type'},
  #
  #            {'colName': 'D2', 'key': 'd2', 'classname': 'rotate-451'},
  #            {'colName': '', 'key': 'type'},
  #            {'colName': '', 'key': 'type'},
  #            {'colName': '', 'key': 'type'},
  #            {'colName': '', 'key': 'type'},
  #
  #            {'colName': '', 'key': 'formulas'},
  #            ],
  #
  #           [{'colName': '', 'key': 'type'},
  #            {'colName': 'Category', 'key': 'category', 'aresType': 'internalLink', 'script_name': 'testLink'},
  #
  #            {'colName': 'Value', 'key': 'd1_value'},
  #            {'colName': 'Past', 'key': 'd1_past', 'dsc': 'youpi'},
  #            {'colName': 'Next', 'key': 'd1_next'},
  #            {'colName': 'Factor', 'key': 'd1_factor', 'aresType': 'input', 'aresCssAttr': 'font-size:10px;padding:4px;margin:0;width:30px;margin-top:-5px'},
  #            {'colName': 'Stress', 'key': 'd1_stress'},
  #
  #           {'colName': 'Value', 'key': 'd2_value'},
  #            {'colName': 'Past', 'key': 'd2_past'},
  #            {'colName': 'Next', 'key': 'd2_next'},
  #            {'colName': 'Factor', 'key': 'd2_factor', 'aresType': 'input', 'aresCssAttr': 'font-size:10px;padding:4px;margin:0;width:30px;margin-top:-5px'},
  #            {'colName': 'Stress', 'key': 'd2_stress'},
  #
  #            {'colName': 'Formula', 'key': 'formulas', 'aresType': 'input', 'aresCssAttr': 'font-size:10px;padding:4px;margin:0;width:200px;margin-top:-5px'},
  #           ]
  #           ]
  #
  # recordSet = [
  #   {'type': 'Asset', 'category': 'Fed funds', 'd1_value': -10, 'd1_past': 18, 'd1_next': 58, 'd1_factor': 2, 'd1_stress': '',
  #    'd2_value': 20, 'd2_past': -38, 'd2_next': 7, 'd2_factor': 3, 'd2_stress': '',
  #    'formulas': 'Value * Factor + Past',
  #    'dsc_category': 'dsc'},
  #   {'type': 'Asset', 'category': 'Test', 'd1_value': 30, 'd1_past': 38, 'd1_next': 78, 'd1_factor': 4, 'd1_stress': '',
  #    'd2_value': 20, 'd2_past': 28, 'd2_next': 21, 'd2_factor': 3, 'd2_stress': '',
  #    'formulas': 'Value * Factor + Next - StressPrev'
  #    }
  # ]
  #
  # select1 = aresObj.select(['1', '2'], 'Test')
  # data = aresObj.datadic({'1': 23, '2': 78})
  #
  # select2 = aresObj.select(['A', 'B'], 'Test 2')
  # select3 = aresObj.slider(12)
  # select1.update(data, [select2, select3])
  # for i in range(100):
  #   recordSet.append({'type': 'Asset', 'category': 'Fed funds', 'd1_value': -10, 'd1_past': 18, 'd1_next': 58, 'd1_factor': 2, 'd1_stress': '',
  #    'd2_value': 20, 'd2_past': -38, 'd2_next': 7, 'd2_factor': 3, 'd2_stress': '',
  #    'formulas': 'Value * Factor + Past',
  #    'dsc_category': 'dsc'})
  #
  #
  # period = ['d1', 'd2']
  # for rec in recordSet:
  #   for i, d in enumerate(period):
  #     if i == 0:
  #       formula = rec['formulas'].replace('Value', "rec['%s_value']" % d).replace('Past', "rec['%s_past']" % d).\
  #         replace('Next', "rec['%s_next']" % d).replace('Factor', "rec['%s_factor']" % d).\
  #         replace('StressPrev', "rec['%s_value']" % d).replace('Stress', "rec['%s_stress']" % d)
  #     else:
  #       formula = rec['formulas'].replace('Value', "rec['%s_value']" % d).replace('Past', "rec['%s_past']" % d).\
  #         replace('Next', "rec['%s_next']" % d).replace('Factor', "rec['%s_factor']" % d).\
  #         replace('StressPrev', "rec['%s_stress']" % period[i-1]).replace('Stress', "rec['%s_stress']" % d)
  #     rec['%s_stress' % d] = eval(formula)
  #

  # recordSet = [
  #   {'_parent': 'A', 'node_cod': 'A', 'value': 10, 'value2': 10,'level': 0, '_id': 'A', '_leaf': False},
  #   {'_parent': 'A', 'node_cod': 'B', 'value': 20, 'value2': 10,'level': 1, '_id': 'A B', '_leaf': False},
  #   {'_parent': 'B', 'node_cod': 'C', 'value': 30, 'value2': 10,'level': 2, '_id': 'A B C', '_leaf': True},
  #   {'_parent': 'D', 'node_cod': 'D', 'value': 40, 'value2': 10,'level': 0, '_id': 'D', '_leaf': False},
  #   {'_parent': 'D', 'node_cod': 'E', 'value': 50, 'value2': 10,'level': 1, '_id': 'D E', '_leaf': True}]
  #
  # pivotTable = aresObj.tablehyr(recordSet,
  #                                   [{'colName': 'Node', 'key': 'node_cod'},
  #                                    {'colName': 'Sensitivity', 'key': 'value'},
  #                                    {'colName': 'Sensitivity 2', 'key': 'value2'}],
  #                                    ['node_cod'], ['value', 'value2'])
  # pivotTable.buttonExport()
  # pivotTable.buttonGroups('Sensitivities', [([1, 2], 'Youpi')])
  #pivotTable = aresObj.DataTableHyr(recordSet, InFilePricesConfig.InFilePices.getHeader(), ['TYPE', 'CODE'], ['TTTT', 'MMM', 'ISSUED_M'])
  #pivotTable.callBackCreateCellNumberColor([2, 3, 4], 0)
  #pivotTable.callBackSumFooter()
  #pivotTable.buttonExport()
  # pivotTable.callBackColorLevel(0, background='#69a370', font='white')
  # pivotTable.showLevels(2)

  # pivotTable.fixedColumns()
  # pivotTable.fixedHeader()
  # pivotTable.scrollX()
  # pivotTable.callBackCreateUrl(1, 'test', extraCols=[0, 3, 4])
  # pivotTable.callBackCreateCellNumber([2, 3], 1)
  #pivotTable.addRows([{'type': 'Asset', 'category': 'Test', 'formulas': ''}], dflt=1110, pos=2)
  #pivotTable.addRows([{}], dflt='')
  #pivotTable.addRows([{'type': 'Asset', 'category': 'Test', 'formulas': ''}], dflt=55656)

  #pivotTable.addClassCol([1, 0], 'grey_cell')
  #pivotTable.addAttrCol([1, 0], 'css', {'white-space': 'nowrap'})
  #pivotTable.addAttrCol([2, 7], 'css', {'border-left': '1px solid black'}, fromRow=0)
  #pivotTable.hideCol([3, 4, 5, 8, 9, 10])



  #pivotTable.addButtonShow([3, 8], 'Past')
  #pivotTable.addButtonShow([4, 9], 'Next')
  #pivotTable.addButtonShow([5, 10], 'Factors')


  #pivotTable.addButtonGrpShow(2, [2, 3, 4, 5, 6], 'HidePivot')

  #pivotTable.callBackCreateCellThreshold([2, 3, 4, 5, 6, 7, 8, 9, 10], 0, digit=0)
  #pivotTable.hideRows([0, 1], 'Assets')
  #pivotTable.addAttr('css', {'height': '700px'})
  #pivotTable.fixedHeader(300)
  #pivotTable.selectableRow()
  #pivotTable.addPivotFilter('filterTable_mytable.txt', 'filterTable_mytable.txt')
  #pivotTable.agg(['TYPE', 'ISSUER'], ['TTTT'])
  #pivotTable.buttonExport()
  #pivotTable.addCols(['Aurelie'], ['Youpi'])
  #pivotTable.callBackSumFooter()
  #pivotTable.addRow()

  #pivotTable.callBackFooterSum([2, 4])
  #pivotTable.callBackHeaderColumns()
  #pivotTable.callBackNumHeatMap('TTTT', 2)

  #thread_1 = Afficheur("1")
  #thread_2 = Afficheur("2")

  #thread_1.start()
  #thread_2.start()

  #thread_1.join()
  #thread_2.join()

  #textObj = aresObj.text("10")

  #slide = aresObj.slider(10)
  # alert($('#%s tbody tr').eq(0).find('td').eq(4).html())
  #slide.change("var result = 2 * %s + 5 ;%s.html(result) ; %s" % (slide.val, textObj.jqId, pivotTable.jsCell(0,0, slide.val)))

  #aresObj.downloadData('download', 'data2.txt')



