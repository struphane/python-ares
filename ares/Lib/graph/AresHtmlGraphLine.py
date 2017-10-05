"""


"""

from ares.Lib.html import AresHtmlContainer

class NvD3Line(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'line', 'lineChart'
  references = ['http://nvd3.org/examples/line.html']
  __chartStyle = {
    'margin': '{left: 100}',
    'transitionDuration': '350',
    'showLegend': 'true',
    'showYAxis': 'true',
    'showXAxis': 'true'

  }

  __chartProp = {
    'xAxis': {'axisLabel': "'Time (ms)'", 'tickFormat': "d3.format(',r')"},
    'yAxis': {'axisLabel': "'Voltage (v)'", 'tickFormat': "d3.format('.02f')"},
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

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
             self.htmlId, self.dataFnc(), self.htmlId, self.htmlId)
    )