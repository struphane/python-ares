"""

"""

import json
from ares.Lib.html import AresHtmlRadio
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3CandlestickBarChart(AresHtmlGraphSvg.Svg):
  """
  NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  alias, chartObject = 'candlestickbar', 'candlestickBarChart'
  references = []
  __chartStyle = {'x': "function(d) { return d['date'] }",
                  'y': "function(d) { return d['close'] }",
                  'margin': '{left: 75, bottom: 50}'
                  }

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
    dispatchChart = []
    for displathKey, jsFnc in self.dispatch.items():
      dispatchChart.append("%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc))
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

