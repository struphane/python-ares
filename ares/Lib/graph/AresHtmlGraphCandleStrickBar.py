"""

"""

from ares.Lib.html import AresHtmlContainer


class NvD3CandlestickBarChart(AresHtmlContainer.Svg):
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
                  'duration': '250',
                  'margin': "{left: 75, bottom: 50}"}

  __chartProp = {
    'xAxis': {'axisLabel': '"Dates"', 'tickFormat': "function(d) {return d3.time.format('%x')(new Date(new Date() - (20000 * 86400000) + (d * 86400000)));}"},
    'yAxis': {'axisLabel': "'Stock Price", 'tickFormat': "function(d,i){ return '$' + d3.format(',.1f')(d); }"}
  }
  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s().%s ;

        d3.select("#%s svg").datum(%s)%s.call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(),
             self.htmlId, self.dataFnc(), self.getSvg(), self.htmlId, self.htmlId)
    )
