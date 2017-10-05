"""

"""

from ares.Lib.html import AresHtmlContainer
from ares.Lib import AresItem


class NvD3Pie(AresHtmlContainer.Svg):
  """
  NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  alias = 'pie'

  chartStyle = {'showLabels': 'true',
                'x': "function(d) { return d[0]; }",
                'y': "function(d) { return d[1]; }"}
  chartObject = 'pieChart'

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def dataFnc(self):
    """ Return the data Source converted to them be sent to the javascript layer """
    return "getDataFromRecordSet(%s, ['%s', '%s'])" % (self.jqRecordSet, 'PTF', 'VAL')

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartProperties = []
    self.resolveProperties(chartProperties, self.chartProp, None)
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        d3.select("#%s svg").datum(%s)
          .%s
          .call(%s);

      ''' % (self.htmlId, self.chartObject, "\n.".join(chartProperties),
             self.htmlId, self.dataFnc(), self.getSvg(), self.htmlId)
    )
