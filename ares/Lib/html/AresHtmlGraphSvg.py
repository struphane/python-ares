"""
"""

from ares.Lib import AresHtml
from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlRadio

class Svg(AresHtml.Html):
  """

  """
  __css = {'width': '95%', 'height': '100%'}
  references = []
  __prop = {} #'transition': '',

  def __init__(self, aresObj, header, vals, recordSetDef, cssCls=None, cssAttr=None, mockData=False):
    """ selectors is a tuple with the category first and the value list second """
    self.chartAttrs = dict(getattr(self, "_%s__chartStyle" % self.__class__.__name__, {}))
    self.chartProps = dict(getattr(self, "_%s__chartProp" % self.__class__.__name__, {}))
    super(Svg, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = header
    self.dispatch, self.htmlContent = {}, []
    self.recordSetId = id(vals)
    self.header = dict([(col['key'], col.get('type')) for col in recordSetDef])
    self.svgProp = dict(self._Svg__prop)
    for key, val in getattr(self, "_%s__svgProp" % self.__class__.__name__, {}).items():
      self.svgProp[key] = val
    if mockData:
      self.dataFnc = self.dataMockFnc

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
    return "\n.".join(res)

  def propToStr(self):
    """ Convert the list of dictionary object attributes to proper object attributes """
    res = []
    self.resolveProperties(res, self.chartProps, None)
    specialProperties = ['%s.%s;' % (self.htmlId, prop) for prop in res]
    return "\n".join(specialProperties)

  def resolveProperties(self, res, data, prefix):
    """ Convert the dictionary of properties to a flat javascript definition """
    for jsKey, jsVal in data.items():
      if isinstance(jsVal, dict):
        if prefix is not None:
          # Deeper sub level in the NVD3 Chart property
          self.resolveProperties(res, jsVal, "%s.%s" % (prefix, jsKey))
        else:
          # First sub level of the NVD3 Chart property
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
      return ".%s" % "\n.".join(svgProperties)
    return ''

  def __str__(self):
    """ Return the svg container """
    self.processData()
    self.htmlContent.append('<div %s><svg style="width:100%%;height:400px;"></svg></div>' % self.strAttr())
    return str(AresHtmlContainer.AresBox(self.htmlId, "\n".join(self.htmlContent), self.headerBox, properties=self.references))

  def setKeys(self, keys, selected=None):
    """ Set a default key for the graph """
    self.chartKeys = [(key, self.header[key]) for key in keys]
    self.selectedChartKey = keys[selected] if selected is not None else keys[0]

  def setVals(self, vals, selected=None):
    """ Set a default value for the graph """
    self.chartVals = [(val, self.header[val]) for val in vals]
    self.selectedChartVal = vals[selected] if selected is not None else vals[0]

  @property
  def jqId(self):
    """ Returns the javascript SVG reference """
    return '$("#%s svg")' % self.htmlId

  @property
  def jqRecordSet(self):
    """ Returns the javascript SVG reference """
    return 'recordSet_%s' % self.recordSetId

  @property
  def jqData(self):
    """ Returns the javascript SVG reference """
    return "eval('%s_' + %s + '_' + %s)" % (self.htmlId, self.dynKeySelection, self.dynValSelection)

  @property
  def jqSeriesKey(self):
    """ Returns the selected category for the graph """
    return 'serie_%s' % self.htmlId

  def dataMockFnc(self, cat=None, val=None):
    """ Return the json data """
    return open(r"ares\json\%sData.json" % self.alias).read().strip()

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _ in self.chartKeys], cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {})
    categories.select(self.selectedChartKey)
    self.dynKeySelection = categories.val # The javascript representation of the radio
    values = AresHtmlRadio.Radio(self.aresObj, [val for val, _ in self.chartVals], cssAttr={'display': 'None'} if len(self.chartVals) == 1 else {})
    values.select(self.selectedChartVal)
    self.dynValSelection = values.val # The javascript representation of the radio

    categories.click([self])
    values.click([self])

    self.htmlContent.append(str(categories))
    self.htmlContent.append(str(values))

    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(self.jsUpdate())


class MultiSvg(Svg):
  """
  """

  def setSeries(self, series, selected=None):
    """ """
    self.setKeys(series, selected)

  def setY(self, series, selected=None):
    """ """
    self.setVals(series, selected)

  def setX(self, x):
    """ """
    self.selectedX = (x, self.header[x])

  @property
  def jqData(self):
    """ Returns the javascript SVG reference """
    return "eval('%s_' + %s + '_' + %s)" % (self.htmlId, self.dynKeySelection, self.dynValSelection)

  def graph(self):
    """ Add the Graph definition in the Javascript method """
    categories = AresHtmlRadio.Radio(self.aresObj, [key for key, _ in self.chartKeys], cssAttr={'display': 'None'} if len(self.chartKeys) == 1 else {})
    categories.select(self.selectedChartKey)
    self.dynKeySelection = categories.val # The javascript representation of the radio
    values = AresHtmlRadio.Radio(self.aresObj, [val for val, _ in self.chartVals], cssAttr={'display': 'None'} if len(self.chartVals) == 1 else {})
    values.select(self.selectedChartVal)
    self.dynValSelection = values.val # The javascript representation of the radio

    categories.click([self])
    values.click([self])

    self.htmlContent.append(str(categories))
    self.htmlContent.append(str(values))

    chartAttributes = []
    self.resolveProperties(chartAttributes, self.chartAttrs, None)
    self.aresObj.jsGraphs.append(self.jsUpdate())