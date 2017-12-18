""" Chart module in charge of generating a Pie Chart
@author: Olivier Nogues

"""

from ares.Lib.html import AresHtmlGraphSvg


class XNvD3Pie(AresHtmlGraphSvg.XSvg):
  """ NVD3 Pie Chart python interface """
  alias, chartObject = 'pie', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html',
                'https://bl.ocks.org/mbostock/3887235',
                'http://bl.ocks.org/enjalot/1203641',
                'https://stackoverflow.com/questions/16191542/how-to-customize-color-in-pie-chart-of-nvd3']
  __chartStyle = {'showLabels': 'true',
                  'x': "function(d) { return d.key; }",
                  'y': "function(d) { return d.value; }"}

  __svgProp = {
    'transition': '',
  }

  __chartProp = {
  #  'pie': {'startAngle': 'function(d) { return d.startAngle/2 -Math.PI/2 }',
  #          'endAngle': 'function(d) { return d.endAngle/2 -Math.PI/2 }'}
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  clickJsFnc = None

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    data = data if data is not None else self.getData()
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    #self.click()
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    #dispatchChart.append("%s.legend.dispatch.on('stateChange.pie', function(d){ d.disabled ; alert(%s.legend); } )" % (self.htmlId, self.htmlId))
    return '''
              %(chartDimension)s ;
              d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s)%(svgProp)s.call(%(htmlId)s); %(dispatchChart)s ;
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'],
                   'chartProp': self.propToStr(), 'height': self.height, 'data': data['data'], 'svgProp': self.getSvg(),
                   'dispatchChart': ";".join(dispatchChart)}

  def click(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = self.clickJsFnc


class XNvD3Donut(AresHtmlGraphSvg.XSvg):
  """ NVD3 Pie Chart python interface """
  alias, chartObject = 'donut', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html']

  __chartStyle = {'showLabels': 'true',
                  'labelThreshold': .05,
                  'labelType': '"percent"',
                  'donut': 'true',
                  'donutRatio': 0.35,
                  'x': "function(d) { return d.key; }",
                  'y': "function(d) { return d.value; }"}

  __svgProp = {
    'transition': '',
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  clickJsFnc = None

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    data = data if data is not None else self.getData()
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    #self.click()
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    #dispatchChart.append("%s.legend.dispatch.on('stateChange.pie', function(d){ d.disabled ; alert(%s.legend); } )" % (self.htmlId, self.htmlId))
    return '''
              %(chartDimension)s ;
              d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s)%(svgProp)s.call(%(htmlId)s); %(dispatchChart)s ;
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'],
                   'chartProp': self.propToStr(), 'height': self.height, 'data': data['data'], 'svgProp': self.getSvg(),
                   'dispatchChart': ";".join(dispatchChart)}

  def click(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = self.clickJsFnc


class XNvD3Meter(AresHtmlGraphSvg.XSvg):
  """
  """

  alias, chartObject = 'meter', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html',
                'https://bl.ocks.org/mbostock/3887235',
                'http://bl.ocks.org/enjalot/1203641',
                'https://stackoverflow.com/questions/16191542/how-to-customize-color-in-pie-chart-of-nvd3']
  __chartStyle = {'showLabels': 'false',
                  'donut': 'true',
                  'growOnHover': 'false',
                  'x': "function(d) { return d.key; }",
                  'y': "function(d) { return d.value; }"}

  __svgProp = {
    'transition': '',
  }

  __chartProp = {
  #  'pie': {'startAngle': 'function(d) { return d.startAngle/2 -Math.PI/2 }',
  #          'endAngle': 'function(d) { return d.endAngle/2 -Math.PI/2 }'}
  }

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']
  clickJsFnc = None

  def val(self, value):
    """

    :param value:
    :return:
    """
    self.addChartAttr({'title': "'%s%%'" % value})

  def arcsRadius(self):
    """

    :return:
    """
    self.addChartAttr({'arcsRadius': "'arcRadius1'"})

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    data = data if data is not None else self.getData()
    if self.clickJsFnc is None:
      self.clickJsFnc = 'alert(e.data.key);'

    #self.click()
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    #dispatchChart.append("%s.legend.dispatch.on('stateChange.pie', function(d){ d.disabled ; alert(%s.legend); } )" % (self.htmlId, self.htmlId))
    return '''
              // var arcRadius1 = [{ inner: 0.6, outer: 1 },{ inner: 0.65, outer: 0.95 }];

              %(chartDimension)s ;
              d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s)%(svgProp)s.call(%(htmlId)s); %(dispatchChart)s ;
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'],
                   'chartProp': self.propToStr(), 'height': self.height, 'data': data['data'], 'svgProp': self.getSvg(),
                   'dispatchChart': ";".join(dispatchChart)}

  def click(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = self.clickJsFnc