"""


"""

from ares.Lib.graph import AresHtmlGraph

class LineWithFocus(AresHtmlGraph.JsNvD3Graph):
  """

  """

  mockData = r'json\lineWithFocus.json'
  chartObject = 'lineWithFocusChart'
  alias = 'lineChartFocus'

  style = {'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat': "function(d) { return d3.time.format('x')(new Date(d)) }",},
                         'yAxis': {'tickFormat': "d3.format(',.2f')",},
                         'x2Axis': {'showMaxMin': 'false',
                                    'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }",},
                         'y2Axis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']