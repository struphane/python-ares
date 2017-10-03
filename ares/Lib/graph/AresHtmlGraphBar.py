"""

"""

from ares.Lib.graph import AresHtmlGraph


class Bar(AresHtmlGraph.JsNvD3Graph):
  """

  data format expected in the graph:
    [{key: "Cumulative Return", values: [{ "label": "One","value" : 29.765957771107},  {"label": "Four", "value" : 196.45946739256}]}]
  """
  duration = 200
  mockData = r'json\bar.json'
  alias = 'bar'
  clickObject = 'discretebar'
  icon = 'fa fa-bar-chart'
  chartObject = 'discreteBarChart'
  style = {'chartStyle': {'staggerLabels': 'true',
                          'showValues': 'true',
                          'transitionDuration': '350'
                          } }
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  @classmethod
  def aresExample(cls, aresObj):
    #return aresObj.bar([{"key": "Cumulative Return", "values": [{ "label": "One","value" : 29.765957771107},  {"label": "Four", "value": 196.45946739256}]}])
    return aresObj.bar([{"key": "Cumulative Return", "values": [1, 2, 3, 4, 5]}])