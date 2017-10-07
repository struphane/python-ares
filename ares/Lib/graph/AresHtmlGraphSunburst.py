"""


"""

from ares.Lib.html import AresHtmlContainer

class NvD3Sunburst(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'sunburst', 'sunburstChart'
  references = ['http://nvd3.org/examples/line.html']
  __chartStyle = {
    'color': 'd3.scale.category20c()',
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