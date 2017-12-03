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

  def replace(self, htmlObj):
    """ To add a button to hide th """

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.div("MyDiv")

  def jsUpdate(self, data=''):
    """ """
    return '$("#%s").html(%s)' % (self.htmlId, data)

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
    self.cssRow = {"text-align": "center", "width": "100%", 'display': 'inline-block', "padding": "20%"}
    if len(hltmObjs) >= 5:
      vals = [('col-md-2', htmlObj) for htmlObj in hltmObjs]
    elif len(hltmObjs) == 4:
      vals = [('col-md-3 col-sm-6 col-xs-12', htmlObj) for htmlObj in hltmObjs]
    elif len(hltmObjs) == 3:
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
  __cssCls = ['panel', 'ares-panel-success']
  references = ['http://astronautweb.co/snippet/font-awesome/']

  def __init__(self, htmlId, vals, headerBox, properties=None):
    """  """
    self.idContainer = htmlId
    self.vals = vals
    self.headerBox = headerBox
    self.prop = properties
    self.cssAttr = {'margin-top': '10px'}
    self.cssCls = list(self.__cssCls)

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    return "win_%s" % self.idContainer

  def __str__(self):
    """  Return the HTML representation of the Box objects """
    attr = 'style="%s"' % ";".join(["%s:%s" % (key, val) for key, val in self.cssAttr.items()])
    item = AresItem.Item('<div class="%s" id="%s_main" %s>' % (" ".join(self.cssCls), self.htmlId, attr))
    item.add(1, '<div class="ares-panel-heading">')
    item.add(2, '<strong><i class="fa fa-table" aria-hidden="true"></i>&nbsp;%s</strong>' % self.headerBox)
    item.add(3, '<button class="btn btn-xs " id="%s_close" name="ares_close"></button>' % self.htmlId)
    item.add(3, '<button class="btn btn-xs" id="%s_min" name="ares_min"></button>' % self.htmlId)
    item.add(3, '<button class="btn btn-xs " id="%s_zoom" name="ares_zoom" onclick="ZoomIn(\'%s\', \'%s\')"></button>' % (self.htmlId, self.htmlId, self.idContainer))
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

