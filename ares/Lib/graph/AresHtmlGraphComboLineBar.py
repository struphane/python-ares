""" Chart module in charge of generating a Combo Bar Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvgMulti


class NvD3ComboLineBar(AresHtmlGraphSvgMulti.MultiSvg):
  """ NVD3 Combo Line Bar Chart python interface """
  alias, chartObject = 'comboLineBar', 'linePlusBarChart'
  references = ['http://nvd3.org/examples/linePlusBar.html']
  __chartStyle = {
        'margin': '{top: 30, right: 60, bottom: 50, left: 70}',
        'x': 'function(d, i) { return i }',
        'y': 'function(d, i) { return d[1] }',
  }
  __chartProp = {
          'y1Axis': {'tickFormat': "d3.format(',f')"},
          'y2Axis': {'tickFormat': "function(d) { return '$' + d3.format(',f')(d) }"},
          'bars': {'forceY': '[0]'}
  }

  __svgProp = {
    'transition': '',
  }

  # Required CSS and JS modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def formatSeries(self, barStyle, colors):
    """ Change the style for a given series and customise the color """
    self.barStyle = barStyle
    self.colors = colors

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toComboChart(self.vals, self.chartKeys, self.selectedX , self.chartVals, barStyle=self.barStyle, colors=self.colors, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    data = data if data is not None else self.jqData
    return '''
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s).call(%(htmlId)s);
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(),
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data}

