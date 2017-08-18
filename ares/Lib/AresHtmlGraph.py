"""

Most of the graph can be details on the below links:
  - http://nvd3.org/examples/

"""

from ares.Lib import AresHtmlContainer
from ares.Lib import AresItem
from ares.Lib import AresJs

class JsGraph(AresHtmlContainer.GraphSvG):
  """

  the variable self.htmlId will directly refer to the parent Div tag.
  All the variable created in the javascript will be with the suffic _self.htmlId in order to make the link
  very easily between the javascript and the HTML.

  Also it will make the html manual investigation easier

  """
  duration = 350
  clickFnc, clickObject = None, None
  width, height = 960, 500

  def dataFnc(self):
    """ Return the data Source converted to them be sent to the javascript layer """
    return self.vals

  def jsChart(self):
    """ Return the javascript fragment require to build the graph """
    raise NotImplementedError('subclasses must override jsChart()!')

  def jsEvents(self, jsEventFnc=None):
    """ It is not possible to have sub HTML items in a graph object """
    if jsEventFnc is None:
      jsEventFnc = self.jsEventFnc
    jGraphAttr = {'src': self.jsRef(), 'htmlId': self.htmlId, 'duration': self.duration}
    self.jsEvent['addGraph'] = AresJs.JD3Graph(jGraphAttr, self.jsChart().strip(), self.dataFnc())
    self.jsEvent['addGraph'].width = self.width
    self.jsEvent['addGraph'].height = self.height
    if self.clickFnc is not None:
      self.jsEvent['addGraph'].click(self.clickFnc)
    for jEventType, jsEvent in self.jsEvent.items():
      jsEventFnc[jEventType].add(str(jsEvent))
    return jsEventFnc

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object """
    return 'select("#%s svg")' % self.htmlId

  def js(self, evenType, jsDef):
    """ Add a Javascript Event to an HTML object """
    raise Exception("Cannot work for a graph ")

  def addClick(self, fnc):
    """ Add Click function on a graph """
    self.clickFnc = 'chart_%s.%s.dispatch.on("elementClick", function(e) {%s});' % (self.htmlId, self.clickObject, fnc)

class Pie(JsGraph):
  """
  NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  Data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  showLabel, alias = 1, 'pieChart'
  mockData = r'json\pie.json'
  clickObject = 'pie'

  def jsChart(self):
    """ Return the javascript method to use to create the Chart """
    return '''
              nv.models.pieChart()
                .x(function(d){ return d[0] }).
                y(function(d){ return d[1] }).
                showLabels(%s);
            ''' % self.showLabel


class Donut(Pie):
  """

  Data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  mockData = r'json\pie.json'
  alias = 'donutChart'
  clickObject = 'pie'

  def jsChart(self):
    """ Return the javascript method to use to create the Chart """
    return '''
              nv.models.pieChart()
                .x(function(d){ return d[0] ; })
                .y(function(d){ return d[1] ; })
                .showLabels(%s)
                .labelThreshold(.05)
                .labelType("percent")
                .donut(true)
                .donutRatio(0.35);
           ''' % self.showLabel


class Bar(JsGraph):
  """

  Data format expected in the graph:
    [{key: "Cumulative Return", values: [{ "label": "One","value" : 29.765957771107},  {"label": "Four", "value" : 196.45946739256}]}]
  """
  duration = 200
  mockData = r'json\bar.json'
  alias = 'bar'
  clickObject = 'discretebar'

  def jsChart(self):
    """ """
    return '''
              nv.models.discreteBarChart()
                .x(function(d) { return d[0] ; })    //Specify the data accessors.
                .y(function(d) { return d[1] ; })
                .staggerLabels(true)    // Too many bars and not enough room? Try staggering labels.
                .showValues(true)       // ...instead, show the bar value right on top of each bar.
                .transitionDuration(350);
           '''


class Line(JsGraph):
  """

  Data format expected in the graph
    [{color: "#ff7f0e", key: "Sine Wave", values: [{x: 1, y:10.0}, {x: 2, y:30.0}]}]

  """
  duration = 200
  mockData = r'json\line.json'
  alias = 'lineChart'

  def jsxAxix(self):
    """ """
    return '''
            chart_%s.xAxis     //Chart x-axis settings
                    .axisLabel('Time (ms)')
                    .tickFormat(d3.format(',r'));
           ''' % self.htmlId

  def jsyAxix(self):
    """ """
    return '''
            chart_%s.yAxis     //Chart y-axis settings
                    .axisLabel('Voltage (v)')
                    .tickFormat(d3.format('.02f'));
           ''' % self.htmlId

  def jsChart(self):
    """ """
    return '''
              nv.models.lineChart()
                .margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                .showYAxis(true)        //Show the y-axis
                .showXAxis(true)        //Show the x-axis
              ;

              %s

              %s
           ''' % (self.jsxAxix().strip(), self.jsyAxix().strip())


class StackedArea(JsGraph):
  """ This object will output a simple stacked area chart

  Reference website: http://nvd3.org/examples/stackedArea.html
  """
  alias = 'stackedAreaChart'
  mockData = r'json\stackedAreaData.json'
  withFocus = False
  multiY = False
  chartFunction = 'stackedAreaChart'
  useExtraChartOptions = True
  chartOptions = '''
                  .useInteractiveGuideline(true)
                  .clipEdge(true)
                  '''
  extraOptions = ''
  useDefaultYAxis = True
  clickObject = 'scatter'

  def pyDataToJs(self, localPath=None):
    """
    """
    if self.useMocked:
      if hasattr(self, 'mockData'):
        mockFile = open(self.mockData, 'r')
        self.pyData = eval(mockFile.read())

      else:
        raise Exception('No mock data defined for this chart')

    jsData = '['
    for rec in self.pyData:
      keys = rec.keys()
      jsData = '%s {"key": "%s", "values" : [' % (jsData, rec['key'])
      for value in rec['values']:
        jsData = '%s [%s, %s], ' % (jsData, str(value[0]), str(value[1]))

      jsData = '%s ]' % jsData
      if len(keys) > 2:
        for key in keys:
          if key not in ('key', 'values'):
            if rec[key][0] == 'str':
              jsData = '%s, "%s": "%s" ' % (jsData, key, rec[key][1])
            else:
              jsData = '%s, "%s": %s ' % (jsData, key, rec[key][1])
      jsData = '%s },' % jsData
    jsData = '%s ]' % jsData
    return jsData

  def addExtraOptions(self):
    """ To be overriden in case extraOptions are used """
    return self.extraOptions

  def jsChart(self):
    """ """
    focusOption = ''
    if self.withFocus:
      focusOption = '''
            chart_%s.x2Axis
                .showMaxMin(false)
                .tickFormat(function(d) { return d3.time.format('%%x')(new Date(d)) });
          
            chart_%s.y2Axis
                .tickFormat(d3.format(',.2f'));''' % (self.htmlId, self.htmlId)
    elif self.multiY:
      focusOption = '''
      
            chart_%s.y2Axis
                .tickFormat(d3.format(',.2f'));''' % (self.htmlId)

    if not self.useExtraChartOptions:
      self.chartOptions = ''

    if self.useDefaultYAxis:
      yAxis = '''chart_%s.yAxis
                .tickFormat(d3.format(',.2f'));''' % self.htmlId
    else:
      yAxis = ''

    return ''' 
            nv.models.%s()
                .x(function(d) { return d[0] })
                .y(function(d) { return d[1] })
                %s
                ;

            chart_%s.xAxis
                .showMaxMin(false)
                .tickFormat(function(d) { return d3.time.format('%%x')(new Date(d)) });
          
            %s
                
            %s
            
            %s
          ''' % (self.chartFunction, self.chartOptions, self.htmlId, yAxis, focusOption, self.addExtraOptions())


class MultiBars(StackedArea):
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
  withFocus = False
  chartFunction = 'multiBarChart'
  useExtraChartOptions = False
  alias = 'multiBarChart'
  clickObject = 'multibar'

class LineWithFocus(StackedArea):
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
  withFocus = True
  chartFunction = 'lineWithFocusChart'
  useExtraChartOptions = False
  alias = 'lineChartFocus'

class HorizontalBars(StackedArea):
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
  withFocus = False
  chartFunction = 'multiBarHorizontalChart'
  useExtraChartOptions = True
  chartOptions = ''' 
                  .margin({top: 30, right: 20, bottom: 50, left: 175})
                  .showValues(true)
                  .tooltips(false)
                  .showControls(false)
                  '''


class ComboLineBar(StackedArea):
  """
  This object will combine a line and a bar chart.
  The first item should be the line chart

  The second will the bar chart

  Reference website: http://nvd3.org/examples/linePlusBar.html
  """
  alias = 'comboLineBar'
  mockData = r'json\linePlusBarData.json'
  withFocus = False
  chartFunction = 'linePlusBarChart'
  multiY = True
  interGuidelines = False
  extraOptions = '''
                    chart_%s.bars.forceY([0]) ;
                    chart_%s.y1Axis.tickFormat(d3.format(',.2f')) ;
                 '''
  chartOptions = '''
                    .color(d3.scale.category10().range())
                 '''
  useDefaultYAxis = False

  def addExtraOptions(self):
    return self.extraOptions % (self.htmlId, self.htmlId)


class ScatterChart(StackedArea):
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
  withFocus = False
  chartFunction = 'scatterChart'
  useExtraChartOptions = False
  alias = 'scatterChart'

class Network(JsGraph):
  """

  Reference website: https://github.com/nylen/d3-process-map
  """
  mockData = r'json\mapGraph.json'
  alias = 'network'

  def js(self, localPath=None):
    """ Return the entries to be added to the Javascript to create the graph during the loading """
    res = ["%svar config = %s ;\n" % (INDENT, self.pyDataToJs(localPath))]
    return "\n".join(res)


class IndentedTree(JsGraph):
  """
  Data expected:
    [ (label, url, values), (label, url, dataKeys)]
    Example
    [ ('NVD3', 'http://novus.github.com/nvd3',
            [("Charts", None,
                [("Simple Line", "http://novus.github.com/nvd3/ghpages/line.html", {"type": "Historical"})])]),
      ("Chart Components", None, "Universal")]
  reference site: http://nvd3.org/examples/indentedtree.html
  """
  showCount = 1
  alias = 'tree'

  def __init__(self, htmlId, cols, data, useMockData=False):
    """

    cols should be a list of col and the col object should be defined like a dictionary with the below properties
      col = { key: 'type', label: 'Type', width: '25%', type: 'text' }
    """
    super(IndentedTree, self).__init__(htmlId, data)
    self.cols = cols

  def pyDataToJs(self, localPath=None):
    """ """
    return self.pyData[0]

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object """
    return 'select("#chart%s")' % self.htmlId

  def jsChart(self):
    """ """
    return '''
              nv.models.indentedTree()
                .tableClass('table table-striped') //for bootstrap styling
                .columns([
                  {
                    key: 'key',
                    label: 'Name',
                    showCount: true,
                    type: 'text',
                    classes: function(d) { return d.url ? 'clickable name' : 'name' },
                    click: function(d) {if (d.url) window.location.href = d.url; }
                  },

                  // Section dedicated to the columns definition
                  {
                    key: 'type',
                    label: 'Type',
                    width: '25%',
                    type: 'text'
                  }

                ]);
          '''


class WordCloud(JsGraph):
  """

  This module will require the javascript module: d3.layout.cloud.js

  TODO finalise the update method and make it generic with all the graph
  the update method should appear once and only once in the javascript section of the page
  """
  mockData = r'json\pie.json'
  alias = 'cloudChart'

  def pyDataToJs(self, localPath=None):
    """ """
    res = []
    for label, value in self.pyData:
      res.append({"text": label, "size": value})
    return str(res)

  def js(self, localPath=None):
    """ Return the entries to be added to the Javascript to create the graph during the loading """
    res = ["var fill = d3.scale.category20();"]
    res.append("%svar data_%s = %s ;" % (INDENT, self.htmlId, self.pyDataToJs(localPath)))
    res.append('''
          d3.layout.cloud().size([960, 600])
            .words(data_%s) // Refer to the data variable
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .font("Impact")
            .fontSize(function(d) { return d.size; })
            .on("end", draw)
            .start()
          ;

          function draw(words) {
            d3.select("#chart%s svg") // Refer to the chart variable
              .append("g")
              .attr("transform", "translate(150,150)")
              .selectAll("text")
              .data(words)
              .enter().append("text")
              .style("font-size", function(d) { return d.size + "px"; })
              .style("font-family", "Impact")
              .style("fill", function(d, i) {  return fill(i); })
              .attr("text-anchor", "middle")
              .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
              .text(function(d) {  return d.text; });
          }
          ;

          %s
        '''% (self.htmlId, self.htmlId, self.jsUpdate()))
    return "\n".join(res)

  def jsUpdate(self):
    """ This function allow different component to update the world Cloud chart

    For example:

    """

    return '''
          // words should be the javascript version of the data set expected by the graph
          // Should be the select to the svg component
          function drawCloudUpdate(words, jsGraphRef){
             d3.layout.cloud().size([500, 500])
                .words(words)
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .start();

             jsGraphRef
                .selectAll("g").attr("transform", "translate(150,150)")
                .selectAll("text")
                  .data(words).enter().append("text")
                  .style("font-size", function(d) { return d.size + "px"; })
                  .style("font-family", "Impact")
                  .style("fill", function(d, i) { return fill(i); })
                  .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";  })
                  .text(function(d) { return d.text; });
          };
          '''




if __name__ == '__main__':
  obj = Pie(0, [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}])

  print(obj.jsEvents())
  print('\n'.join(obj.onLoad()))
  print(obj.__repr__())
