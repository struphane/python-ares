""" Chart module in charge of generating a Line with Scatter Line PLus Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3ScatterPlusLineChart(AresHtmlGraphSvg.MultiSvg):
  """ NVD3 Scatter Plus Line Chart python interface """
  alias, chartObject = 'scatterline', 'scatterChart'
  references = ['']
  __chartStyle = {'showDistX': 'true',
                  'showDistY': 'true',
                  'duration': '300',
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
    recordSet = AresChartsService.toMultiSeries(self.vals, self.chartKeys, self.selectedX , self.chartVals, extKeys=self.extKeys)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(vals)))

  def jsUpdate(self):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
            d3.select("#%s svg").remove();
            d3.select("#%s").append("svg");
            var %s = nv.models.%s().%s ;
            %s
            d3.select("#%s svg").style("height", '%spx').datum(nv.log(%s)).call(%s);
            nv.utils.windowResize(%s.update);
          ''' % (self.htmlId, self.htmlId, self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
                 self.htmlId, self.height, self.jqData, self.htmlId, self.htmlId)


