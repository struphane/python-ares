"""

"""

import os
import importlib
import inspect
import ExAjaxRec

from ares.Lib import AresHtml

NAME = 'Ares Example'
# Just to set up the menu on the left hand side
SHORTCUTS = [('Text', [('Input Events', 'AresExText'),
                         ]),

              ('Tables', [('Basic Table', 'AresExTables'),
                         ('Complex Table', 'AresExTablesComplex'),
                         ('Ajax Table', 'AresExTableAjax'),
                         ('Table with Chart', 'AresExTablePie')
                         ]),
             ('Graphs', [('NvD3', 'AresExSimpleCharts'),
                         ('Others', 'AresExOtherCharts'),
                         ]),

             ('Templates', [
               ('World Population', 'AresWorldPopulation'),
               ('Data Extraction', 'AresDataExtract'),
               ('Dashboard 1', 'AresDashboard1.py'),
               ('Dashboard 2', 'AresDashboard2.py'),
               ('Dashboard 3', 'AresDashboard3.py'),
                      ]),
              ]

def report(aresObj):
  """

  """
  recordSet = ExAjaxRec.getRecordSet(aresObj)
  stackedArea = aresObj.stackedArea(recordSet, [{'key': 'PTF', 'colName': 'Portfolio', 'colspan': 1, 'rowspan': 2},
                                                      {'key': 'VAL', 'colName': 'Portfolio 2', 'colspan': 1, 'type': 'number'}],
                                    headerBox='Stacked Bar Chart Example', mockData=True)
  meter = aresObj.meter(1, headerBox='Meter Chart Example', cssAttr={'height': '400px'})

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
  colRight = aresObj.col([meter, titlehtml, aresObj.list(htmlRefs)])
  aresObj.row([colLeft, colRight])
