"""


"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3LineCumulative(AresHtmlGraphSvg.MultiSvg):
  """

  """
  alias, chartObject = 'lineCumulative', 'cumulativeLineChart'
  references = ['http://nvd3.org/examples/cumulativeLine.html']
  __chartStyle = {
    'x': 'function(d) { return d[0] }',
    'y': 'function(d) { return d[1]/100 }',
    'color': 'd3.scale.category10().range()',
    'useInteractiveGuideline': 'true',
  }

  __chartProp = {
    'xAxis': {'tickValues': "[1078030800000,1122782400000,1167541200000,1251691200000]",
              'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }"},
    'yAxis': {'tickFormat': "d3.format(',.1%')"},
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toMultiSeries(self.vals, self.chartKeys, self.selectedX , self.chartVals)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(vals)))

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
