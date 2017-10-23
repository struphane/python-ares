"""


"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg



class NvD3ScatterChart(AresHtmlGraphSvg.MultiSvg):
  """

  """
  alias, chartObject = 'scatter', 'scatterChart'
  references = ['http://nvd3.org/examples/scatter.html']
  __chartStyle = {'showDistX': 'true',
                  'showDistY': 'true',
                  'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'color': 'd3.scale.category10().range()',
  }

  __chartProp = {
        'xAxis': {'tickFormat': "d3.format('.02f')"},
        'yAxis': {'tickFormat': "d3.format('.02f')"},
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

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


