"""

"""

from ares.Lib.graph import AresHtmlGraph


class ComboLineBar(AresHtmlGraph.JsNvD3Graph):
  """
  This object will combine a line and a bar chart.
  The first item should be the line chart

  The second will the bar chart

  Reference website: http://nvd3.org/examples/linePlusBar.html
  """
  alias = 'comboLineBar'
  mockData = r'json\linePlusBarData.json'
  chartObject = 'linePlusBarChart'

  style = {'chartStyle': {'color': 'd3.scale.category10().range()'},
           'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }",
                                   },
                         'bars': {'forceY': '[0]'},
                         'y1Axis': {'tickFormat': "d3.format(',.2f')"},
                         'y2Axis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']