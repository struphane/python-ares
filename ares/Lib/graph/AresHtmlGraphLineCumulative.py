""" Chart module in charge of generating a Line Cumulative Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvgMulti


class NvD3LineCumulative(AresHtmlGraphSvgMulti.MultiSvg):
  """

  """
  alias, chartObject = 'lineCumulative', 'cumulativeLineChart'
  references = ['http://nvd3.org/examples/cumulativeLine.html']
  __chartStyle = {
    'x': 'function(d) { return d[0] }',
    'y': 'function(d) { return d[1]/100 }',
    'color': 'd3.scale.category10().range()',
    'useInteractiveGuideline': 'true',
    'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvgMulti.MultiSvg.colorCharts),
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
    recordSet = AresChartsService.toMultiSeries(self.vals, self.chartKeys, self.selectedX , self.chartVals, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    return '''
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s).call(%(htmlId)s);
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(),
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data}
