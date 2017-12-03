""" Chart module in charge of generating a Donut Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class Donut3D(AresHtmlGraphSvg.Svg):
  """ NVD3 Donut Chart python interface """
  alias, chartObject = 'pie3D', 'pieChart'
  references = ['http://nvd3.org/examples/pie.html']
  __chartStyle = {'showLabels': 'true',
                  'labelThreshold': .05,
                  'labelType': '"percent"',
                  'donut': 'true',
                  'donutRatio': 0.35,
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
  reqJs = ['donut-3d']

  def showLegend(self, boolFlag):
    """ Change the D3 flag to display the legend in the chart """
    if boolFlag:
      self.addChartProp('showLegend', 'true')
    else:
      self.addChartProp('showLegend', 'false')

  def outSideLabels(self, boolFlag):
    """ Change the flag to display the labels of teh chart outside """
    if boolFlag:
      self.addChartProp('showLabels', 'true')
      self.addChartProp('labelsOutside', 'true')
    else:
      self.addChartProp('labelsOutside', 'false')

  def changeColor(self, rangeColors):
    """ Change the default colors in the chart """
    self.addChartProp('color', 'd3.scale.ordinal().range(%s).range()' % json.dumps(rangeColors))

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toPie(self.vals, self.chartKeys, self.chartVals, extKeys=self.extKeys)
    newRecordSet = {}
    for key, vals in recordSet.items():
      newRecordSet[key] = [{'label': label, 'value': val} for label, val in vals]
    self.aresObj.jsGlobal.add("data_%s = %s ;" % (self.htmlId, json.dumps(newRecordSet)))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    # Dispatch method to add events on the chart (in progress)
    dispatchChart = ["%s.pie.dispatch.on('%s', function(e) { %s ;})" % (self.htmlId, displathKey, jsFnc) for displathKey, jsFnc in self.dispatch.items()]
    return '''
                d3.select("#%(htmlId)s svg").remove();
                var svg = d3.select("#(htmlId)%s").append("svg").attr("height", 250).attr("width", 400);
                svg.append("g").attr("id","salesDonut");
                var data = %(data)s ;
                for (i in data) { data[i].color = d3.scale.category20()(i) ; }; 
                Donut3D.draw("salesDonut", data, 250, 100, 100, 60, 20, 0.4);
                ''' % {'htmlId': self.htmlId, 'data': data}

  def click(self, jsFnc):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = jsFnc

  def alertVal(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = "alert('selected value = ' + e.data) ;"