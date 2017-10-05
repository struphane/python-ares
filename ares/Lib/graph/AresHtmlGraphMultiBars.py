"""


"""

from ares.Lib.graph import AresHtmlGraph

class MultiBars(AresHtmlGraph.JsNvD3Graph):
  """

  """

  mockData = r'json\multiBar.json'
  chartObject = 'multiBarChart'
  alias = 'multiBarChart'
  clickObject = 'multibar'
  style = {'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }",
                                   },
                         'yAxis': {'tickFormat': "d3.format(',.2f')"}
                         },
           'chartDef': {'stacked': 'true'},
           }
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']