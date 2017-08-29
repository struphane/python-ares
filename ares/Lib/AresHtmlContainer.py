""" Python Module to define all the HTML Containers

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs

class Div(AresHtml.Html):
  """ Python Wrapper for a simple DIV tag """
  reference = 'https://www.w3schools.com/tags/tag_div.asp'
  alias = 'div'

  def __str__(self):
    """ Return the HMTL object of for div """
    return '<div %s>%s</div>' % (self.strAttr(), self.vals)

  @property
  def val(self):
    """ Return the Javascript Value """
    return '$("#%s").html()' % self.htmlId

  def onLoadFnc(self):
    """ Activate the Jquery tooltips display """
    return "$( function() { $( document ).tooltip() ; }) ;"

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.div("MyDiv")


class IFrame(AresHtml.Html):
  """ Python Wrapper for an iFrame object"""

  reference = 'https://www.w3schools.com/TAgs/tag_iframe.asp'
  alias = 'iframe'
  default = {'width': '1000px', 'height': '700px', 'margin': 'auto 0', 'display': 'block'}

  def addStyle(self, name, value):
    """ Add the style to the Title object """
    if self.style is None:
      self.style = dict(self.default)
    self.style[name] = value

  def __str__(self):
    """ Return an iFrame Tag """
    if not hasattr(self, 'style'):
      self.style = dict(self.default)
    styleStr = ";".join(["%s:%s" % (key, val) for key, val in self.style.items()])
    return '''<iframe src="%s" style=%s">  
    <p>Your browser does not support iframes.</p>
    </iframe>''' % (self.vals, styleStr)


class ListBadge(AresHtml.Html):
  """
  HTML List

  This object will return a HTML list and the constructor of this class is
  expecting in the values a list of tuples. The first one should be the
  name and the second the count to be displayed in the badge

  Default class parameters
    - CSS Default Class = list-group
  """
  cssCls = 'list-group'
  reference = 'https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp'
  alias = 'listbadge'

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
  cssCls, alias = 'container-fluid', 'container'
  reference = 'https://getbootstrap.com/docs/3.3/css/'

  def __init__(self, htmlId, header, vals, cssCls=None):
    """  """
    super(Container, self).__init__(htmlId, vals, cssCls)
    self.headerBox = header

  def __str__(self):
    """ Return the String representation of a HTML List """
    item = AresItem.Item('<div class="panel panel-success">') #% self.strAttr())
    item.add(2, '<div class="panel-heading"><strong><i class="fa fa-table" aria-hidden="true"></i>&nbsp;%s</strong></div>' % self.headerBox)
    item.add(2, '<div class="panel-body">')
    for val in self.vals:
      item.add(3, val)
    item.add(2, '</div>')
    item.add(1, '</div>')
    return str(item)

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
  cssCls = 'panel-body span4'
  width, height = 100, 400
  reference = 'https://www.w3schools.com/html/html5_svg.asp'
  icon = 'fa fa-pie-chart'
  categories, values = None, None

  def __str__(self):
    """ Return the String representation of a DIV containing a SVG tag """
    item = AresItem.Item('<div class="panel panel-success" style="width:%s%%;height:%spx;">' % (self.width, self.height))
    item.add(1, '<div class="panel-heading"><strong><i class="%s" aria-hidden="true"></i>&nbsp;%s</strong></div>' % (self.icon, self.headerBox))
    item.add(1, '<div style="width:95%%;height:95%%;" %s>' % self.strAttr())

    # Add the pointers for the display
    if self.categories is not None:
      item.join(self.categories)
    if self.values is not None:
      item.join(self.values)

    item.add(1, '<svg style="width:100%;height:100%;"></svg>')
    item.add(0, '</div>')
    item.add(0, '</div>')
    return str(item)

  def selectCategory(self, selectedCategory, categories, pyDataSrc):
    """ Return the category to be selected in the graph display """
    item = AresItem.Item('Category')
    item.add(2, '<select id="%s_col_selector" class ="selectpicker">' % self.htmlId)
    for cat in categories:
      if selectedCategory == cat:
        item.add(3, '<option selected>%s</option>' % cat)
      else:
        item.add(3, '<option>%s</option>' % cat)
    item.add(2, '</select>')
    self.categories = item
    self.jsEvent['cat-change'] = AresJs.JQueryEvents("%s_col_selector" % self.htmlId, "$('#%s_col_selector')" % self.htmlId,
                                                     'change', self.update(pyDataSrc.getData()), '')

  def selectValues(self, selectedValue, values, pyDataSrc):
    """ Return the value to be selected in the graph display """
    item = AresItem.Item('Value')
    item.add(2, '<select id="%s_val_selector" class ="selectpicker">' % self.htmlId)
    for val in values:
      if selectedValue == val:
        item.add(3, '<option selected>%s</option>' % val)
      else:
        item.add(3, '<option>%s</option>' % val)
    item.add(2, '</select>')
    self.values = item
    self.jsEvent['val-change'] = AresJs.JQueryEvents("%s_val_selector" % self.htmlId, "$('#%s_val_selector')" % self.htmlId,
                                                     'change', self.update(pyDataSrc.getData()), '')

  @property
  def jqId(self):
    """ Returns the javascript SVG reference """
    return '$("#%s svg")' % self.htmlId

  @property
  def jqCategory(self):
    """ Returns the selected category for the graph """
    return '$("#%s_col_selector option:selected").text()'% self.htmlId

  @property
  def jqValue(self):
    """ Return the selected value to use for the graph """
    return '$("#%s_val_selector option:selected").text()' % self.htmlId


class Network(AresHtml.Html):
  """
  Wrapper to create a Network graph container

  Default class parameters
    - CSS Default Class = container-fluid
  """
  dim = None
  cssCls = 'container-fluid'

  def __str__(self):
    """ Return the Graph container for D3 and DVD3 """
    items = AresItem.Item('<div %s>' % self.strAttr())
    items.add(1, '<div class="row">')
    items.add(2, '<div id="graph-container">')
    items.add(3, '<div id="graph-bg"></div>')
    items.add(3, '<div id="graph"></div>')
    items.add(2, '%s%s</div>')
    items.add(1, '</div>')
    items.add(0, '</div>')
    return str(items)


class Tabs(AresHtml.Html):
  """
  Python wrapper for a multi Tabs component

  Default class parameters
    - CSS Default Class = nav nav-tabs
    - title = Home
  """
  alias = 'tabs'
  cssCls = 'nav nav-tabs'

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


class Image(AresHtml.Html):
  """
  Python wrapper for a multi Tabs component

  Default class parameters
    - CSS Default Class = nav nav-tabs
    - title = Home
  """
  alias =  'img'
  cssCls = 'img-responsive'
  reference = 'https://www.w3schools.com/bootstrap/bootstrap_ref_css_images.asp'
  doubleDots = 1

  def __str__(self):
    """ Return the HTML representation of a Tabular object """
    doubleDotsPath = "/".join([".." for i in range(self.doubleDots)])
    return ' <img src="%s/static/images/%s" class="img-responsive" %s> ' % (doubleDotsPath, self.vals, self.strAttr())

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.img("../../../static/images/sample_img.jpg")


class Row(AresHtml.Html):
  """

  """
  cssCls, alias = "row", 'row'
  gridCss = 'panel panel-success'
  reference = 'https://getbootstrap.com/docs/3.3/css/'

  def __init__(self, htmlId, hltmObjs, cssCls=None):
    if len(hltmObjs) > 3:
      raise Exception('Row object can only display maximum 3 components')

    if len(hltmObjs) == 3:
      vals = [('col-6 col-md-4', htmlObj) for htmlObj in hltmObjs]
    elif len(hltmObjs) == 2:
      vals = [('col-xs-6', htmlObj) for htmlObj in hltmObjs]
    super(Row, self).__init__(htmlId, vals, cssCls)

  def extend(self, component):
    """ Extend one of the objects on to columns """
    tempVals = []
    for size, htmlOjb in self.vals:
      if component.htmlId == htmlOjb.htmlId:
        tempVals.append(('col-xs-12 col-md-8', htmlOjb))
      else:
        tempVals.append(('col-xs-6 col-md-4', htmlOjb))
    self.vals = tempVals

  def __str__(self):
    """ Return the HTML display of a split container"""
    res = AresItem.Item('<div %s>' % self.strAttr())
    for css, htmlObj in self.vals:
      res.add(1, '<div class="%s">%s</div>' % (css, htmlObj))
    res.add(0, '</div>')
    return str(res)

  def jsEvents(self, jsEventFnc=None):
    """ Function to get the Javascript methods for this object and all the underlying objects """
    if jsEventFnc is None:
      jsEventFnc = self.jsEventFnc
    for jEventType, jsEvent in self.jsEvent.items():
      jsEventFnc[jEventType].add(str(jsEvent))
    for _, val in self.vals:
      if hasattr(val, 'jsEvent'):
        getattr(val, 'jsEvents')(jsEventFnc)
    return jsEventFnc

  def onLoad(self, loadFnc=None):
    """ Functions to get all the onload items for this object and all the underlying object """
    if loadFnc is None:
      loadFnc = self.jsOnLoad
    fnc = self.onLoadFnc()
    if fnc is not None:
      loadFnc.add(fnc)
    for _, val in self.vals:
      if hasattr(val, 'onLoad'):
        getattr(val, 'onLoad')(loadFnc)
    return loadFnc


class Vignet(AresHtml.Html):
  """
  Vignet to display a value for a given recordset.
  This Vignet can be
  """

  cssCls, alias = "panel panel-success", 'vignet'

  def __init__(self, htmlId, title, content, recordSet, fnc, col, cssCls=None):
    vals = fnc(recordSet, col)
    super(Vignet, self).__init__(htmlId, vals, cssCls)
    self.title = title
    self.text = content

  def __str__(self):
    res = AresItem.Item('<div %s style="padding:5px">' % self.strAttr())
    res.add(1, "<p><strong>%s</strong></p>" % self.title)
    res.add(1, "<p>%s</p>" % self.text)
    res.add(1, "<p><h1><center>%s</center></h1></p>" % self.vals)
    res.add(0, "</div>")
    return str(res)


if __name__ == '__main__':
  obj = Tabs(0, ['!', '2'])
  print(obj)


