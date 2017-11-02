""" Chart module in charge of generating a Bar Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg

import re
regex = re.compile('[^a-zA-Z0-9_]')

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
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, regex.sub('', key.strip()), json.dumps(vals)))

  def showLeged(self, boolFlag):
    """ Change the D3 flag to display the legend in the chart """
    if boolFlag:
      self.addChartProp('showLegend', 'true')
    else:
      self.addChartProp('showLegend', 'false')

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

  def jsUpdate(self):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
              d3.select("#%s svg").remove();
              d3.select("#%s").append("svg");
              var %s = nv.models.%s().%s ;
              %s
              d3.select("#%s svg").style("height", '%spx').datum(%s).call(%s);
              nv.utils.windowResize(%s.update);
            ''' % (self.htmlId, self.htmlId, self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
                   self.htmlId, self.height, self.jqData, self.htmlId, self.htmlId)


