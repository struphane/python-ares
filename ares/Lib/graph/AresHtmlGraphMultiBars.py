""" Chart module in charge of generating a Multi Bar Chart
@author: Olivier Nogues

"""

import json

from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvgMulti
from ares.Lib.html import AresHtmlGraphSvg


class XNvD3MultiBars(AresHtmlGraphSvg.XSvg):
  """

  """
  alias, chartObject = 'multiBar', 'multiBarChart'
  references = ['http://nvd3.org/examples/multiBar.html']
  __chartStyle = {'x': 'function(d) { return d.label }',
                  'y': 'function(d) { return d.value }',
                  'reduceXTicks': 'true',
                  'rotateLabels': '0',
                  'showControls': 'true',
                  'groupSpacing': '0.1',
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvg.XSvg.colorCharts),
                  }

  __chartProp = {
      'xAxis': {'tickFormat': "d3.format(',f')"},
      'yAxis': {'tickFormat': "d3.format(',.1f')"}
  }
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  clickJsFnc = None
  multiSeries = True

  def xtimstamps(self):
    """

    :return:
    """
    self.addChartAttr({'reduceXTicks': 'false'})
    self.delChartProp(['xAxis'])
    self.addChartProp('xAxis', {'ticks(5).tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }"})

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    # self.click()
    data = data if data is not None else self.getData()
    dispatchChart = ["%s.multibar.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
            %(chartDimension)s ;
            var seriesNames = %(seriesNames)s;
            var chartData = []; var itemsCount = 0 ;
            %(data)s.forEach(function(recordSet) {
              chartData.push( { key: seriesNames[itemsCount], values: [] } ) ; itemsCount++ ;
              eval(recordSet).forEach(function(entry) { chartData[itemsCount-1].values.push( { label: entry.key, value: entry.value } ) ;} );});
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(chartData).call(%(htmlId)s); %(dispatchChart)s ;
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'], 'seriesNames': data['seriesNames'],
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data['data'], 'dispatchChart': ";".join(dispatchChart) }

  def click(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = self.clickJsFnc