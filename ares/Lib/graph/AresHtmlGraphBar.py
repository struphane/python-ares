"""

"""

from ares.Lib.html import AresHtmlContainer


class NvD3Bar(AresHtmlContainer.Svg):
  """

  data format expected in the graph:
    [{key: "Cumulative Return", values: [{ "label": "One","value" : 29.765957771107},  {"label": "Four", "value" : 196.45946739256}]}]
  """
  alias, chartObject = 'bar', 'discreteBarChart'
  references = ['http://nvd3.org/examples/discreteBar.html']
  __chartStyle = {'showValues': 'true',
                'staggerLabels': 'true',
                'transitionDuration': 350,
                'x': "function(d) { return d[0]; }",
                'y': "function(d) { return d[1]; }"}
  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def dataFnc(self):
    """
    """
    return '''
            [
            {
              key: "Cumulative Return",
              values: [
                  ["A Label" , -29.765957771107],
                  ["B Label" , -9.765957771107]
              ]
            },
            {
              key: "Cumulative Test",
              values: [
                  ["A Label" , 29.765957771107],
                  ["B Label" , 9.765957771107]
              ]
            }
          ]
           '''


  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s()
            .%s ;

        d3.select("#%s svg").datum(%s)
          .call(%s);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(),
             self.htmlId, self.dataFnc(), self.htmlId)
    )

