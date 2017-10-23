"""


"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3SparkLinePlus(AresHtmlGraphSvg.MultiSvg):
  """

  """
  alias, chartObject = 'sparklineplus', 'sparklinePlus'
  references = ['http://nvd3.org/examples/line.html']
  __chartStyle = {
    'margin': '{left:70}',
    'x': "function(d) { return d[0]; }",
    'y': "function(d) { return d[1]; }",
    'showLastValue': 'true',
    'showLastValue': "function(d) {return d3.time.format('%x')(new Date(data[d].x))}",
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def filterSerie(self, key):
    """  """
    self.filterAKey = key

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toMultiSeries(self.vals, self.chartKeys, self.selectedX , self.chartVals)
    for key, recordSets in recordSet.items():
      for recrordSet in recordSets:
        if recrordSet['key'] ==  self.filterAKey:
          self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(recrordSet['values'])))

  def jsUpdate(self):
    dispatchChart = []
    for displathKey, jsFnc in self.dispatch.items():
      dispatchChart.append("%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc))
    return '''
              var %s = nv.models.%s().%s ;
              %s
              d3.select("#%s svg").datum(%s).call(%s);
              nv.utils.windowResize(%s.update);
          ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
                 self.htmlId, self.jqData, self.htmlId, self.htmlId)