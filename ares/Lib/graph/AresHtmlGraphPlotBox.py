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
    return "eval('%s_' + %s + '_FIXED')" % (self.htmlId, self.dynKeySelection)

  def setVals(self, q1, q2, q3, whisker_low, whisker_high):
    """ Set a default value for the graph """
    self.chartVals = [q1, q2, q3, whisker_low, whisker_high, '']
    self.selectedChartVal = 'FIXED'

  def processData(self):
      """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
      recordSet = AresChartsService.toPlotBox(self.vals, self.chartKeys, self.chartVals,
                                              withMean=self.withMean, seriesNames=self.seriesNames)
      for key, vals in recordSet.items():
        self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, regex.sub('', key.strip()), json.dumps(vals)))

  def jsUpdate(self):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
              var %s = nv.models.%s().%s ;
              d3.select("#%s svg").datum(%s)%s.call(%s);
              nv.utils.windowResize(%s.update);
            ''' % (self.htmlId, self.chartObject, self.attrToStr(),
                   self.htmlId, self.jqData, self.getSvg(), self.htmlId, self.htmlId)

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _ in self.chartKeys], cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {})
    categories.select(self.selectedChartKey)
    self.dynKeySelection = categories.val # The javascript representation of the radio
    self.dynValSelection = 'FIXED' # The javascript representation of the radio
    categories.click([self])
    self.htmlContent.append(str(categories))
    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(self.jsUpdate())

  def __str__(self):
    """ Return the svg container """
    self.processData()
    self.htmlContent.append('<div %s class="gallery"><svg style="width:100%%;height:400px;"></svg></div>' % self.strAttr())
    return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

  def processDataMock(self, cat=None, val=None):
    """ Return the json data """
    self.chartKeys = [('MOCK', None)]
    self.selectedChartKey = 'MOCK'
    self.chartVals = [('DATA', None)]
    self.selectedChartVal = self.chartVals[0][0]
    self.aresObj.jsGlobal.add("%s_%s_%s = %s" % (self.htmlId, self.selectedChartKey, self.selectedChartVal,
                                                 open(r"ares\json\%sData.json" % self.alias).read().strip()))