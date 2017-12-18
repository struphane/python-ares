""" Chart module in charge of generating a Line with Scatter Chart
@author: Olivier Nogues

"""

from ares.Lib.html import AresHtmlGraphSvg


class XNvD3ScatterChart(AresHtmlGraphSvg.XSvg):
  """ NVD3 Scatter Chart python interface """
  alias, chartObject = 'scatter', 'scatterChart'
  references = ['http://nvd3.org/examples/scatter.html']
  __chartStyle = {'showDistX': 'true',
                  'showDistY': 'true',
                  'x': 'function(d) { return d.label }',
                  'y': 'function(d) { return d.value }',
  }

  __chartProp = {
        #'xAxis': {'tickFormat': "d3.format('.02f')"},
        'yAxis': {'tickFormat': "d3.format('.02f')"},
  }

  # Required modules
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
    #self.mapxAxes(['cash', 'tab', 'visa'])
    # //var chartData = [ { key: '', values: [] } ];
    # //%(data)s.forEach(function(entry) {chartData[0].values.push({key: {'cash': 0, 'tab': 1, 'visa': 2}[entry.key], value: entry.value})});
    return '''
            %(chartDimension)s ;
            var seriesNames = %(seriesNames)s;
            var chartData = []; var itemsCount = 0 ;
            %(data)s.forEach(function(recordSet) {
              chartData.push( { key: seriesNames[itemsCount], values: [] } ) ; itemsCount++ ;
              eval(recordSet).forEach(function(entry) {chartData[itemsCount-1].values.push( { label: entry.key, value: entry.value } ) ;  } );});
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(chartData).call(%(htmlId)s);
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'], 'seriesNames': data['seriesNames'],
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data['data']}