"""


"""

from ares.Lib.html import AresHtmlContainer


class NvD3HorizontalBars(AresHtmlContainer.Svg):
  """
  """
  alias, chartObject = 'horizBarChart', 'multiBarHorizontalChart'
  references = ['http://nvd3.org/examples/multiBarHorizontal.html']
  __chartStyle = {'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'margin': '{top: 30, right: 20, bottom: 50, left: 175}',
                  'showValues': 'true',
                  'showControls': 'true'
  }
  __chartProp = {
          'yAxis': {'tickFormat': "d3.format(',.2f')"}
  }
  # Required CSS and JS modules
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


  def dataFnc(self):
    """ """
    return '''
            [{key: 'test 1', values: [['A', 2.3], ['B', -10]]},
             {key: 'test 2', values: [['C', 12.3], ['D', -19]]}
            ]
           '''