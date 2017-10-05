"""

"""

from ares.Lib.html import AresHtmlContainer
from ares.Lib import AresItem


class NvD3Donut(AresHtmlContainer.Svg):
  """
  NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  alias, chartObject = 'donut', 'pieChart'
  chartStyle = {'showLabels': 'true',
                'labelThreshold': .05,
                'labelType': '"percent"',
                'donut': 'true',
                'donutRatio': 0.35,
                'x': "function(d) { return d[0]; }",
                'y': "function(d) { return d[1]; }"}

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def dataFnc(self):
    """ Return the data Source converted to them be sent to the javascript layer """
    return "getDataFromRecordSet(%s, ['%s', '%s'])" % (self.jqRecordSet, 'PTF', 'VAL')

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        d3.select("#%s svg").datum(%s)
            .%s
            .call(%s);
      ''' % (self.htmlId, self.chartObject, "\n.".join(chartAttributes),
             self.htmlId, self.dataFnc(), self.getSvg(), self.htmlId)
    )
