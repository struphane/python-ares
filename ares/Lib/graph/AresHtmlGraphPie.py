""" Chart module in charge of generating a Pie Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3Pie(AresHtmlGraphSvg.Svg):
  """ NVD3 Pie Chart python interface """
  alias, chartObject = 'pie', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html',
                'https://bl.ocks.org/mbostock/3887235',
                'http://bl.ocks.org/enjalot/1203641',
                'https://stackoverflow.com/questions/16191542/how-to-customize-color-in-pie-chart-of-nvd3']
  __chartStyle = {'showLabels': 'true',
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvg.Svg.colorCharts),
                  'x': "function(d) { return d.key; }",
                  'y': "function(d) { return d.value; }"}

  __svgProp = {
    'transition': '',
  }

  __chartProp = {}

  # Required modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toPie(self.vals, self.chartKeys, self.chartVals, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s" % (self.htmlId, json.dumps(recordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    data = data if data is not None else self.jqData
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

class XNvD3Pie(AresHtmlGraphSvg.XSvg):
  """ NVD3 Pie Chart python interface """
  alias, chartObject = 'pie', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html',
                'https://bl.ocks.org/mbostock/3887235',
                'http://bl.ocks.org/enjalot/1203641',
                'https://stackoverflow.com/questions/16191542/how-to-customize-color-in-pie-chart-of-nvd3']
  __chartStyle = {'showLabels': 'true',
                  'color': 'd3.scale.ordinal().range(%s).range()' % json.dumps(AresHtmlGraphSvg.Svg.colorCharts),
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

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    data = data if data is not None else self.jqData
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
              %(xdimension)s ;
              d3.select("#%(htmlId)s svg").remove(); d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s)%(svgProp)s.call(%(htmlId)s); %(dispatchChart)s ;
              nv.utils.windowResize(%(htmlId)s.update);
            ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'xdimension': self.xDimensions,
                   'chartProp': self.propToStr(), 'height': self.height, 'data': data, 'svgProp': self.getSvg(),
                   'dispatchChart': ";".join(dispatchChart)}

  def click(self, jsFnc):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = jsFnc