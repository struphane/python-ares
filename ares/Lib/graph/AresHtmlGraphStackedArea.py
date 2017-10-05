"""

"""

from ares.Lib.html import AresHtmlContainer

class NvD3StackedArea(AresHtmlContainer.Svg):
  """ This object will output a simple stacked area chart

  Reference website: http://nvd3.org/examples/stackedArea.html
  """
  alias, chartObject = 'stackedAreaChart', 'multiBarChart'
  chartStyle = {'transitionDuration': 350,
                'reduceXTicks': 'true',
                'rotateLabels': 0,
                'showControls': 'true',
                'groupSpacing': 0.1
  }

  chartProp = {
     'xAxis': {'tickFormat': "d3.format(',f')"},
     'yAxis': {'tickFormat': "d3.format(',.1f'"},
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
    chartAttributes, chartProperties = [], []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.resolveProperties(chartProperties, self.chartProps, None)
    specialProperties = ['%s.%s;' % (self.htmlId, prop) for prop in chartProperties]
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        %s

        d3.select("#%s svg").datum(%s)
          .call(%s);
      ''' % (self.htmlId, self.chartObject, "\n.".join(chartAttributes), "\n".join(specialProperties),
             self.htmlId, self.dataFnc(), self.htmlId)
    )
