""" Generic underlying module for the multidimentional D3 charts
@author: Olivier Nogues

"""

import json
from ares.Lib import AresHtml
from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlRadio
from ares.Lib.html import AresHtmlGraphSvg

class MultiSvg(AresHtmlGraphSvg.Svg):
  """
  """

  def setSeries(self, series, selected=None):
    """ """
    self.setKeys(series, selected)

  def setY(self, series, selected=None):
    """ """
    self.setVals(series, selected)

  def setX(self, x):
    """ """
    self.selectedX = self.header[x]

  def setXOrder(self, xValsList):
    """ For the order on the abscisse """
    self.addChartProp('xAxis', {'tickValues': [i for i in range(len(xValsList))]})
    self.addChartProp('xAxis', {'tickFormat': "function(d){ return %s[d] }" % json.dumps(xValsList)})

  def setExtVals(self, keys, components):
    """ Link the result to the different components on the page """
    self.extKeys = keys
    self.components = components

  def xAxisAsDate(self):
    """ Force the x axis to be a date """
    self.addChartProp('xAxis', {'tickFormat': "function(d) { return d3.time.format('%Y/%m/%d')(new Date(d)) }"})

  def __str__(self):
    """ Return the svg container """
    self.processData()
    self.categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _, _ in self.chartKeys],
                                          cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {}, checked=self.selectedChartKey)
    self.values = AresHtmlRadio.Radio(self.aresObj, [val for val, _, _ in self.chartVals],
                                      cssAttr={'display': 'None'} if len(self.chartVals) == 1 else {}, checked=self.selectedChartVal)
    self.categories.click([self])
    self.values.click([self])

    self.htmlContent.append(str(self.categories))
    self.htmlContent.append(str(self.values))
    self.htmlContent.append('<div %s style="height:%spx;"><svg style="width:100%%;height:%spx;"></svg></div>' % (self.strAttr(), self.height, self.height))
    if self.headerBox:
      return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

    return "\n".join(self.htmlContent)


  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(self.jsUpdate())
    for comp in self.components:
      comp.link(self.jsUpdate())