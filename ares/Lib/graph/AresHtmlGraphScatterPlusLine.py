"""


"""

from ares.Lib.html import AresHtmlContainer


class NvD3ScatterPlusLineChart(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'scatterPlusLine', 'scatterChart'
  references = ['']
  __chartStyle = {'showDistX': 'true',
                  'showDistY': 'true',
                  'duration': '300',
                  'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'color': 'd3.scale.category10().range()',
  }

  __chartProp = {
        'xAxis': {'tickFormat': "d3.format('.02f')"},
        'yAxis': {'tickFormat': "d3.format('.02f')"},
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        %s

        d3.select("#%s svg").datum(nv.log(%s)).call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(), self.htmlId, self.htmlId)
    )

