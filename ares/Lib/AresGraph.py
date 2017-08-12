"""

Most of the graph can be details on the below links:
  - http://nvd3.org/examples/

"""

import os
import pprint

INDENT = '  '

class JsGraph(object):
  """

  the variable self.htmlId will directly refer to the parent Div tag.
  All the variable created in the javascript will be with the suffic _self.htmlId in order to make the link
  very easily between the javascript and the HTML.

  Also it will make the html manual investigation easier

  """
  duration = 350
  pyData = None

  def __init__(self, htmlId, data, useMockData=False):
    """ """
    self.__htmlId = htmlId
    self.pyData = data
    self.useMocked = useMockData

  @property
  def htmlId(self):
    return self.__htmlId

  def pyDataToJs(self):
    """ Return the data Source """
    raise NotImplementedError('subclasses must override data()!')

  def jsChart(self):
    """ Return the javascript fragment require to build the graph """
    raise NotImplementedError('subclasses must override jsChart()!')

  def js(self, localPath=None):
    """ Return the entries to be added to the Javascript to create the graph during the loading """
    res = ['%svar chart_%s = %s' % (INDENT, self.htmlId, self.jsChart().strip())]
    res.append('\n\n// Data section for chart_%s' % self.htmlId)
    res.append("%svar data_%s = %s ;\n" % (INDENT, self.htmlId, self.pyDataToJs(localPath)))
    res.append('''%sd3.%s
                      .datum(data_%s).transition()
                      .duration(%s)
                      .call(chart_%s);
                '''% (INDENT, self.jsRef(), self.htmlId, self.duration, self.htmlId))
    return "\n".join(res)

  def jsRef(self):
    """ Function to return the Jquery reference to the Html object """
    return 'select("#chart%s svg")' % self.htmlId

class Pie(JsGraph):
  """ NVD3 Wrapper for a Pie Chart object.

  This will expect as input data a list of tuple (label, value)

  Data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  showLabel = True

  def pyDataToJs(self, localPath=None):
    """ """
    res = []
    for label, value in self.pyData:
      res.append({"label": label, "value": value})

    # If the script is run locally intermediate data will be stored
    # This is for investigation only
    if localPath is not None:
      dataFolder = r"%s\data" % localPath
      if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)

      inFile = open(r"%s\chart_%s.dat" % (dataFolder, self.htmlId), "w")
      inFile.write("----------------- Python Object ----------------- \n")
      pprint.pprint(self.pyData, inFile)
      inFile.write("\n\n----------------- Javascript Object ----------------- \n")
      pprint.pprint(res, inFile)
      inFile.close()
    return str(res)

  def jsChart(self):
    """
    """
    return "nv.models.pieChart().x(function(d){ return d.label }).y(function(d){ return d.value }).showLabels(true);"

class Donut(Pie):
  """

  Data format expected in the Graph:
    [{ "label": "One","value" : 29.765957771107} , {"label": "Three", "value" : 32.807804682612}]
  """
  showLabel = 1 # True in Javascript

  def jsChart(self):
    """ """
    return '''
              nv.models.pieChart()
                .x(function(d){ return d.label })
                .y(function(d){ return d.value })
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

  def jsChart(self):
    """ """
    return '''
              nv.models.discreteBarChart()
                .x(function(d) { return d.label })    //Specify the data accessors.
                .y(function(d) { return d.value })
                .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
                .showValues(true)       //...instead, show the bar value right on top of each bar.
                .duration(350);
           '''

class Line(JsGraph):
  """

  Data format expected in the graph
    [{color: "#ff7f0e", key: "Sine Wave", values: [{x: 1, y:10.0}, {x: 2, y:30.0}]}]

  """
  duration = 200

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

  To be factorised in an abstract class

  Reference website: http://nvd3.org/examples/stackedArea.html
  """

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
  """ """

  mockData = r'json\multiBar.json'
  withFocus = False
  chartFunction = 'multiBarChart'
  useExtraChartOptions = False

class LineWithFocus(StackedArea):
  """ """

  mockData = r'json\lineWithFocus.json'
  withFocus = True
  chartFunction = 'lineWithFocusChart'
  useExtraChartOptions = False

class HorizontalBars(StackedArea):
  """ """

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
  mockData = r'json\linePlusBarData.json'
  withFocus = False
  chartFunction = 'linePlusBarChart'
  multiY = True
  interGuidelines = False
  extraOptions = '''chart_%s.bars.forceY([0]); chart_22.y1Axis
                .tickFormat(d3.format(',.2f'));'''
  chartOptions = '''.color(d3.scale.category10().range())'''
  useDefaultYAxis = False

  def addExtraOptions(self):
    return self.extraOptions % self.htmlId


class ScatterChart(StackedArea):
  """

  """
  mockData = r'json\linePlusBarData.json'
  chartFunction = 'scatterChart'

class Network(JsGraph):
  """

  Reference website: https://github.com/nylen/d3-process-map
  """

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

  def pyDataToJs(self, localPath=None):
    """ """
    res = []
    for label, value in self.pyData:
      res.append({"text": label, "size": value})

    # If the script is run locally intermediate data will be stored
    # This is for investigation only
    if localPath is not None:
      dataFolder = r"%s\data" % localPath
      if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)

      inFile = open(r"%s\chart_%s.dat" % (dataFolder, self.htmlId), "w")
      inFile.write("----------------- Python Object ----------------- \n")
      pprint.pprint(self.pyData, inFile)
      inFile.write("\n\n----------------- Javascript Object ----------------- \n")
      pprint.pprint(res, inFile)
      inFile.close()
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
            .fontSize(function(d) {  return d.size; })
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
              .attr("transform", function(d) {  return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
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
