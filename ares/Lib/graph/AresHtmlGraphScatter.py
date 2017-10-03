"""


"""

from ares.Lib.graph import AresHtmlGraph

class ScatterChart(AresHtmlGraph.JsNvD3Graph):
  """ Simple Scatter chart

    http://nvd3.org/livecode/index.html#codemirrorNav

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
  mockData = r'json\multiBar.json'
  chartObject = 'scatterChart'
  alias = 'scatterChart'
  style = {'chartStyle': {},
           'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }"},
                         'yAxis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']