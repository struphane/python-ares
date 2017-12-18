""" Chart module in charge of generating a Horizontal Chart
@author: Olivier Nogues

"""

import json
from ares.Lib.html import AresHtmlGraphSvgMulti
from ares.Lib.html import AresHtmlGraphSvg


class XNvD3HorizontalBars(AresHtmlGraphSvg.XSvg):
  alias, chartObject = 'horizBar', 'multiBarHorizontalChart'
  references = ['http://nvd3.org/examples/multiBarHorizontal.html',
                'http://python-nvd3.readthedocs.io/en/latest/classes-doc/multi-bar-horizontal-chart.html']
  __chartStyle = {'x': 'function(d) { return d.label }',
                  'y': 'function(d) { return d.value }',
                  'margin': '{top: 30, right: 20, bottom: 50, left: 175}',
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvgMulti.MultiSvg.colorCharts),
                  'showValues': 'true',
                  'showControls': 'true'
  }

  __chartProp = {
          'yAxis': {'tickFormat': "d3.format(',.2f')"}
  }
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  clickJsFnc = None
  multiSeries = True

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    #self.click()
    data = data if data is not None else self.getData()
    return '''
            %(chartDimension)s ;
            var seriesNames = %(seriesNames)s;
            var chartData = []; var itemsCount = 0 ;
            %(data)s.forEach(function(recordSet) {
              chartData.push( { key: seriesNames[itemsCount], values: [] } ) ; itemsCount++ ;
              eval(recordSet).forEach(function(entry) { chartData[itemsCount-1].values.push( { label: entry.key, value: entry.value } ) ;} );});
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(chartData).call(%(htmlId)s);
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'], 'seriesNames': data['seriesNames'],
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data['data']}