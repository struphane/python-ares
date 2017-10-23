"""

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class NvD3ComboLineBar(AresHtmlGraphSvg.MultiSvg):
  """
  This object will combine a line and a bar chart.
  The first item should be the line chart

  The second will the bar chart

  Reference website: http://nvd3.org/examples/linePlusBar.html
  """
  alias, chartObject = 'comboLineBar', 'linePlusBarChart'
  references = ['http://nvd3.org/examples/linePlusBar.html']
  __chartStyle = {
        'margin': '{top: 30, right: 60, bottom: 50, left: 70}',
        'x': 'function(d, i) { return i }',
        'y': 'function(d, i) { return d[1] }'
  }
  __chartProp = {
          'y1Axis': {'tickFormat': "d3.format(',f')"},
          'y2Axis': {'tickFormat': "function(d) { return '$' + d3.format(',f')(d) }"},
          'bars': {'forceY': '[0]'}
  }

  __svgProp = {
    'transition': '',
  }

  # Required CSS and JS modules
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    colors = dict([(col.get('key', col['colName']), col.get('color', 'green')) for col in self.header])
    barStyle = dict([(col.get('key', col['colName']), col.get('barStyle', False)) for col in self.header])
    recordSet = AresChartsService.toComboChart(self.vals, self.chartKeys, self.selectedX , self.chartVals, barStyle, colors)
    for key, vals in recordSet.items():
      self.aresObj.jsGlobal.add("%s_%s = %s ;" % (self.htmlId, key, json.dumps(vals)))

  def jsUpdate(self):
    dispatchChart = []
    for displathKey, jsFnc in self.dispatch.items():
      dispatchChart.append("%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc))
    return '''
            var %s = nv.models.%s().%s ;
            %s
            d3.select("#%s svg").datum(%s)%s.call(%s);
            nv.utils.windowResize(%s.update);
          ''' % (self.htmlId, self.chartObject, self.attrToStr(), self.propToStr(),
                 self.htmlId, self.jqData, self.getSvg(), self.htmlId, self.htmlId)

