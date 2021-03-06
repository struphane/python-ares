""" Chart module in charge of generating a Candle Stick Bar Chart
@author: Olivier Nogues

"""
#TODO Migrate to the new Chart framework

import json
from ares.Lib.html import AresHtmlRadio
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg
from ares.Lib.html import AresHtmlContainer


class NvD3CandlestickBarChart(AresHtmlGraphSvg.Svg):
  """ NVD3 Candle Chart Stick bar Chart python interface """
  alias, chartObject = 'candlestickbar', 'candlestickBarChart'
  references = ['http://krispo.github.io/angular-nvd3/#/candlestickBarChart']
  __chartStyle = {'x': "function(d) { return d['date'] }",
                  'y': "function(d) { return d['close'] }",
                  'margin': '{left: 75, bottom: 50}'}

  __chartProp = {
      'xAxis': {'axisLabel': '"Dates"', 'tickFormat': "function(d) {return d3.time.format('%x')(new Date(new Date() - (20000 * 86400000) + (d * 86400000)));}"},
      'yAxis': {'axisLabel': "'Stock Price", 'tickFormat': "function(d,i){ return '$' + d3.format(',.1f')(d); }"}
  }
  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  @property
  def jqData(self):
    """ Returns the javascript SVG reference """
    return "data_%s[ %s + '_FIXED']" % (self.htmlId, self.categories.val)

  def processData(self):
      """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
      recordSet = AresChartsService.toCandleStick(self.vals, self.chartKeys, *self.chartVals)
      self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    return '''
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ;
              d3.select("#%(htmlId)s svg").datum(%(data)s)%(svgProp)s.call(%(htmlId)s);
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(),
                   'data': data, 'svgProp': self.getSvg()}

  def __str__(self):
    """ Return the svg container """
    self.processData()
    self.categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _ in self.chartKeys], cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {}, checked=self.selectedChartKey)
    self.categories.click([self])

    self.htmlContent.append(str(self.categories))
    self.htmlContent.append('<div %s><svg style="width:100%%;height:400px;"></svg></div>' % self.strAttr())
    if self.headerBox:
      return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

    return "\n".join(self.htmlContent)

  def processDataMock(self):
    """ Return the json data """
    self.chartKeys = [('MOCK', None)]
    self.selectedChartKey = 'MOCK'
    self.aresObj.jsGlobal.add("data_%s = {'%s': %s}" % (self.htmlId, self.selectedChartKey,
                                                        open(r"ares\json\%sData.json" % self.alias).read().strip()))