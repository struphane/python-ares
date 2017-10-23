"""

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3StackedArea(AresHtmlGraphSvg.MultiSvg):
  """ This object will output a simple stacked area chart

  """
  alias, chartObject = 'stackedArea', 'stackedAreaChart'
  references = ['http://nvd3.org/examples/stackedArea.html']
  __chartStyle = {'margin': '{right: 100}',
                  'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'useInteractiveGuideline': 'true',
                  'rightAlignYAxis': 'true',
                  'showControls': 'true',
                  'clipEdge': 'true',
  }

  __chartProp = {
     'xAxis': {'tickFormat': "function(d) { return d3.time.format('%x')( new Date(d) ) }", 'showMaxMin': 'false'},
     'yAxis': {'tickFormat': "d3.format(',.2f')"},
     #'zoom': {'enabled': 'true', 'scaleExtent': '[1,10]', 'useFixedDomain': 'false', 'useNiceScale': 'false',
     #         'horizontalOff': 'false', 'verticalOff': 'true', 'unzoomEventType': '"dblclick.zoom"'}
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
