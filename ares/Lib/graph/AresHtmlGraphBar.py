""" Chart module in charge of generating a Bar Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3Bar(AresHtmlGraphSvg.Svg):
  """ NVD3 Bar Chart python interface """
  alias, chartObject = 'bar', 'discreteBarChart'
  references = ['http://nvd3.org/examples/discreteBar.html']
  __chartStyle = {'showValues': 'true',
                  'staggerLabels': 'true',
                  'x': "function(d) { return d[0]; }",
                  'y': "function(d) { return d[1]; }"}
  # Required external modules (javascript and CSS
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  seriesName = '' # User to remap the key from the recordset in the final display

  __chartProp = {
    #'xAxis': {'tickFormat': "d3.format(',r')"}, # 'axisLabel': "'Time (ms)'",
    #'yAxis': {'tickFormat': "d3.format('.02f')"}, # 'axisLabel': "'Voltage (v)'"
  }

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toBar(self.vals,self.seriesName, self.chartKeys, self.chartVals, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def showLegend(self, boolFlag):
    """ Change the D3 flag to display the legend in the chart """
    if boolFlag:
      self.addChartProp('showLegend', 'true')
    else:
      self.addChartProp('showLegend', 'false')

  def showValues(self, boolFlag):
    """ Change the D3 flag to display the legend in the chart """
    if boolFlag:
      self.addChartProp('showValues', 'true')
    else:
      self.addChartProp('showValues', 'false')

  def outSideLabels(self, boolFlag):
    """ Change the flag to display the labels of teh chart outside """
    if boolFlag:
      self.addChartProp('showLabels', 'true')
      self.addChartProp('labelsOutside', 'true')
    else:
      self.addChartProp('labelsOutside', 'false')

  def changeColor(self, rangeColors):
    """ Change the default colors in the chart """
    self.addChartProp('color', 'd3.scale.ordinal().range(%s).range()' % json.dumps(rangeColors))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    # Dispatch method to add events on the chart (in progress)
    dispatchChart = ["%s.discretebar.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
              d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s).call(%(htmlId)s); %(dispatchChart)s ;
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(),
                   'chartProp': self.propToStr(), 'height': self.height, 'data': data, 'dispatchChart': ";".join(dispatchChart)}

  def click(self, jsFnc):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = jsFnc

  def clickIndex(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = "alert(e.index)"

  def clickPoint(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = "alert(e.data)"