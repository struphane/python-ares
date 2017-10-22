"""


"""

from Libs import AresChartsService
from ares.Lib.html import AresHtmlContainer

class NvD3Line(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'line', 'lineChart'
  references = ['http://nvd3.org/examples/line.html']
  __chartStyle = {
    'margin': '{left: 100}',
    'showLegend': 'true',
    'showYAxis': 'true',
    'showXAxis': 'true',
    'x': "function(d) { return d[0]; }",
    'y': "function(d) { return d[1]; }"

  }
  seriesName = ''
  __chartProp = {
    #'xAxis': {'tickFormat': "d3.format(',r')"}, # 'axisLabel': "'Time (ms)'",
    #'yAxis': {'tickFormat': "d3.format('.02f')"}, # 'axisLabel': "'Voltage (v)'"
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def dataFnc(self, cat, val):
    """ Return the json data """
    return AresChartsService.toBar(self.vals, self.seriesName, cat, val, isXDt='%Y-%m-%d')

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        %s

        d3.select("#%s svg").datum(%s).call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(self.selectedCat, self.selectedVal), self.htmlId, self.htmlId)
    )