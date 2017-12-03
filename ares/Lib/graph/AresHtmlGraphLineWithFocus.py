""" Chart module in charge of generating a Line with Focus Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvgMulti


class NvD3LineWithFocus(AresHtmlGraphSvgMulti.MultiSvg):
  """ NVD3 Line with Focus Chart python interface """
  alias, chartObject = 'lineChartFocus', 'lineWithFocusChart'
  references = ['http://nvd3.org/examples/lineWithFocus.html']
  __chartStyle = {
      'x': "function(d) { return d[0]; }",
      'y': "function(d) { return d[1]; }"
  }

  __chartProp = {
    #'xAxis': {'tickFormat': "d3.format(',f')"},
    #'yAxis': {'tickFormat': "d3.format(',.2f')"},
    #'y2Axis': {'tickFormat': "d3.format(',.2f')"},
  }

  __svgProp = {
      'transition': '',
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def xAxisAsDate(self):
    """ Force the x axis to be a date """
    self.addChartProp('xAxis', {'tickFormat': "function(d) { return d3.time.format('%Y/%m/%d')(new Date(d)) }"})
    self.addChartProp('x2Axis', {'tickFormat': "function(d) { return d3.time.format('%Y/%m/%d')(new Date(d)) }"})

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