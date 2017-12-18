""" Chart module in charge of generating a Bar Chart
@author: Olivier Nogues

"""

from ares.Lib.html import AresHtmlGraphSvg


class XNvD3Bar(AresHtmlGraphSvg.XSvg):
  """ NVD3 Bar Chart python interface """
  alias, chartObject = 'bar', 'discreteBarChart'
  references = ['http://nvd3.org/examples/discreteBar.html']
  __chartStyle = {'showValues': 'true',
                  'staggerLabels': 'true',
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
  multiSeries = False

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.getData()
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    #self.click()
    dispatchChart = ["%s.discretebar.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
              %(chartDimension)s ;
              var chartData = [{key: %(seriesNames)s[0], values: [] } ];
              %(data)s.forEach(function(entry) {chartData[0].values.push({key: entry.key, value: entry.value}) });
              d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(chartData).call(%(htmlId)s); %(dispatchChart)s ;
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'], 'seriesNames': data['seriesNames'],
                   'chartProp': self.propToStr(), 'height': self.height, 'data': data['data'], 'dispatchChart': ";".join(dispatchChart)}

  def click(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = self.clickJsFnc

