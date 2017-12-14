""" Generic underlying module for the D3 charts
@author: Olivier Nogues

"""

import json
from ares.Lib import AresHtml
from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlRadio


class Svg(AresHtml.Html):
  """

  """
  __css = {'width': '95%', 'height': '100%'}
  colorCharts = ['#e5f2e5', '#cce5cc', '#b2d8b2', '#99cc99', '#fbf7f', '#66b266', '#4ca64c', '#329932', '#198c19', '#008000',
                 '#007300', '#007300', '#006600', '#005900', '#004c00', '#004000', '#003300', '#002600']

  height = 250

  def __init__(self, aresObj, header, vals, recordSetDef, chartKey=None, chartVal=None, cssCls=None, cssAttr=None, mockData=False):
    """ selectors is a tuple with the category first and the value list second """
    self.chartAttrs = dict(getattr(self, "_%s__chartStyle" % self.__class__.__name__, {}))
    self.chartProps = dict(getattr(self, "_%s__chartProp" % self.__class__.__name__, {}))
    super(Svg, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = header
    self.extKeys, self.dispatch, self.htmlContent, self.components = None, {}, [], []
    self.header = dict([(self.recKey(col), (self.recKey(col), col.get('type'), col.get('multiplier', 1))) for col in recordSetDef])
    self.svgProp = dict([(key, val) for key, val in getattr(self, "_%s__svgProp" % self.__class__.__name__, {}).items()])
    if mockData:
      self.processData = self.processDataMock

    # To add the default key and val if unique
    if chartKey is not None:
      self.chartKeys = [self.header[chartKey]]
      self.selectedChartKey = chartKey
    if chartVal is not None:
      self.chartVals = [self.header[chartVal]]
      self.selectedChartVal = chartVal

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))


  # --------------------------------------------------------------------------------------------------------------
  #
  #                                   CHARTS ATTRIBUTES AND PROPERTIES
  # --------------------------------------------------------------------------------------------------------------
  def addChartAttr(self, attrs):
    """ Change the object chart properties """
    self.chartAttrs.update(attrs)

  def delChartAttr(self, attrsList):
    """ Change the object chart properties """
    for attr in attrsList:
      if attr in self.chartAttrs:
        del self.chartAttrs[attr]

  def addChartProp(self, key, attrs):
    """ Change the object chart properties """
    if key not in self.chartProps:
      self.chartProps[key] = attrs
    else:
      self.chartProps[key].update(attrs)

  def delChartProp(self, attrs):
    """ Change the object chart properties """
    self.chartProps.update(attrs)

  def addSvgProp(self, attr):
    """ Change the object SVG properties """
    self.svgProp.update(attr)

  def attrToStr(self):
    """ Convert the list of dictionary attribute to class attributes """
    res = []
    self.resolveProperties(res, self.chartAttrs, None)
    return ".".join(res)

  def propToStr(self):
    """ Convert the list of dictionary object attributes to proper object attributes """
    res = []
    self.resolveProperties(res, self.chartProps, None)
    return "".join(['%s.%s;' % (self.htmlId, prop) for prop in res])

  def resolveProperties(self, res, data, prefix):
    """ Convert the dictionary of properties to a flat javascript definition """
    for jsKey, jsVal in data.items():
      if isinstance(jsVal, dict):
        if prefix is not None: # Deeper sub level in the NVD3 Chart property
          self.resolveProperties(res, jsVal, "%s.%s" % (prefix, jsKey))
        else: # First sub level of the NVD3 Chart property
          self.resolveProperties(res, jsVal, jsKey)
        continue

      if prefix is not None:
        res.append('%s.%s(%s)' % (prefix, jsKey, jsVal))
      else:
        res.append('%s(%s)' % (jsKey, jsVal))

  def getSvg(self):
    """ Return the SVG properties as a string """
    svgProperties = []
    self.resolveProperties(svgProperties, self.svgProp, None)
    if svgProperties:
      return ".%s" % ".".join(svgProperties)

    return ''

  # --------------------------------------------------------------------------------------------------------------
  #
  #                                     SETTER AND GETTER FOR THE CHARTS
  # --------------------------------------------------------------------------------------------------------------
  def __str__(self):
    """ Return the svg container """
    self.processData()
    self.categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _, _ in self.chartKeys],
                                     cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {},
                                     internalRef='key_%s' % self.htmlId, checked=self.selectedChartKey)
    self.values = AresHtmlRadio.Radio(self.aresObj, [val for val, _, _ in self.chartVals],
                                 cssAttr={'display': 'None'} if len(self.chartVals) == 1 else {},
                                 internalRef='val_%s' % self.htmlId, checked=self.selectedChartVal)

    self.categories.click([self])
    self.values.click([self])

    self.htmlContent.append(str(self.categories))
    self.htmlContent.append(str(self.values))
    self.htmlContent.append('<div %s><svg style="width:100%%;height:%spx;"></svg></div>' % (self.strAttr(), self.height))
    if self.headerBox:
      return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

    return "\n".join(self.htmlContent)

  def setKeys(self, keys, selected=None):
    """ Set a default key for the graph """
    self.chartKeys = [self.header[key] for key in keys]
    self.selectedChartKey = keys[selected] if selected is not None else keys[0]

  def mapxAxes(self, xValsList):
    """
    For the order on the abscisse, this can only work with 1 series
    Please make sure that the keys are correctly defined with intergers
    """
    self.addChartProp('xAxis', {'tickValues': [i for i in range(len(xValsList))]})
    self.addChartProp('xAxis', {'tickFormat': "function(d){ return %s[d] }" % json.dumps(xValsList)})

  def setVals(self, vals, selected=None):
    """ Set a default value for the graph """
    self.chartVals = [self.header[val] for val in vals]
    self.selectedChartVal = vals[selected] if selected is not None else vals[0]

  def setExtVals(self, keys, components):
    """ Link the result to the different components on the page """
    self.extKeys = keys
    self.components = components

  @property
  def jqId(self):
    """ Returns the javascript SVG reference """
    return '$("#%s svg")' % self.htmlId

  @property
  def jqData(self):
    """ Returns the javascript SVG reference """
    if self.components:
      dataComp = "+ '_' + ".join([comp.val for comp in self.components])
      return "data_%s[%s + '_' + %s + '_' + %s]" % (self.htmlId, dataComp, self.categories.val, self.values.val)

    return "data_%s[%s + '_' + %s]" % (self.htmlId, self.categories.val, self.values.val)

  @property
  def jqSeriesKey(self):
    """ Returns the selected category for the graph """
    return 'serie_%s' % self.htmlId

  # --------------------------------------------------------------------------------------------------------------
  #
  # --------------------------------------------------------------------------------------------------------------
  def dispatch(self, dispatchType, dispatchFnc):
    """ Add items and the functions in the dispatch methods in the chart """
    self.dispatch[dispatchType] = dispatchFnc

  def changeColor(self, rangeColors):
    """ Change the default colors in the chart """
    self.addChartProp('color', 'd3.scale.ordinal().range(%s).range()' % json.dumps(rangeColors))

  def showLegend(self, boolFlag):
    """ Change the D3 flag to display the legend in the chart """
    if boolFlag:
      self.addChartProp('showLegend', 'true')
    else:
      self.addChartProp('showLegend', 'false')

  def showValues(self, boolFlag):
    """ Change the D3 flag to display the legend in the chart """
    if boolFlag:
      self.addChartProp('showValues', 'true')
    else:
      self.addChartProp('showValues', 'false')

  def outSideLabels(self, boolFlag):
    """ Change the flag to display the labels of teh chart outside """
    if boolFlag:
      self.addChartProp('showLabels', 'true')
      self.addChartProp('labelsOutside', 'true')
    else:
      self.addChartProp('labelsOutside', 'false')

  def show(self):
    return "d3.select('#%s').style('display', 'block')" % (self.htmlId)

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(self.jsUpdate())
    for comp in self.components:
      comp.link(self.jsUpdate())

  def yAxisAsInt(self, withCcy=None):
    """ Return the data as integer """
    if withCcy is None:
      self.addChartProp("yAxis", {"tickFormat": "function(d){ return d3.format(',.0f')(d) }" })
    else:
      self.addChartProp("yAxis", {"tickFormat": "function(d){ return d3.format(',.0f')(d) + ' %s' }" % withCcy})

  def yAxisLabel(self, value):
    """ Add a label the the y axis """
    self.addChartProp('yAxis', {'axisLabel': "'%s'" % value})

  def xAxisLabel(self, value):
    """ Add a label the the y axis """
    self.addChartProp('xAxis', {'axisLabel': "'%s'" % value})

  def processDataMock(self, cat=None, val=None):
    """ Return the json data """
    self.chartKeys = [('MOCK', None, None)]
    self.selectedChartKey = 'MOCK'
    self.chartVals = [('DATA', None, None)]
    self.selectedChartVal = self.chartVals[0][0]
    self.aresObj.jsGlobal.add("data_%s = {'%s_%s': %s}" % (self.htmlId, self.selectedChartKey, self.selectedChartVal,
                                                      open(r"ares\json\%sData.json" % self.alias).read().strip()))

class XSvg(AresHtml.Html):
  """

  """
  __css = {'width': '95%', 'height': '100%'}
  colorCharts = ['#e5f2e5', '#cce5cc', '#b2d8b2', '#99cc99', '#fbf7f', '#66b266', '#4ca64c', '#329932', '#198c19', '#008000',
                 '#007300', '#007300', '#006600', '#005900', '#004c00', '#004000', '#003300', '#002600']

  height = 250

  def __init__(self, aresObj, headerBox, crossFilter, cssCls=None, cssAttr=None):
    """ selectors is a tuple with the category first and the value list second """
    self.chartAttrs = dict(getattr(self, "_%s__chartStyle" % self.__class__.__name__, {}))
    self.chartProps = dict(getattr(self, "_%s__chartProp" % self.__class__.__name__, {}))
    super(XSvg, self).__init__(aresObj, crossFilter, cssCls, cssAttr)
    self.extKeys, self.dispatch, self.htmlContent, self.components = None, {}, [], []
    self.svgProp = dict([(key, val) for key, val in getattr(self, "_%s__svgProp" % self.__class__.__name__, {}).items()])
    self.headerBox = headerBox
    crossFilter.links.add(self.htmlId)
    crossFilter.xFilter.charts.add(self)

  # --------------------------------------------------------------------------------------------------------------
  #
  #                                   CHARTS ATTRIBUTES AND PROPERTIES
  # --------------------------------------------------------------------------------------------------------------
  def addChartAttr(self, attrs):
    """ Change the object chart properties """
    self.chartAttrs.update(attrs)

  def delChartAttr(self, attrsList):
    """ Change the object chart properties """
    for attr in attrsList:
      if attr in self.chartAttrs:
        del self.chartAttrs[attr]

  def addChartProp(self, key, attrs):
    """ Change the object chart properties """
    if key not in self.chartProps:
      self.chartProps[key] = attrs
    else:
      self.chartProps[key].update(attrs)

  def delChartProp(self, attrs):
    """ Change the object chart properties """
    self.chartProps.update(attrs)

  def addSvgProp(self, attr):
    """ Change the object SVG properties """
    self.svgProp.update(attr)

  def attrToStr(self):
    """ Convert the list of dictionary attribute to class attributes """
    res = []
    self.resolveProperties(res, self.chartAttrs, None)
    return ".".join(res)

  def propToStr(self):
    """ Convert the list of dictionary object attributes to proper object attributes """
    res = []
    self.resolveProperties(res, self.chartProps, None)
    return "".join(['%s.%s;' % (self.htmlId, prop) for prop in res])

  def resolveProperties(self, res, data, prefix):
    """ Convert the dictionary of properties to a flat javascript definition """
    for jsKey, jsVal in data.items():
      if isinstance(jsVal, dict):
        if prefix is not None: # Deeper sub level in the NVD3 Chart property
          self.resolveProperties(res, jsVal, "%s.%s" % (prefix, jsKey))
        else: # First sub level of the NVD3 Chart property
          self.resolveProperties(res, jsVal, jsKey)
        continue

      if prefix is not None:
        res.append('%s.%s(%s)' % (prefix, jsKey, jsVal))
      else:
        res.append('%s(%s)' % (jsKey, jsVal))

  def getSvg(self):
    """ Return the SVG properties as a string """
    svgProperties = []
    self.resolveProperties(svgProperties, self.svgProp, None)
    if svgProperties:
      return ".%s" % ".".join(svgProperties)

    return ''

  @property
  def jqData(self):
    return self.vals.data()

  @property
  def xDimensions(self):
    return self.vals.dimension()

  # --------------------------------------------------------------------------------------------------------------
  #
  #                                     SETTER AND GETTER FOR THE CHARTS
  # --------------------------------------------------------------------------------------------------------------
  def __str__(self):
    """ Return the svg container """
    crossFilterGrp = self.vals
    for filter in crossFilterGrp.filters:
      for chart in crossFilterGrp.xFilter.charts:
        # Update all the charts linked to a given recordSet
        filter.change(chart.jsUpdate())
    self.htmlContent.append('<div %s><svg style="width:100%%;height:%spx;"></svg></div>' % (self.strAttr(), self.height))
    if self.headerBox:
      return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

    return "\n".join(self.htmlContent)

  def mapxAxes(self, xValsList):
    """
    For the order on the abscisse, this can only work with 1 series
    Please make sure that the keys are correctly defined with intergers
    """
    self.addChartProp('xAxis', {'tickValues': [i for i in range(len(xValsList))]})
    self.addChartProp('xAxis', {'tickFormat': "function(d){ return %s[d] }" % json.dumps(xValsList)})

  @property
  def jqId(self):
    """ Returns the javascript SVG reference """
    return '$("#%s svg")' % self.htmlId

  # --------------------------------------------------------------------------------------------------------------
  #
  # --------------------------------------------------------------------------------------------------------------
  def dispatch(self, dispatchType, dispatchFnc):
    """ Add items and the functions in the dispatch methods in the chart """
    self.dispatch[dispatchType] = dispatchFnc

  def changeColor(self, rangeColors):
    """ Change the default colors in the chart

    http://www.color-hex.com/color/008000
    """
    self.addChartProp('color', 'd3.scale.ordinal().range(%s).range()' % json.dumps(rangeColors))

  def showLegend(self, boolFlag):
    """ Change the D3 flag to display the legend in the chart """
    if boolFlag:
      self.addChartProp('showLegend', 'true')
    else:
      self.addChartProp('showLegend', 'false')

  def showValues(self, boolFlag):
    """ Change the D3 flag to display the legend in the chart """
    if boolFlag:
      self.addChartProp('showValues', 'true')
    else:
      self.addChartProp('showValues', 'false')

  def outSideLabels(self, boolFlag):
    """ Change the flag to display the labels of teh chart outside """
    if boolFlag:
      self.addChartProp('showLabels', 'true')
      self.addChartProp('labelsOutside', 'true')
    else:
      self.addChartProp('labelsOutside', 'false')

  def show(self):
    return "d3.select('#%s').style('display', 'block')" % (self.htmlId)

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(self.jsUpdate(None))
    for comp in self.components:
      comp.link(self.jsUpdate())

  def yAxisAsInt(self, withCcy=None):
    """ Return the data as integer """
    if withCcy is None:
      self.addChartProp("yAxis", {"tickFormat": "function(d){ return d3.format(',.0f')(d) }" })
    else:
      self.addChartProp("yAxis", {"tickFormat": "function(d){ return d3.format(',.0f')(d) + ' %s' }" % withCcy})

  def yAxisLabel(self, value):
    """ Add a label the the y axis """
    self.addChartProp('yAxis', {'axisLabel': "'%s'" % value})

  def xAxisLabel(self, value):
    """ Add a label the the y axis """
    self.addChartProp('xAxis', {'axisLabel': "'%s'" % value})
