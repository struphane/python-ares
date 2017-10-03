"""

"""

from ares.Lib.graph import AresHtmlGraph

class StackedArea(AresHtmlGraph.JsNvD3Graph):
  """ This object will output a simple stacked area chart

  Reference website: http://nvd3.org/examples/stackedArea.html
  """
  alias = 'stackedAreaChart'
  mockData = r'json\stackedAreaData.json'
  chartObject = 'stackedAreaChart'
  style = {'chartStyle': {'useInteractiveGuideline': 'true', 'clipEdge': 'true'},
           'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   # 'tickFormat' :"function(d) { return d3.time.format('%%x')(new Date(d)) }",
                                   },
                         'yAxis': {'tickFormat': "d3.format(',.2f')"}
                         }}

  clickObject = 'scatter'
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

