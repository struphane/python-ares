""" Chart module in charge of generating a Spark Line Chart
@author: Olivier Nogues

"""

import json
from ares.Lib.html import AresHtmlGraphSvg


class XNvD3SparkLinePlus(AresHtmlGraphSvg.XSvg):
  """ NVD3 Spark Plus Line Chart python interface """
  alias, chartObject = 'sparklineplus', 'sparklinePlus'
  references = ['http://nvd3.org/examples/line.html']
  __chartStyle = {
    'margin': '{left:70}',
    'x': "function(d) { return d.key; }",
    'y': "function(d) { return d.value; }",
    'showLastValue': 'true',
    'showLastValue': "function(d) {return d3.time.format('%x')(new Date(data[d].x))}",
  }

  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    # Dispatch method to add events on the chart (in progress)
    data = data if data is not None else self.jqData
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
              %(chartDimension)s ;
              d3.select("#%(htmlId)s svg").remove();
              d3.select("#%(htmlId)s").append("svg");
              var %(htmlId)s = nv.models.%(chartObject)s().%(chartAttr)s ; %(chartProp)s
              d3.select("#%(htmlId)s svg").style("height", '%(height)spx').datum(%(data)s).call(%(htmlId)s);
              nv.utils.windowResize(%(htmlId)s.update);
          ''' % {'htmlId': self.htmlId, 'chartObject': self.chartObject, 'chartAttr': self.attrToStr(), 'chartDimension': data['vars'],
                  'chartProp': self.propToStr(), 'height': self.height, 'data': data['data']}