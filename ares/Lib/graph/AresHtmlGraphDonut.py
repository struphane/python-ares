""" Chart module in charge of generating a Donut Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3Donut(AresHtmlGraphSvg.Svg):
  """ NVD3 Donut Chart python interface """
  alias, chartObject = 'donut', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html']
  __chartStyle = {'showLabels': 'true',
                  'labelThreshold': .05,
                  'labelType': '"percent"',
                  'donut': 'true',
                  'donutRatio': 0.35,
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvg.Svg.colorCharts),
                  'x': "function(d) { return d[0]; }",
                  'y': "function(d) { return d[1]; }"}

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

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toPie(self.vals, self.chartKeys, self.chartVals, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    # Dispatch method to add events on the chart (in progress)
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
              d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s)%(svgProp)s.call(%(htmlId)s); %(dispatchChart)s ;
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(),
                   'chartProp': self.propToStr(), 'height': self.height, 'data': data, 'svgProp': self.getSvg(),
                   'dispatchChart': ";".join(dispatchChart)}

  def click(self, jsFnc):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = jsFnc

  def alertVal(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = "alert('selected value = ' + e.data) ;"


class XNvD3Donut(AresHtmlGraphSvg.XSvg):
  """ NVD3 Pie Chart python interface """
  alias, chartObject = 'donut', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html']

  __chartStyle = {'showLabels': 'true',
                  'labelThreshold': .05,
                  'labelType': '"percent"',
                  'donut': 'true',
                  'donutRatio': 0.35,
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvg.Svg.colorCharts),
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
    data = data if data is not None else self.jqData
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