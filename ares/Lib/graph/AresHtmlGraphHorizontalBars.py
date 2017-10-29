""" Chart module in charge of generating a Horizontal Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3HorizontalBars(AresHtmlGraphSvg.MultiSvg):
  """
  """
  alias, chartObject = 'horizBar', 'multiBarHorizontalChart'
  references = ['http://nvd3.org/examples/multiBarHorizontal.html']
  __chartStyle = {'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'margin': '{top: 30, right: 20, bottom: 50, left: 175}',
                  'showValues': 'true',
                  'showControls': 'true'
  }
  __chartProp = {
          'yAxis': {'tickFormat': "d3.format(',.2f')"}
  }
  # Required CSS and JS modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toMultiSeries(self.vals, self.chartKeys, self.selectedX , self.chartVals, extKeys=self.extKeys)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(vals)))

  def jsUpdate(self):
    dispatchChart = []
    for displathKey, jsFnc in self.dispatch.items():
      dispatchChart.append("%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc))
    return '''
              d3.select("#%s svg").remove();
              d3.select("#%s").append("svg");
              var %s = nv.models.%s().%s ; %s
              d3.select("#%s svg").style("height", '%spx').datum(%s).call(%s);
              nv.utils.windowResize(%s.update);
           ''' % (self.htmlId, self.htmlId, self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
                  self.htmlId, self.height, self.jqData, self.htmlId, self.htmlId)
