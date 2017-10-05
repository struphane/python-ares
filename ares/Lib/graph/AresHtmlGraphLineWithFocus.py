"""


"""

from ares.Lib.html import AresHtmlContainer

class NvD3LineWithFocus(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'lineChartFocus', 'lineWithFocusChart'
  references = ['http://nvd3.org/examples/lineWithFocus.html']
  __chartProp = {
    'xAxis': {'tickFormat': "d3.format(',f')"},
    'yAxis': {'tickFormat': "d3.format(',.2f')"},
    'y2Axis': {'tickFormat': "d3.format(',.2f')"},
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
      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(), self.htmlId)
    )