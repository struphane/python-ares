""" Chart module in charge of generating a Parallel Cordinates Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlRadio
from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlGraphSvg

import re
regex = re.compile('[^a-zA-Z0-9_]')

class NvD3ParallelCoordinates(AresHtmlGraphSvg.Svg):
  """ NVD3 Venn Chart python interface """
  alias, chartObject = 'parallelc', 'parallelCoordinatesChart'
  references = ['https://bl.ocks.org/jasondavies/1341281']
  __chartStyle = {'displayBrush': "false", 'lineTension': 0.8}

  __svgProp = {
  }

  __chartProp = {
  }
  height = 200

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toVenn(self.vals, self.chartKeys[0], self.chartKeys[1], self.chartVals, extKeys=self.extKeys)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, regex.sub('', key.strip()), json.dumps(vals)))

  def brushEnd(self):
    """  """
    self.dispatch('brushEnd', "function (e) {d3.select('#resetBrushButton').style('visibility', 'visible');}")

  def dimensionsOrder(self,):
    """  """
    self.dispatch('dimensionsOrder', "function (e, b) {if (b) { d3.select('#resetSortingButton').style('visibility', 'visible');}}")

  def jsUpdate(self):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    return '''
              var dim = dimensions();
              chart = nv.models.%s().%s;
              d3.select('#test').datum(mydata()).call(chart);
              nv.utils.windowResize(chart.update);

              // update chart data values randomly
              setInterval(function () { data[0].values.P1 = Math.floor(Math.random() * 100); chart.update();}, 4000);

              // update chart data dimension randomly
              setInterval(function () {
                  var element = {key: "P7", format: d3.format("p"), tooltip: "year",}
                  if (dim.length === 7) {dim.splice(dim.indexOf(element), 1);}
                  else {dim.push(element);}
                  chart.dimensionData(dim);
                  chart.update();
              }, 10000);

           '''

  def __str__(self):
    """ Return the svg container """
    self.processData()
    categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _, _ in self.chartKeys], cssAttr={'display': 'None'} if len(self.chartKeys) == 2 else {}, internalRef='key_%s' % self.htmlId)
    categories.select(self.selectedChartKey)
    self.dynKeySelection = categories.val # The javascript representation of the radio
    values = AresHtmlRadio.Radio(self.aresObj, [val for val, _, _ in self.chartVals], cssAttr={'display': 'None'} if len(self.chartVals) == 1 else {}, internalRef='val_%s' % self.htmlId)
    values.select(self.selectedChartVal)
    self.dynValSelection = values.val # The javascript representation of the radio

    categories.click([self])
    values.click([self])

    self.htmlContent.append(str(categories))
    self.htmlContent.append(str(values))
    self.htmlContent.append('<div %s></div>' % self.strAttr())
    return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))