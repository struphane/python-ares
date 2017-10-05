"""


"""

from ares.Lib.html import AresHtmlContainer


class NvD3ScatterChart(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'scatter', 'scatterChart'
  references = ['http://nvd3.org/examples/scatter.html']
  __chartStyle = {'showDistX': 'true',
                  'showDistY': 'true',
                  'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'transitionDuration': 350,
                  'color': 'd3.scale.category10().range()',
  }

  __chartProp = {
        'tooltipContent': "function(key) {return '<h3>' + key + '</h3>' ;}",
        'xAxis': {'tickFormat': "d3.format('.02f')"},
        'yAxis': {'tickFormat': "d3.format('.02f')"},
        'scatter': {'onlyCircles': 'false'}
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

        d3.select("#%s svg").datum(%s).call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(), self.htmlId, self.htmlId)
    )

