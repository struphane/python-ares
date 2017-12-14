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
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvg.Svg.colorCharts),
                  'x': "function(d) { return d.key; }",
                  'y': "function(d) { return d.value; }"}
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

class XNvD3Bar(AresHtmlGraphSvg.XSvg):
  """ NVD3 Bar Chart python interface """
  alias, chartObject = 'bar', 'discreteBarChart'
  references = ['http://nvd3.org/examples/discreteBar.html']
  __chartStyle = {'showValues': 'true',
                  'staggerLabels': 'true',
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvg.Svg.colorCharts),
                  'x': "function(d) { return d.key; }",
                  'y': "function(d) { return d.value; }"}
  # Required external modules (javascript and CSS
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  seriesName = '' # User to remap the key from the recordset in the final display

  __chartProp = {
    #'xAxis': {'tickFormat': "d3.format(',r')"}, # 'axisLabel': "'Time (ms)'",
    #'yAxis': {'tickFormat': "d3.format('.02f')"}, # 'axisLabel': "'Voltage (v)'"
  }

  clickJsFnc = None

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    #self.click()
    dispatchChart = ["%s.discretebar.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
              %(chartDimension)s ;
              var chartData = [{key: '', values: [] } ];
              %(data)s.forEach(function(entry) {
                chartData[0].values.push({key: entry.key, value: entry.value})
              });
              d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(chartData).call(%(htmlId)s); %(dispatchChart)s ;
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'],
                   'chartProp': self.propToStr(), 'height': self.height, 'data': data['data'], 'dispatchChart': ";".join(dispatchChart)}

  def click(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = self.clickJsFnc

