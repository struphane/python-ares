"""


"""

from ares.Lib.graph import AresHtmlGraph

class HorizontalBars(AresHtmlGraph.JsNvD3Graph):
  """ Simple Horizontal bar chart

    http://nvd3.org/examples/multiBarHorizontal.html

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
  alias = 'horizBarChart'
  mockData = r'json\horizBars.json'
  chartObject = 'multiBarHorizontalChart'

  style = {'chartStyle': {'margin': '{top: 30, right: 20, bottom: 50, left: 175}',
                          'showValues': 'true',
                          'tooltips': 'false',
                          'showControls': 'false'},
           'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat':"function(d) { return d3.time.format('%x')(new Date(d)) }",},
                         'yAxis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']
