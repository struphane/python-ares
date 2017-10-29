""" Chart module in charge of generating a Bar Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3Bar(AresHtmlGraphSvg.Svg):
  """

  data format expected in the graph:
    [{key: "Cumulative Return", values: [{ "label": "One","value" : 29.765957771107},  {"label": "Four", "value" : 196.45946739256}]}]
  """
  alias, chartObject = 'bar', 'discreteBarChart'
  references = ['http://nvd3.org/examples/discreteBar.html']
  __chartStyle = {'showValues': 'true',
                  'staggerLabels': 'true',
                  'x': "function(d) { return d[0]; }",
                  'y': "function(d) { return d[1]; }"}
  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  seriesName = ''

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toBar(self.vals,self.seriesName, self.chartKeys, self.chartVals, extKeys=self.extKeys)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(vals)))

  def jsUpdate(self):
    """  """
    dispatchChart = []
    for displathKey, jsFnc in self.dispatch.items():
      dispatchChart.append("%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc))
    return '''
              d3.select("#%s svg").remove();
              d3.select("#%s").append("svg");
              var %s = nv.models.%s().%s ;
              d3.select("#%s svg").style("height", '%spx').datum(%s).call(%s);
              nv.utils.windowResize(%s.update);
            ''' % (self.htmlId, self.htmlId, self.htmlId, self.chartObject, self.attrToStr(),
                   self.htmlId, self.height, self.jqData, self.htmlId, self.htmlId)


