"""

"""

import json
from ares.Lib.html import AresHtmlContainer

class NvD3StackedAreaWithFocus(AresHtmlContainer.Svg):
  """ This object will output a simple stacked area chart

  """
  alias, chartObject = 'stackedAreaWithFocus', 'stackedAreaWithFocusChart'
  references = ['http://nvd3.org/examples/stackedArea.html']
  __chartStyle = {'useInteractiveGuideline': 'true',
                  'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'controlLabels': '{stacked: "Stacked"}',
                  'duration': 'true',
                  'showControls': '300',
  }

  __chartProp = {
     'xAxis': {'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }", 'showMaxMin': 'false'},
     'x2Axis': {'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }"},
     'yAxis': {'tickFormat': "d3.format(',.2f')"},
     'y2Axis': {'tickFormat': "d3.format(',.2f')"},
     'legend': {'vers': "'furious'"}
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
