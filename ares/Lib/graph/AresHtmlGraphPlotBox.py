"""

"""

from ares.Lib.html import AresHtmlContainer


class NvD3PlotBox(AresHtmlContainer.Svg):
  """
  NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  alias, chartObject = 'boxplot', 'boxPlotChart'
  references = ['http://nvd3.org/examples/pie.html']
  __chartStyle = {'x': "function(d) { return d.label }",
                  'maxBoxWidth': '75',
                  'yDomain': '[0, 500]',
                  'staggerLabels': "true"}

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s().%s ;

        d3.select("#%s svg").datum(%s)%s.call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(),
             self.htmlId, self.dataFnc(), self.getSvg(), self.htmlId, self.htmlId)
    )
