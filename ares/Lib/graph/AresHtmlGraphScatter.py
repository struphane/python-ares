"""


"""

from ares.Lib.html import AresHtmlContainer


class NvD3ScatterChart(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'scatterChart', 'scatterChart'
  __chartStyle = {'showDistX': 'true',
                'showDistY': 'true',
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

  def dataFnc(self):
    """
    """
    return '''[{key: 'test', values: [{x: 1.4, y: 2.3}]}] '''

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        %s

        d3.select("#%s svg").datum(%s)
          .call(%s);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
             self.htmlId, self.dataFnc(), self.htmlId)
    )

