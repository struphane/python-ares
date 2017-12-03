""" Generic underlying module for the multidimentional D3 charts
@author: Olivier Nogues

"""

import json
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

  @property
  def jqData(self):
    """ Returns the javascript SVG reference """
    if self.components:
      dataComp = "+ '_' + ".join([comp.val for comp in self.components])
      return "eval('%s_' + %s + '_' + %s + '_' + %s)" % (self.htmlId, dataComp, self.dynKeySelection, self.dynValSelection)

    return "eval('%s_' + %s + '_' + %s)" % (self.htmlId, self.dynKeySelection, self.dynValSelection)

  def __str__(self):
    """ Return the svg container """
    self.processData()
    categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _, _ in self.chartKeys], cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {})
    categories.select(self.selectedChartKey)
    self.dynKeySelection = categories.val # The javascript representation of the radio
    values = AresHtmlRadio.Radio(self.aresObj, [val for val, _, _ in self.chartVals], cssAttr={'display': 'None'} if len(self.chartVals) == 1 else {})
    values.select(self.selectedChartVal)
    self.dynValSelection = values.val # The javascript representation of the radio
    categories.click([self])
    values.click([self])

    self.htmlContent.append(str(categories))
    self.htmlContent.append(str(values))
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