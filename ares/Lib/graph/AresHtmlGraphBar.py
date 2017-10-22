"""

"""

from Libs import AresChartsService
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
                  'x': "function(d) { return d[0]; }",
                  'y': "function(d) { return d[1]; }"}
  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  seriesName = ''

  def dataFnc(self, cat, val):
    """ Return the json data """
    return AresChartsService.toBar(self.vals, self.seriesName, cat, val)

  def setKeys(self, keys, selected=None):
    """ Set a default key for the graph """
    if len(keys) == 1:
      self.selectedCat = keys[0]
      self.dfltCat = keys[0]
      self.multiCat = False
    else:
      if selected is None:
        raise Exception("A selected category should be defined")

      self.selectedCat = selected
      self.multiCat = keys
      self.dfltCat = selected

  def setVals(self, vals, selected=None):
    """ Set a default value for the graph """
    if len(vals) == 1:
      self.selectedVal = vals[0]
      self.multiVal = False
      self.dfltVal = vals[0]
    else:
      if selected is None:
        raise Exception("A selected value should be defined")

      self.selectedVal = selected
      self.multiVal = vals
      self.dfltVal = selected

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(
      '''
        var %s = nv.models.%s().%s ;

        d3.select("#%s svg").datum(%s).call(%s);

        nv.utils.windowResize(%s.update);
      ''' % (self.htmlId, self.chartObject, self.attrToStr(),
             self.htmlId, self.dataFnc(self.selectedCat, self.selectedVal), self.htmlId, self.htmlId)
    )

