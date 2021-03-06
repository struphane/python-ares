""" Chart module in charge of generating a Line Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvgMulti
from ares.Lib.html import AresHtmlGraphSvg


class NvD3Line(AresHtmlGraphSvgMulti.MultiSvg):
  """ NVD3 Line bar Chart python interface """
  alias, chartObject = 'line', 'lineChart'
  references = ['http://nvd3.org/examples/line.html',
                'https://stackoverflow.com/questions/23727627/nvd3-line-chart-with-string-values-on-x-axis']
  __chartStyle = {
    'margin': '{left: 100}',
    'showLegend': 'true',
    'showYAxis': 'true',
    'showXAxis': 'true',
    'x': "function(d) { return d[0]; }",
    'y': "function(d) { return d[1]; }"

  }

  __chartProp = {
    #'xAxis': {'tickFormat': "d3.format(',r')"}, # 'axisLabel': "'Time (ms)'",
    #'yAxis': {'tickFormat': "d3.format('.02f')"}, # 'axisLabel': "'Voltage (v)'"
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toMultiSeries(self.vals, self.chartKeys, self.selectedX , self.chartVals, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    return '''
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s).call(%(htmlId)s);
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(),
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data}


class XNvD3Line(AresHtmlGraphSvg.XSvg):
  alias, chartObject = 'line', 'lineChart'
  references = ['http://nvd3.org/examples/line.html',
                'https://stackoverflow.com/questions/23727627/nvd3-line-chart-with-string-values-on-x-axis']
  __chartStyle = {
    'margin': '{left: 100}',
    'showLegend': 'true',
    'showYAxis': 'true',
    'showXAxis': 'true',
    'x': "function(d) { return d.key; }",
    'y': "function(d) { return d.value; }",
    'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvgMulti.MultiSvg.colorCharts[::-1]),
  }

  __chartProp = {
    #'xAxis': {'tickFormat': "d3.format(',r')"}, # 'axisLabel': "'Time (ms)'",
    #'yAxis': {'tickFormat': "d3.format('.02f')"}, # 'axisLabel': "'Voltage (v)'"
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    dispatchChart = ["%s.multibar.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
            %(chartDimension)s ;
            var chartData = [ { key: '', values: [] } ];
            %(data)s.map(function(element, index) {chartData[0].values.push( { key: index, value: element.value  } ) } ) ;
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(chartData).call(%(htmlId)s); %(dispatchChart)s ;
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'],
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data['data'], 'dispatchChart': ";".join(dispatchChart)}

  def click(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = self.clickJsFnc