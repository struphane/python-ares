""" Chart module in charge of generating a Line with Scatter Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvgMulti
from ares.Lib.html import AresHtmlGraphSvg

class NvD3ScatterChart(AresHtmlGraphSvgMulti.MultiSvg):
  """ NVD3 Scatter Chart python interface """
  alias, chartObject = 'scatter', 'scatterChart'
  references = ['http://nvd3.org/examples/scatter.html']
  __chartStyle = {'showDistX': 'true',
                  'showDistY': 'true',
                  'x': 'function(d) { return d[0] }',
                  'y': 'function(d) { return d[1] }',
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvgMulti.MultiSvg.colorCharts),
  }

  __chartProp = {
        'xAxis': {'tickFormat': "d3.format('.02f')"},
        'yAxis': {'tickFormat': "d3.format('.02f')"},
  }

  # Required modules
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


class XNvD3ScatterChart(AresHtmlGraphSvg.XSvg):
  """ NVD3 Scatter Chart python interface """
  alias, chartObject = 'scatter', 'scatterChart'
  references = ['http://nvd3.org/examples/scatter.html']
  __chartStyle = {'showDistX': 'true',
                  'showDistY': 'true',
                  'x': 'function(d) { return d.key }',
                  'y': 'function(d) { return d.value }',
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvgMulti.MultiSvg.colorCharts[5:]),
  }

  __chartProp = {
        #'xAxis': {'tickFormat': "d3.format('.02f')"},
        'yAxis': {'tickFormat': "d3.format('.02f')"},
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  clickJsFnc = None

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    #self.click()
    data = data if data is not None else self.jqData
    self.mapxAxes(['cash', 'tab', 'visa'])
    return '''
            %(chartDimension)s ;
            var chartData = [ { key: '', values: [] } ];
            %(data)s.forEach(function(entry) {chartData[0].values.push({key: {'cash': 0, 'tab': 1, 'visa': 2}[entry.key], value: entry.value})});
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(chartData).call(%(htmlId)s);
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'],
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data['data']}