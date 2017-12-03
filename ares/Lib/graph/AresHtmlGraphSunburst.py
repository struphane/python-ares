""" Chart module in charge of generating a PlotBox Chart
@author: Olivier Nogues

"""
#TODO Migrate to the new Chart framework

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg

class NvD3Sunburst(AresHtmlGraphSvg.Svg):
  """ NVD3 Sunburst Chart python interface """
  alias, chartObject = 'sunburst', 'sunburstChart'
  references = ['http://bl.ocks.org/jensgrubert/7789216']

  __chartStyle = {'showLabels': 'true',
                  'x': "function(d) { return d[0]; }",
                  'y': "function(d) { return d[1]; }",
                  'color': 'd3.scale.category20c()',}

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