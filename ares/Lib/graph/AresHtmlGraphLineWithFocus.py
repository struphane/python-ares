"""


"""

from ares.Lib.graph import AresHtmlGraph

class LineWithFocus(AresHtmlGraph.JsNvD3Graph):
  """ Simple line chart with a focus field to zoom in on specific parts of the chart

    http://nvd3.org/examples/lineWithFocus.html

    Expected data should look like:

    [
    {
      "key" : "North America" ,
      "values" : [ [ 1025409600000 , 23.041422681023] , [ 1028088000000 , 19.854291255832] , [ 1030766400000 , 21.02286281168] ,
        ...]
    },

    {
      "key" : "Africa" ,
      "values" : [ [ 1025409600000 , 7.9356392949025] , [ 1028088000000 , 7.4514668527298] , [ 1030766400000 , 7.9085410566608] ,
        ... ]
    },
    ...
    ]

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