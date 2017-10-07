"""


"""

from ares.Lib.html import AresHtmlContainer

class NvD3SparkLinePlus(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'sparklineplus', 'sparklinePlus'
  references = ['http://nvd3.org/examples/line.html']
  __chartStyle = {
    'margin': '{left:70}',
    'x': 'function(d,i) { return i }',
    'showLastValue': 'true',
    'showLastValue': "function(d) {return d3.time.format('%x')(new Date(data[d].x))}",
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