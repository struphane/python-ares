"""


"""

from ares.Lib.html import AresHtmlContainer

class NvD3MultiBars(AresHtmlContainer.Svg):
  """

  """
  alias, chartObject = 'multiBar', 'multiBarChart'
  references = ['http://nvd3.org/examples/multiBar.html']
  __chartStyle = {'transitionDuration': '350',
                  'reduceXTicks': 'true',
                  'rotateLabels': '0',
                  'showControls': 'true',
                  'groupSpacing': '0.1',
                  }

  __chartProp = {
      'xAxis': {'tickFormat': "d3.format(',f')"},
      'yAxis': {'tickFormat': "d3.format(',.1f')"}
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