""" Chart module in charge of generating a Line with Stacked with Focus AreaChart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvgMulti


class NvD3StackedAreaWithFocus(AresHtmlGraphSvgMulti.MultiSvg):
  """ NVD3 Stacked Area with focus Chart python interface """
  alias, chartObject = 'stackedAreaWithFocus', 'stackedAreaWithFocusChart'
  references = ['http://nvd3.org/examples/stackedArea.html']
  __chartStyle = {'useInteractiveGuideline': 'true',
                  'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvgMulti.MultiSvg.colorCharts),
                  'controlLabels': '{stacked: "Stacked"}',
                  'duration': 'true',
                  'showControls': '300',
  }

  __chartProp = {
     'xAxis': {'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }", 'showMaxMin': 'false'},
     'x2Axis': {'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }"},
     'yAxis': {'tickFormat': "d3.format(',.2f')"},
     'y2Axis': {'tickFormat': "d3.format(',.2f')"},
     'legend': {'vers': "'furious'"}
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

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

