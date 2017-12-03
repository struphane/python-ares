""" Chart module in charge of generating a PlotBox Chart
@author: Olivier Nogues

"""
#TODO Migrate to the new Chart framework

import json
from ares.Lib.html import AresHtmlRadio
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg
from ares.Lib.html import AresHtmlContainer


class NvD3PlotBox(AresHtmlGraphSvg.Svg):
  """ NVD3 Plot Box python interface """
  alias, chartObject = 'boxplot', 'boxPlotChart'
  references = ['http://nvd3.org/examples/pie.html']
  __chartStyle = {'x': "function(d) { return d.label }",
                  'maxBoxWidth': '75',
                  'yDomain': '[0, 500]',
                  'staggerLabels': "true"}

  __svgProp = { } # Do not update those variables directly, please use the functions in the base class !

  __chartProp = { } # Do not update those variables directly, please use the functions in the base class !

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  seriesNames, withMean = None, True

  @property
  def jqData(self):
    """ Returns the javascript SVG reference """
    return "data_%s[%s]" % (self.htmlId, self.categories.val)

  def setVals(self, q1, q2, q3, whisker_low, whisker_high):
    """ Set a default value for the graph """
    self.chartVals = [q1, q2, q3, whisker_low, whisker_high, '']
    self.selectedChartVal = 'FIXED'

  def processData(self):
      """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
      recordSet = AresChartsService.toPlotBox(self.vals, self.chartKeys, self.chartVals, withMean=self.withMean, seriesNames=self.seriesNames)
      self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    return '''
              d3.select("#%(htmlId)s svg").remove();
              d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ;
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s)%(svgProp)s.call(%(htmlId)s);
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(),
                   'data': data, 'svgProp': self.getSvg(), 'height': self.height}

  def __str__(self):
    """ Return the svg container """
    self.processData()
    self.categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _, _ in self.chartKeys],
                                          cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {},
                                          checked=self.selectedChartKey)
    self.categories.click([self])
    self.htmlContent.append(str(self.categories))

    self.htmlContent.append('<div %s><svg style="width:100%%;height:%spx;"></svg></div>' % (self.strAttr(), self.height))
    if self.headerBox:
      return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

    return "\n".join(self.htmlContent)

  def processDataMock(self, cat=None, val=None):
    """ Return the json data """
    self.chartKeys = [('MOCK', None, None)]
    self.selectedChartKey = 'MOCK'
    self.chartVals = [('DATA', None)]
    self.selectedChartVal = self.chartVals[0][0]
    self.aresObj.jsGlobal.add("data_%s = {'%s', %s}" % (self.htmlId, self.selectedChartKey, open(r"ares\json\%sData.json" % self.alias).read().strip()))