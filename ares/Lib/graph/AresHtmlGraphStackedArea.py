"""

"""

import json
from ares.Lib.html import AresHtmlContainer

class NvD3StackedArea(AresHtmlContainer.Svg):
  """ This object will output a simple stacked area chart

  Reference website: http://nvd3.org/examples/stackedArea.html
  """
  alias, chartObject = 'stackedAreaChart', 'multiBarChart'
  __chartStyle = {'transitionDuration': 350,
                  'reduceXTicks': 'true',
                  'rotateLabels': 0,
                  'showControls': 'true',
                  'groupSpacing': 0.1
  }

  __chartProp = {
     'xAxis': {'tickFormat': "d3.format(',f')"},
     'yAxis': {'tickFormat': "d3.format(',.1f'"},
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def dataFnc(self):
    """
    """
    return json.dumps(json.load(open(r"E:\GitHub\Ares\ares\json\stackedAreaData.json")))

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
