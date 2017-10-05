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
    'x': "function(d) { return d[0]; }",
    'y': "function(d) { return d[1]; }"
  }

  __svgProp = {
    'transition': '',
  }


  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartAttr = ".%s" % self.attrToStr() if  self.attrToStr() != '' else ''
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()%s;

        %s

        d3.select("#%s svg").datum(%s)%s.call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, chartAttr, self.propToStr(),
             self.htmlId, self.dataFnc(), self.getSvg(), self.htmlId, self.htmlId)
    )