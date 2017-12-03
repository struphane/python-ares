""" Chart module in charge of generating a Donut Chart
@author: Olivier Nogues

"""

import json
from Libs import AresChartsService
from ares.Lib.html import AresHtmlGraphSvg


class Donut3D(AresHtmlGraphSvg.Svg):
  """ NVD3 Donut Chart python interface """
  alias, chartObject = 'pie', 'pieChart'
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

  def processData(self):
    """ produce the different recordSet with the level of clicks defined in teh vals and set functions """
    recordSet = AresChartsService.toPie(self.vals, self.chartKeys, self.chartVals, extKeys=self.extKeys)
    self.aresObj.jsGlobal.add("data_%s = %s ;" % (self.htmlId, json.dumps(recordSet)))

  def processDataMock(self, cat=None, val=None):
    """ Return the json data """
    self.chartKeys = [('MOCK', None, None)]
    self.selectedChartKey = 'MOCK'
    self.chartVals = [('DATA', None, None)]
    self.selectedChartVal = self.chartVals[0][0]
    self.aresObj.jsGlobal.add("data_%s = {'%s_%s': %s}" % (self.htmlId, self.selectedChartKey, self.selectedChartVal,
                                                      open(r"ares\json\%sData.json" % self.alias).read().strip()))

  def jsUpdate(self, data=None):
    """ Javascript function to build and update the chart based on js variables stored as globals to your report  """
    data = data if data is not None else self.jqData
    # Dispatch method to add events on the chart (in progress)
    return '''  
              d3.select("#%(htmlId)s svg").remove();
              var svg = d3.select("#%(htmlId)s").append("svg").attr("height", 250).attr("width", 400);
              svg.append("g").attr("id","salesDonut"); var data = %(data)s ; var newData = [] ;
              for (i in data) { newData.push( {color: d3.scale.category20()(i), label: data[i][0], value: data[i][1]} )}; 
              Donut3D.draw("salesDonut", newData, 250, 100, 100, 60, 20, 0.4);
              ''' % {'htmlId': self.htmlId, 'data': data}

  def click(self, jsFnc):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = jsFnc

  def alertVal(self):
    """ Add a click even on the chart  """
    self.dispatch['elementClick'] = "alert('selected value = ' + e.data) ;"