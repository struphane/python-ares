"""

Most of the graph can be details on the below links:
  - http://nvd3.org/examples/

"""


from click import echo

from ares.Lib.html import AresHtmlContainer
from ares.Lib import AresItem
from ares.Lib import AresJs


class JsNvD3Graph(AresHtmlContainer.GraphSvG):
  """

  the variable self.htmlId will directly refer to the parent Div tag.
  All the variable created in the javascript will be with the suffic _self.htmlId in order to make the link
  very easily between the javascript and the HTML.

  Also it will make the html manual investigation easier

  """
  duration = 350
  clickFnc, clickObject = None, None
  style = {'chartStyle': {}, 'chartAttr': {}}
  pyDataSource = None
  chartObject = 'to be overriden'
  jsFrag = '''.x(function(d) { return d[0]; }).y(function(d) { return d[1]; })'''
  jsFiles = ['jquery']

  def dataFnc(self):
    """ Return the data Source converted to them be sent to the javascript layer """
    return "buildMultiSeriesRecordSet(%s, %s, %s, %s, %s)" % (self.jqRecordSet, self.jqSeriesKey, self.jqCategory, self.jqValue, self.jqSeries)

  def update(self, data):
    """ Update the content of an HTML component """
    item = AresItem.Item("var filterRecordSet = buildMultiSeriesRecordSet(%s, %s, %s, %s, %s) ;" % (self.jqRecordSet, self.jqSeriesKey,  self.jqCategory, self.jqValue, self.jqSeries))
    item.add(0, "var %s = nv.models.%s().x(function(d) { return d[0]; }).y(function(d) { return d[1]; });" % (self.chartObject, self.chartObject))
    item.add(0, "d3.%s.datum(filterRecordSet).transition().duration(500).call(%s) ;" % (self.jqId, self.chartObject))
    return str(item)

  def addStyle(self, style):
    """ add style to graphs (will be added to the nv.models js function"""
    self.style.setdefault('chartStyle', {}).update(style)

  def addAttr(self, attr):
    """ add attributes to graphs (will be added AFTER the nv.models js function
    Mostly used to custom/add axis"""
    for subObj, subAttr in attr.items():
      self.style.setdefault('chartAttr', {}).setdefault(subObj, {}).update(subAttr)

  def getChartDefaultStyle(self):
    """ Return the chart default Style """
    return self.style

  def delStyle(self, style):
    """ """
    self.style['charStyle'].pop(style, None)

  def delAttr(self, axis, attr):
    """ """
    self.style['chartAttr'].get(axis, {}).pop(attr, None)

  def formatChart(self):
    """ """
    chartStyle, chartAttr = [], []
    for style, attr in self.style.get('chartStyle', {}).items():
      chartStyle.append('%s(%s)' % (style, attr))
    for subObj, attr in self.style.get('chartAttr', {}).items():
      for subAttr, val in attr.items():
        chartAttr.append('chart_%s.%s.%s(%s)' % (self.htmlId, subObj, subAttr, val))
    return ('\n.'.join(chartStyle), ';'.join(chartAttr))

  def addClick(self, fnc):
    """ Add Click function on a graph """
    self.clickFnc = 'chart_%s.%s.dispatch.on("elementClick", function(e) {%s});' % (self.htmlId, self.clickObject, fnc)

  def linkTo(self, dataSource):
    """ Add a link to the datasource to remove the need to specify that in the selectors"""
    self.pyDataSource = dataSource
    try:
      dataSource.jsLinkTo([self]) #all datasource should have a jsLinkTo function (see AresHtmlTable)
    except Exception as e:
      echo(e)
      echo('Please use a data source that has a jsLinkTo attribute')


  # ------------------------------------------------------------------------------------------------------------
  #                                           Javascript Events section
  # ------------------------------------------------------------------------------------------------------------
  def jsEvents(self, jsEventFnc=None):
    """ It is not possible to have sub HTML items in a graph object """
    if jsEventFnc is None:
      jsEventFnc = self.jsEventFnc
    jGraphAttr = {'src': self.jqId, 'htmlId': self.htmlId, 'duration': self.duration}
    self.jsEvent['addGraph'] = AresJs.JD3Graph(jGraphAttr, self.jsChart().strip(), self.dataFnc())
    if self.clickFnc is not None:
      self.jsEvent['addGraph'].click(self.clickFnc)
    for jEventType, jsEvent in self.jsEvent.items():
      jsEventFnc[jEventType].add(str(jsEvent))
    return jsEventFnc

  def jsUpdate(self, jsDataVar='data'):
    """ Update the content of an HTML component """
    item = AresItem.Item("var filterRecordSet = buildMultiSeriesRecordSet(%s, %s, %s, %s, %s) ;" % (jsDataVar, self.jqSeriesKey, self.jqCategory, self.jqValue, self.jqSeries))
    item.add(0, "var %s = nv.models.%s().x(function(d) { return d[0]; }).y(function(d) { return d[1]; });" % (self.chartObject, self.chartObject))
    item.add(0, "d3.%s.datum(filterRecordSet).transition().duration(500).call(%s) ;" % (self.jqId, self.chartObject))
    return str(item)

  def jsChart(self):
    style, attr = self.formatChart()
    if style:
      style = '\n.%s' % style
    return '''nv.models.%s()%s%s; %s ''' % (self.chartObject, self.jsFrag, style, attr)

  @property
  def jqId(self):
    """ Function to return the Jquery reference to the Html object """
    return 'select("#%s svg")' % self.htmlId

  def js(self, evenType, jsDef):
    """ Add a Javascript Event to an HTML object """
    raise Exception("Cannot work for a graph ")


class Pie(JsNvD3Graph):
  """
  NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  alias = 'pie'
  mockData = r'json\pie.json'
  clickObject = 'pie'
  style = {'chartStyle': {'showLabels': '1'}}
  chartObject = 'pieChart'
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['d3']

  def update(self, data):
    """ Update the content of an HTML component """
    chartStyle = ['%s(%s)' % (style, attr) for style, attr in self.style.get('chartStyle', {}).items()]
    item = AresItem.Item("var filterRecordSet = wrapperSimpleCharts(%s, %s, %s) ;" % (self.jqRecordSet, self.jqCategory, self.jqValue))
    item.add(0, "var %s = nv.models.%s().x(function(d) { return d[0]; }).y(function(d) { return d[1]; }).%s;" % (self.chartObject, self.chartObject, ".".join(chartStyle)))
    item.add(0, "d3.%s.datum(filterRecordSet).transition().duration(500).call(%s) ;" % (self.jqId, self.chartObject))
    return str(item)

  def dataFnc(self):
    """ Return the data Source converted to them be sent to the javascript layer """
    return "wrapperSimpleCharts(%s, %s, %s)" % (self.jqRecordSet, self.jqCategory, self.jqValue)


class Donut(Pie):
  """

  data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  mockData = r'json\pie.json'
  alias = 'donut'
  clickObject = 'pie'
  style = {'chartStyle': {'showLabels': '1', 'labelThreshold': '.05', 'labelType': '"percent"', 'donut': 'true', 'donutRatio': '0.35'} }
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']


class Bar(JsNvD3Graph):
  """

  data format expected in the graph:
    [{key: "Cumulative Return", values: [{ "label": "One","value" : 29.765957771107},  {"label": "Four", "value" : 196.45946739256}]}]
  """
  duration = 200
  mockData = r'json\bar.json'
  alias = 'bar'
  clickObject = 'discretebar'
  icon = 'fa fa-bar-chart'
  chartObject = 'discreteBarChart'
  style = {'chartStyle': {'staggerLabels': 'true',
                          'showValues': 'true',
                          'transitionDuration': '350'
                          } }
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  @classmethod
  def aresExample(cls, aresObj):
    #return aresObj.bar([{"key": "Cumulative Return", "values": [{ "label": "One","value" : 29.765957771107},  {"label": "Four", "value": 196.45946739256}]}])
    return aresObj.bar([{"key": "Cumulative Return", "values": [1, 2, 3, 4, 5]}])


class Line(JsNvD3Graph):
  """

  data format expected in the graph
    [{color: "#ff7f0e", key: "Sine Wave", values: [{x: 1, y:10.0}, {x: 2, y:30.0}]}]

  """
  duration = 200
  mockData = r'json\line.json'
  alias = 'lineChart'
  chartObject = 'lineChart'
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']

  style = {'chartStyle': {'margin': '{left: 100}', 'useInteractiveGuideline': 'true', 'showLegend': 'true',
                          'showYAxis': 'true', 'showXAxis': 'true'},
           'chartAttr': {'xAxis': {'axisLabel': '',
                                  'tickFormat': "d3.format(',r')"
                                  },
                         'yAxis': {'axisLabel': "'Voltage (v)'",
                                   'tickFormat': "d3.format('.02f')"}
                        }
           }


class StackedArea(JsNvD3Graph):
  """ This object will output a simple stacked area chart

  Reference website: http://nvd3.org/examples/stackedArea.html
  """
  alias = 'stackedAreaChart'
  mockData = r'json\stackedAreaData.json'
  chartObject = 'stackedAreaChart'
  style = {'chartStyle': {'useInteractiveGuideline': 'true', 'clipEdge': 'true'},
           'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   # 'tickFormat' :"function(d) { return d3.time.format('%%x')(new Date(d)) }",
                                   },
                         'yAxis': {'tickFormat': "d3.format(',.2f')"}
                         }}

  clickObject = 'scatter'
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']


class MultiBars(JsNvD3Graph):
  """ Simple multi bar chart

    http://nvd3.org/examples/multiBar.html

    Expected data should look like:

    [
    {
      "key" : "North America" ,
      "values" : [ [ 1025409600000 , 23.041422681023] , [ 1028088000000 , 19.854291255832] , [ 1030766400000 , 21.02286281168] ,
        ...]
    },

    {
      "key" : "Africa" ,
      "values" : [ [ 1025409600000 , 7.9356392949025] , [ 1028088000000 , 7.4514668527298] , [ 1030766400000 , 7.9085410566608] ,
        ... ]
    },
    ...
    ]
"""

  mockData = r'json\multiBar.json'
  chartObject = 'multiBarChart'
  alias = 'multiBarChart'
  clickObject = 'multibar'
  style = {'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }",
                                   },
                         'yAxis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']


class LineWithFocus(JsNvD3Graph):
  """ Simple line chart with a focus field to zoom in on specific parts of the chart

    http://nvd3.org/examples/lineWithFocus.html

    Expected data should look like:

    [
    {
      "key" : "North America" ,
      "values" : [ [ 1025409600000 , 23.041422681023] , [ 1028088000000 , 19.854291255832] , [ 1030766400000 , 21.02286281168] ,
        ...]
    },

    {
      "key" : "Africa" ,
      "values" : [ [ 1025409600000 , 7.9356392949025] , [ 1028088000000 , 7.4514668527298] , [ 1030766400000 , 7.9085410566608] ,
        ... ]
    },
    ...
    ]

  """

  mockData = r'json\lineWithFocus.json'
  chartObject = 'lineWithFocusChart'
  alias = 'lineChartFocus'

  style = {'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat': "function(d) { return d3.time.format('x')(new Date(d)) }",},
                         'yAxis': {'tickFormat': "d3.format(',.2f')",},
                         'x2Axis': {'showMaxMin': 'false',
                                    'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }",},
                         'y2Axis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']


class HorizontalBars(JsNvD3Graph):
  """ Simple Horizontal bar chart

    http://nvd3.org/examples/multiBarHorizontal.html

    Expected data should look like:

    [
    {
      "key" : "North America" ,
      "values" : [ [ 1025409600000 , 23.041422681023] , [ 1028088000000 , 19.854291255832] , [ 1030766400000 , 21.02286281168] ,
        ...]
    },

    {
      "key" : "Africa" ,
      "values" : [ [ 1025409600000 , 7.9356392949025] , [ 1028088000000 , 7.4514668527298] , [ 1030766400000 , 7.9085410566608] ,
        ... ]
    },
    ...
    ]

  """
  alias = 'horizBarChart'
  mockData = r'json\horizBars.json'
  chartObject = 'multiBarHorizontalChart'

  style = {'chartStyle': {'margin': '{top: 30, right: 20, bottom: 50, left: 175}',
                          'showValues': 'true',
                          'tooltips': 'false',
                          'showControls': 'false'},
           'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat':"function(d) { return d3.time.format('%x')(new Date(d)) }",},
                         'yAxis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']


class ComboLineBar(JsNvD3Graph):
  """
  This object will combine a line and a bar chart.
  The first item should be the line chart

  The second will the bar chart

  Reference website: http://nvd3.org/examples/linePlusBar.html
  """
  alias = 'comboLineBar'
  mockData = r'json\linePlusBarData.json'
  chartObject = 'linePlusBarChart'

  style = {'chartStyle': {'color': 'd3.scale.category10().range()'},
           'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }",
                                   },
                         'bars': {'forceY': '[0]'},
                         'y1Axis': {'tickFormat': "d3.format(',.2f')"},
                         'y2Axis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']


class ScatterChart(JsNvD3Graph):
  """ Simple Scatter chart

    http://nvd3.org/livecode/index.html#codemirrorNav

    Expected data should look like:

    [
    {
      "key" : "North America" ,
      "values" : [ [ 1025409600000 , 23.041422681023] , [ 1028088000000 , 19.854291255832] , [ 1030766400000 , 21.02286281168] ,
        ...]
    },

    {
      "key" : "Africa" ,
      "values" : [ [ 1025409600000 , 7.9356392949025] , [ 1028088000000 , 7.4514668527298] , [ 1030766400000 , 7.9085410566608] ,
        ... ]
    },
    ...
    ]

  """
  mockData = r'json\multiBar.json'
  chartObject = 'scatterChart'
  alias = 'scatterChart'
  style = {'chartStyle': {},
           'chartAttr': {'xAxis': {'showMaxMin': 'false',
                                   'tickFormat': "function(d) { return d3.time.format('%x')(new Date(d)) }"},
                         'yAxis': {'tickFormat': "d3.format(',.2f')"}
                         }}
  reqCss = ['bootstrap', 'font-awesome', 'd3']
  reqJs = ['jquery', 'd3']


class Network(JsNvD3Graph):
  """

  Reference website: https://github.com/nylen/d3-process-map
  """
  mockData = r'json\mapGraph.json'
  alias = 'network'

  def js(self, localPath=None):
    """ Return the entries to be added to the Javascript to create the graph during the loading """
    res = ["%svar config = %s ;\n" % (INDENT, self.pyDataToJs(localPath))]
    return "\n".join(res)





