"""
Definition of all the different HTML Containers wrappers.

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs


class Div(AresHtml.Html):
  """ Python Wrapper for a simple DIV tag """
  references = ['https://www.w3schools.com/tags/tag_div.asp']
  alias = 'div'
  reqCss = ['bootstrap']
  reqJs = ['jquery']

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, htmlComp=None):
    super(Div, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.htmlComp = htmlComp

  def __str__(self):
    """ Return the HMTL object of for div """
    if self.htmlComp is not None:
      self.vals = self.vals.format(*self.htmlComp)
    return '<div %s>%s</div>' % (self.strAttr(), self.vals)

  @property
  def val(self):
    """ Return the Javascript Value """
    return '$("#%s").html()' % self.htmlId

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.div("MyDiv")


class TextContainer(AresHtml.Html):
  """ Python Wrapper for a simple DIV tag """
  reference = 'https://www.w3schools.com/tags/tag_div.asp'
  alias, cssCls = 'textContainer', ['container']
  reqCss = ['bootstrap']
  reqJs = ['jquery']

  def __str__(self):
    """ Return the HMTL object of for div """
    return '<div %s>%s</div>' % (self.strAttr(), self.vals)

  @property
  def val(self):
    """ Return the Javascript Value """
    return '$("#%s").html()' % self.htmlId


class IFrame(AresHtml.Html):
  """ Python Wrapper for an iFrame object"""
  references = ['https://www.w3schools.com/TAgs/tag_iframe.asp']
  alias = 'iframe'
  __css = {'width': '1000px', 'height': '700px', 'margin': 'auto 0', 'display': 'block'}

  def __str__(self):
    """ Return an iFrame Tag """
    return '<iframe src="%s" %s><p>Your browser does not support iframes.</p></iframe>' % (self.vals, self.strAttr())


class List(AresHtml.Html):
  """
  HTML List

  This object will return a HTML list and the constructor of this class is
  expecting in the values a list of tuples. The first one should be the
  name and the second the count to be displayed in the badge

  Default class parameters
    - CSS Default Class = list-group
  """
  cssCls = ['list-group']
  references = ['https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp',
                'http://astronautweb.co/snippet/font-awesome/']
  alias = 'list'

  def __init__(self, aresObj, headerBox, vals, cssCls=None, cssAttr=None):
    super(List, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.cssClsLi = ["list-group-item"] if 'list-group' in self.attr['class'] else []
    self.headerBox = headerBox

  def __str__(self):
    """ Return the String representation of a HTML List """
    item = AresItem.Item('<ul %s>' % self.strAttr())
    cssLi = ""
    if self.cssClsLi:
      cssLi = 'class="%s"' % " ".join(self.cssClsLi)
    for label in self.vals:

      item.add(3, '<li %s>%s</li>' % (cssLi, label))
    item.add(2, '</ul>')
    if self.headerBox is not None:
      return str(AresBox(self.htmlId, item, self.headerBox, properties=self.references))

    return str(item)

  def jsUpdate(self, jsDataVar='data'):
    """ Return the Javascript update function from a data object """
    return  '''
              // Data is supposed to be a list
              var listResult = data.join('</li><li class="list-group-item">')
              %s.html('<li class="list-group-item">' + listResult + '</li>') ;
            ''' % self.jqId


class ListBadge(AresHtml.Html):
  """
  HTML List

  This object will return a HTML list and the constructor of this class is
  expecting in the values a list of tuples. The first one should be the
  name and the second the count to be displayed in the badge

  Default class parameters
    - CSS Default Class = list-group
  """
  cssCls, alias = 'list-group', 'listbadge'
  references = ['https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp']

  def __str__(self):
    """ Return the String representation of a HTML List """
    item = AresItem.Item('<ul %s>' % self.strAttr())
    for label, cnt in self.vals:
      item.add(1, '<li class="list-group-item">%s<span class="badge">%s</span></li>' % (label, cnt))
    item.add(0, '</ul>')
    return str(item)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.listbadge([('A', 10), ('B', 50)])


class Container(Div):
  """
  Wrapper for a simple DIV container

  Default class parameters
    - CSS Default Class = container
  """
  cssCls, alias = ['container-fluid'], 'container'
  references = ['https://getbootstrap.com/docs/3.3/css/']

  def __init__(self, aresObj, header, vals, cssCls=None, cssAttr=None):
    """ Instanciate a container object """
    super(Container, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = header

  def __str__(self):
    """ Return the String representation of a HTML List """
    item = AresItem.Item(None)
    for val in self.vals:
      item.add(3, val)
    return str(AresBox(self.htmlId, item, self.headerBox, properties=self.references))

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.container('', "MyContainer")


class GraphSvG(AresHtml.Html):
  """
  Python Wrapper to a DIV tag with a SVG

  Default class parameters
    - CSS Default Class = span4 (for the DIV component)
    - width, height = 960, 500 (for the SVG component)
  """
  cssCls = ['panel-body', 'span4']
  width, height = 100, 400
  references = ['https://www.w3schools.com/html/html5_svg.asp']
  icon = 'fa fa-pie-chart'
  categories, values, seriesKey, series = None, None, None, None
  hasSeries = False
  recordSetKey = None
  multiOptions = True

  def __init__(self, aresObj, header, vals, recordSetDef, cssCls=None, cssAttr=None, mockData=False):
    """ selectors is a tuple with the category first and the value list second """
    super(GraphSvG, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = header
    self.recordSetId = id(vals)
    self.header = recordSetDef
    self.serieExist = False

  def __str__(self):
    """ Return the String representation of a DIV containing a SVG tag """
    self.selectCategory()
    self.selectValues()
    self.selectKey()
    self.selectSeries()

    item = AresItem.Item('')
    item.add(1, '<div style="width:95%%;height:100%%;" %s>' % self.strAttr())
    #TODO put a better display for this section
    item.add(1, '<div class="container">')
    # Add the pointers for the display
    if self.categories is not None:
      item.join(self.categories)
    if self.values is not None:
      item.join(self.values)
    if self.seriesKey is not None:
      item.join(self.seriesKey)
    if self.series is not None:
      item.join(self.series)
    item.add(1, '</div>')
    item.add(1, '<svg style="width:100%;height:400px;"></svg>')
    item.add(0, '</div>')
    item = AresBox(self.htmlId, item, self.headerBox)
    return str(item)

  def selectKey(self):
    """ for multicharts, define the key to be used in js recordSet"""
    item = AresItem.Item('')
    item.add(2, '<script>')
    for headerLine in self.header:
      if  headerLine.get('type') == 'series':
        item.add(3, "var serie_%s = '%s';" % (self.htmlId, headerLine.get('key', headerLine['colName'])))
        self.hasSeries = True
        break

    else:
      item.add(3, "var serie_%s = '';" % self.htmlId)
    item.add(2, '</script>')
    self.seriesKey = item

  def selectSeries(self):
    """ """
    style = 'style="margin-bottom:5px"' if len(self.header) > 2 else 'style="display:none"'
    if self.hasSeries and self.multiOptions:
      item = AresItem.Item('<select id="%s_series_selector" class ="form-control input-sm" multiple="true" %s>' % (self.htmlId, style))
      item.add(1, '<optgroup label="Series">')
    else:
      item = AresItem.Item('<select hidden id="%s_series_selector" class ="form-control input-sm" multiple="true" %s>' % (
      self.htmlId, style))
      item.add(3, '<option value="default" selected>default</option>')

    for headerLine in self.header:
      if headerLine.get('type') == 'series':
        if headerLine.get('selectedIdx'):
          item.add(3, '<option value="All">All</option>')
        else:
          item.add(3, '<option value="All" selected>All</option>')
        for i, val in enumerate(headerLine.get('values', []), 1):
          if i in headerLine.get('selectedIdx', []):
            item.add(3, '<option value="%s" selected>%s</option>' % (val, val))
          else:
            item.add(3, '<option value="%s">%s</option>' % (val, val))
    item.add(2, '</select>')
    self.series = item
    self.aresObj.jsOnLoadFnc.add(AresJs.JQueryEvents("%s_series_selector" % self.htmlId, "$('#%s_series_selector')" % self.htmlId,
                                                     'change', self.update(self.vals), ''))

  def selectCategory(self):
    """ Return the category to be selected in the graph display """
    style = 'style="margin-bottom:5px"' if len(self.header) > 2 and self.multiOptions else 'style="display:none"'
    item = AresItem.Item('<select id="%s_col_selector" class ="form-control input-sm" %s>' % (self.htmlId, style))
    item.add(1, '<optgroup label="X-Axis">')
    for headerLine in self.header:
      if headerLine.get('type') != 'object':
        if headerLine.get('selected') and headerLine.get('type') != 'number':
          item.add(3, '<option value="%s" selected>%s</option>' % (headerLine.get('key', headerLine['colName']), headerLine['colName']))
        elif headerLine.get('type') != 'series':
          item.add(3, '<option value="%s">%s</option>' % (headerLine.get('key', headerLine['colName']), headerLine['colName']))
    item.add(2, '</select>')
    self.categories = item
    self.aresObj.jsOnLoadFnc.add(AresJs.JQueryEvents("%s_col_selector" % self.htmlId, "$('#%s_col_selector')" % self.htmlId,
                                                     'change', self.update(self.vals), ''))

  def selectValues(self):
    """ Return the value to be selected in the graph display """
    # To early to think about the multi select
    values = []
    for headerLine in self.header:
      if headerLine.get('type') == 'number':
        isSelected = '' if headerLine.get('selected') else 'selected'
        values.append((isSelected, headerLine.get('key', headerLine['colName']), headerLine['colName']))
    style = 'style="margin-bottom:5px"' if len(values) > 2 and self.multiOptions else 'style="display:none"'
    item = AresItem.Item('<select id="%s_val_selector" class ="form-control input-sm" %s>' % (self.htmlId, style))
    item.add(1, '<optgroup label="Y-Axis">')
    for isSelect, key, val in values:
      item.add(3, '<option value="%s" %s>%s</option>' % (key, isSelect, val))
    item.add(2, '</select></label>')
    self.values = item
    self.aresObj.jsOnLoadFnc.add(AresJs.JQueryEvents("%s_val_selector" % self.htmlId, "$('#%s_val_selector')" % self.htmlId,
                                                     'change', self.update(self.vals), ''))

  @property
  def jqId(self):
    """ Returns the javascript SVG reference """
    return '$("#%s svg")' % self.htmlId

  @property
  def jqRecordSet(self):
    """ Returns the javascript SVG reference """
    return 'recordSet_%s' % self.recordSetId

  @property
  def jqCategory(self):
    """ Returns the selected category for the graph """
    return '$("#%s_col_selector option:selected")'% self.htmlId

  @property
  def jqSeriesKey(self):
    """ Returns the selected category for the graph """
    return 'serie_%s' % self.htmlId

  @property
  def jqSeries(self):
    """ """
    return '$("#%s_series_selector option:selected")'% self.htmlId

  @property
  def jqValue(self):
    """ Return the selected value to use for the graph """
    return '$("#%s_val_selector option:selected")' % self.htmlId


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
    self.dispatch = {}
    self.recordSetId = id(vals)
    self.header = recordSetDef
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
    items = AresItem.Item(None)
    items.add(0, self.selections())
    items.add(0,  '<div %s><svg style="width:100%%;height:400px;"></svg></div>' % self.strAttr())
    return str(AresBox(self.htmlId, str(items), self.headerBox, properties=self.references))

  def selections(self):
    """ Return the different filters according to the object complexity """
    return ''

  @property
  def jqId(self):
    """ Returns the javascript SVG reference """
    return '$("#%s svg")' % self.htmlId

  @property
  def jqRecordSet(self):
    """ Returns the javascript SVG reference """
    return 'recordSet_%s' % self.recordSetId

  @property
  def jqSeriesKey(self):
    """ Returns the selected category for the graph """
    return 'serie_%s' % self.htmlId

  def dataMockFnc(self, cat=None, val=None):
    """ Return the json data """
    return open(r"ares\json\%sData.json" % self.alias).read().strip()


class Tabs(AresHtml.Html):
  """
  Python wrapper for a multi Tabs component

  Default class parameters
    - CSS Default Class = nav nav-tabs
    - title = Home
  """
  alias = 'tabs'
  cssCls = ['nav', 'nav-tabs']

  def __str__(self):
    """ Return the HTML representation of a Tabular object """
    item = AresItem.Item('<ul %s>' % self.strAttr())
    item.add(1, '<li class="active"><a href="#">%s</a></li>' % self.vals[0])
    for val in self.vals[1:]:
      item.add(2, '<li><a href="#">%s</a></li>' % val)
    item.add(0, '</ul>')
    return str(item)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.tabs(["Tab1", "Tab2"])


class Row(AresHtml.Html):
  """

  """
  cssCls, alias = ['row'], 'row'
  gridCss = 'panel panel-success'
  references = ['https://getbootstrap.com/docs/3.3/css/']

  def __init__(self, aresObj, hltmObjs, cssCls=None, cssAttr=None):
    if len(hltmObjs) > 3:
      raise Exception('Row object can only display maximum 3 components')

    self.cssRow = {"text-align": "center", "width": "100%",
                   'display': 'inline-block', "padding": "20%"}
    if len(hltmObjs) == 3:
      vals = [('col-6 col-md-4', htmlObj) for htmlObj in hltmObjs]
    elif len(hltmObjs) == 2:
      vals = [('col-xs-6 col-sm-6', htmlObj) for htmlObj in hltmObjs]
    else:
      vals = [('', hltmObjs[0])]
    super(Row, self).__init__(aresObj, vals, cssCls, cssAttr)

  def extend(self, component):
    """ Extend one of the objects on to columns """
    tempVals = []
    for size, htmlOjb in self.vals:
      if id(component) == id(htmlOjb):
        tempVals.append(('col-xs-12 col-md-8', htmlOjb))
      else:
        tempVals.append(('col-xs-6 col-md-4', htmlOjb))
    self.vals = tempVals

  def __str__(self):
    """ Return the HTML display of a split container"""
    res = AresItem.Item('<div %s>' % self.strAttr())
    for css, htmlObj in self.vals:
      if css == '':
        strAttr = ";".join(["%s:%s" % (key, val) for key, val in self.cssRow.items()])
        res.add(1, '<div style="%s">%s</div>' % (strAttr, htmlObj))
      else:
        res.add(1, '<div class="%s">%s</div>' % (css, htmlObj))
      htmlObj.graph()
    res.add(0, '</div>')
    if self.aresObj.withContainer:
      return str(TextContainer(self.aresObj, str(res)))

    return str(res)


class Col(AresHtml.Html):
  """

  """
  alias = 'col'

  def __str__(self):
    """ Return the HTML display of a split container"""
    res = AresItem.Item('')
    for htmlObj in self.vals:
      res.add(1, str(htmlObj))
      htmlObj.graph()
    return str(res)


class Vignet(AresHtml.Html):
  """
  Vignet to display a value for a given recordset.
  This Vignet can be
  """

  cssCls, alias = ['panel', 'panel-success'], 'vignet'

  def __init__(self, aresObj, title, content, recordSet, fnc=None, col=None, cssCls=None, cssAttr=None):
    vals = recordSet if fnc is None else fnc(recordSet, col)
    super(Vignet, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.title = title
    self.text = content

  def __str__(self):
    res = AresItem.Item("<p>%s</p>" % self.text)
    res.add(1, "<p><h1><center>%s</center></h1></p>" % self.vals)
    res.add(0, "</div>")
    box = AresBox(self.htmlId, res, self.title, properties=self.references)
    box.cssCls = self.cssCls
    return str(box)


class AresBox(AresHtml.Html):
  """ Internal object cannot be used directly from ares.py """
  cssCls = ['panel', 'ares-panel-success']
  references = ['http://astronautweb.co/snippet/font-awesome/']

  def __init__(self, htmlId, vals, headerBox, properties=None):
    """  """
    self.idContainer = htmlId
    self.vals = vals
    self.headerBox = headerBox
    self.prop = properties

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    return "win_%s" % self.idContainer

  def __str__(self):
    """  Return the HTML representation of the Box objects """
    item = AresItem.Item('<div class="%s" id="%s_main" style="margin-top:10px">' % (" ".join(self.cssCls), self.htmlId))
    item.add(1, '<div class="ares-panel-heading">')
    item.add(2, '<strong><i class="fa fa-table" aria-hidden="true"></i>&nbsp;%s</strong>' % self.headerBox)
    item.add(3, '<button class="btn btn-xs " id="%s_close" name="ares_close"></button>' % self.htmlId)
    item.add(3, '<button class="btn btn-xs" id="%s_min" name="ares_min"></button>' % self.htmlId)
    if self.prop is not None:
      item.add(3, '<button class="btn btn-xs" name="ares_prop" data-toggle="modal" data-target="#%s_prop"></button>' % self.htmlId)
    item.add(1, '</div>')
    item.add(1, '<div class="panel-body table-responsive" id="%s" style="padding:8px">' % self.htmlId)
    item.add(2, self.vals)
    item.add(1, '</div>')
    item.add(0, '</div>')
    if self.prop is not None:
      item.add(0, '<div class="modal fade" id="%s_prop" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">' % self.htmlId)
      item.add(1, '<div class="modal-dialog" role="document">')
      item.add(1, '<div class="modal-content">')
      item.add(1, '<div class="modal-header">')
      item.add(1, '<h5 class="modal-title" id="exampleModalLabel">Html / Js documentation</h5>')
      item.add(1, '</div>')
      item.add(1, '<div class="modal-body">')
      for prop in self.prop:
        item.add(0, '<a href="%s" target="_blank">%s</a>' % (prop, prop))
      item.add(1, '</div>')
      item.add(1, '</div>')
      item.add(1, '</div>')
      item.add(0, '</div>')
    return str(item)



