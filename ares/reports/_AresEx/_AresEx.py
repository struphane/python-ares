"""

"""

import os
import importlib
import inspect
import ExAjaxRec

from ares.Lib import AresHtml

NAME = 'Ares Example'
# Just to set up the menu on the left hand side
SHORTCUTS = [('Html Types', [
                  ('slider', 'AresExTables'),
                  ('date', 'AresExTablesComplex'),
                  ('textArea', 'AresExTablesComplex'),
                  ('code', 'AresExTablesComplex'),
                  ('preformat', 'AresExTablesComplex'),
                  ('input', 'AresExTablesComplex'),
                  ('inputInt', 'AresExTablesComplex'),
                  ('inputRange', 'AresExTablesComplex'),
                  ('button', 'AresExTablesComplex'),
                  ('internalLink', 'AresExTablesComplex'),
                  ('externalLink', 'AresExTablesComplex'),
                  ('row and col', 'AresExTablesComplex'),
                  ('radio', 'AresExTablesComplex'),
                  ('select', 'AresExTablesComplex'),
                  ('dropdown', 'AresExTablesComplex'),
                  ('tick', 'AresExTablesComplex'),
                  ('updown', 'AresExTablesComplex'),


                  ]),
             ('Chart Types',
                  [('lineCumulative', 'AresExChartLineCumulative'),
                   ('Pie and donut', 'AresExChartPie'), # Done
                   ('bar', 'AresExChartBar'), # Done
                   ('line', 'AresExChartLine'),
                   #('forceDirected', 'AresExChartLine'),
                   ('stackedArea', 'AresExChartStackedArea'),
                   ('stackedAreaWithFocus', 'AresExChartLine'),
                   ('multiBar', 'AresExChartMultiBar'), # Done
                   ('lineChartFocus', 'AresExChartLine'),
                   ('horizBar', 'AresExChartHorizBar'), # Done
                   ('comboLineBar', 'AresExChartComboLineBar'), # Done
                   ('scatter', 'AresExChartScatter'), # Done
                   ('scatterline', 'AresExChartScatterline'), # Done
                   ('wordcloud', 'AresExChartWordCloud'), # Done
                   #('sunburst', 'AresExChartLine'),
                   ('sparklineplus', 'AresExChartChartLine'),
                   #('boxplot', 'AresExChartLine'),
                   #('candlestickbar', 'AresExChartLine'),
                   ('spider', 'AresExChartSpider'), # Done
                  ]),
              ]

def report(aresObj):
  """

  """
  recordSet = ExAjaxRec.getRecordSet(aresObj)
  stackedArea = aresObj.stackedArea(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                    headerBox='Stacked Bar Chart Example', mockData=True)
  forcedDirected = aresObj.forceDirected(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                    headerBox='Stacked Bar Chart Example', mockData=True)

  # Graph documentation
  graphRefs = []
  for script in os.listdir(os.path.join(aresObj.http['DIRECTORY'], '..', 'ares', 'Lib', 'graph')):
    if script.endswith(".py"):
      mod = importlib.import_module("ares.Lib.graph.%s" % script.replace(".py", ""))
      for name, obj in inspect.getmembers(mod):
        if inspect.isclass(obj):
          for ref in getattr(obj, 'references'):
            graphRefs.append(aresObj.externalLink(None, ref))

  # HTML Objects documentation
  htmlRefs = []
  for script in os.listdir(os.path.join(aresObj.http['DIRECTORY'], '..', 'ares', 'Lib', 'html')):
    if script.endswith(".py"):
      mod = importlib.import_module("ares.Lib.html.%s" % script.replace(".py", ""))
      for name, obj in inspect.getmembers(mod):
        if inspect.isclass(obj) and issubclass(obj, AresHtml.Html):
          for ref in getattr(obj, 'references'):
            htmlRefs.append(aresObj.externalLink(None, ref))

  titleGraph = aresObj.title2("Reference for the charts")
  colLeft = aresObj.col([stackedArea, titleGraph, aresObj.list(graphRefs)])
  titlehtml = aresObj.title2("Reference for the HTLM")
  colRight = aresObj.col([forcedDirected, titlehtml, aresObj.list(htmlRefs)])
  aresObj.row([colLeft, colRight])
