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
    return "eval('%s_' + %s + '_FIXED')" % (self.htmlId, self.dynKeySelection)

  def setVals(self, openCol, highCol, lowCol, closeCol, volumeCol, adjustedCol):
    """ Set a default value for the graph """
    self.chartVals = [openCol, highCol, lowCol, closeCol, volumeCol, adjustedCol]
    self.selectedChartVal = 'FIXED'

  def processData(self):
      """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
      recordSet = AresChartsService.toCandleStick(self.vals, self.chartKeys, *self.chartVals)
      for key, vals in recordSet.items():
        self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(vals)))

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

  def __str__(self):
    """ Return the svg container """
    self.processData()
    categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _ in self.chartKeys], cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {})
    categories.select(self.selectedChartKey)
    self.dynKeySelection = categories.val # The javascript representation of the radio
    self.dynValSelection = 'FIXED' # The javascript representation of the radio
    categories.click([self])
    self.htmlContent.append(str(categories))
    self.htmlContent.append('<div %s><svg style="width:100%%;height:400px;"></svg></div>' % self.strAttr())
    return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

  def processDataMock(self):
    """ Return the json data """
    self.chartKeys = [('MOCK', None)]
    self.selectedChartKey = 'MOCK'
    self.chartVals = [('FIXED', None)]
    self.selectedChartVal = self.chartVals[0][0]
    self.aresObj.jsGlobal.add("%s_%s_%s = %s" % (self.htmlId, self.selectedChartKey, self.selectedChartVal,
                                                 open(r"ares\json\%sData.json" % self.alias).read().strip()))