""" Chart module in charge of generating a Line with Stacked with Focus AreaChart
@author: Olivier Nogues

"""

from ares.Lib.html import AresHtmlGraphSvg


class XNvD3StackedAreaWithFocus(AresHtmlGraphSvg.XSvg):
  alias, chartObject = 'stackedAreaWithFocus', 'stackedAreaWithFocusChart'
  references = ['http://nvd3.org/examples/stackedArea.html']
  __chartStyle = {'useInteractiveGuideline': 'true',
                  'x': 'function(d) { return d.label }',
                  'y': 'function(d) { return d.value }',
                  'controlLabels': '{stacked: "Stacked"}',
                  'duration': 'true',
                  'showControls': '300',
  }

  __chartProp = {
     #'xAxis': {'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }", 'showMaxMin': 'false'},
     #'x2Axis': {'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }"},
     #'xAxis': {'tickFormat': "d3.format(',.2f')"},
     #'x2Axis': {'tickFormat': "d3.format(',.2f')"},
     'yAxis': {'tickFormat': "d3.format(',.2f')"},
     'y2Axis': {'tickFormat': "d3.format(',.2f')"},
     'legend': {'vers': "'furious'"}
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  clickJsFnc = None
  multiSeries = True
  focus = True

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    if not self.focus:
      self.chartObject = 'stackedAreaChart'
    self.click()
    data = data if data is not None else self.getData()
    dispatchChart = ["%s.%s.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, self.chartObject, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
            %(chartDimension)s ;
            var seriesNames = %(seriesNames)s;
            var chartData = []; var itemsCount = 0 ;
            %(data)s.forEach(function(recordSet) {
              chartData.push( { key: seriesNames[itemsCount], values: [] } ) ; itemsCount++ ;
              eval(recordSet).forEach(function(entry) {chartData[itemsCount-1].values.push( { label: entry.key, value: entry.value } ) ;  } );});
            d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
            var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
            d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(chartData).call(%(htmlId)s); %(dispatchChart)s ;
            nv.utils.windowResize(%(htmlId)s.update);
           ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'], 'seriesNames': data['seriesNames'],
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data['data'], 'dispatchChart': ";".join(dispatchChart)}

  def click(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = self.clickJsFnc