"""


"""

from ares.Lib.html import AresHtmlContainer

class NvD3LineCumulative(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'lineCumulative', 'cumulativeLineChart'
  references = ['http://nvd3.org/examples/cumulativeLine.html']
  __chartStyle = {
    'x': 'function(d) { return d[0] }',
    'y': 'function(d) { return d[1]/100 }',
    'color': 'd3.scale.category10().range()',
    'useInteractiveGuideline': 'true',
  }

  __chartProp = {
    'xAxis': {'tickValues': "[1078030800000,1122782400000,1167541200000,1251691200000]", 'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }"},
    'yAxis': {'tickFormat': "d3.format(',.1%')"},
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