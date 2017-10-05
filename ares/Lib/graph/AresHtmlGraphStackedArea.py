"""

"""

import json
from ares.Lib.html import AresHtmlContainer

class NvD3StackedArea(AresHtmlContainer.Svg):
  """ This object will output a simple stacked area chart

  """
  alias, chartObject = 'stackedArea', 'stackedAreaChart'
  references = ['http://nvd3.org/examples/stackedArea.html']
  __chartStyle = {'margin': '{right: 100}',
                  'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'useInteractiveGuideline': 'true',
                  'rightAlignYAxis': 'true',
                  'transitionDuration': '500',
                  'showControls': 'true',
                  'clipEdge': 'true',
  }

  __chartProp = {
     'xAxis': {'tickFormat': "function(d) { return d3.time.format('%x')( new Date(d) ) }", 'showMaxMin': 'false'},
     'yAxis': {'tickFormat': "d3.format(',.2f')"},
     #'zoom': {'enabled': 'true', 'scaleExtent': '[1,10]', 'useFixedDomain': 'false', 'useNiceScale': 'false',
     #         'horizontalOff': 'false', 'verticalOff': 'true', 'unzoomEventType': '"dblclick.zoom"'}
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
