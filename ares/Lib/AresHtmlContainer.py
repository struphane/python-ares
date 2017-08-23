""" Python Module to define all the HTML Containers

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Div(AresHtml.Html):
  """ Python Wrapper for a simple DIV tag """
  reference = 'https://www.w3schools.com/tags/tag_div.asp'
  alias = 'div'

  def __repr__(self):
    """ Return the HMTL object of for div """
    return '<div %s>%s</div>' % (self.strAttr(), self.vals)

  @property
  def val(self):
    """ Return the Javascript Value """
    return '$("#%s").html()' % self.htmlId

  def onLoadFnc(self):
    """ Activate the Jquery tooltips display """
    return "$( document ).tooltip();"

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

  def __repr__(self):
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

  def __repr__(self):
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

  def __repr__(self):
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


class Split(AresHtml.Html):
  """
  Wrapper for a bootstrap Grid

  This container will allow users to display object on the same line
  It is perfect to encapsulate other HTML object

  For example
    ['A', 'B']

  Default class parameters
    - cssCls = container-fluid
    - col_lg = 6
  """
  cssCls, alias = "container-fluid", 'grid'
  gridCss = 'panel panel-success'
  col_lg = 6
  reference = 'https://getbootstrap.com/docs/3.3/css/'

  def __repr__(self):
    """ Return the HTML display of a split container"""
    res = AresItem.Item('<div %s>' % 'class="%s"' % self.gridCss if self.gridCss is not None else '')
    res.add(1, '<div %s>' % self.strAttr())
    res.add(1, '<BR/><div class="row">')
    for htmObj in self.vals:
      res.add(2, '<div class="col-lg-%s">' % self.col_lg)
      res.add(3, str(htmObj))
      res.add(2, '</div>')
    res.add(1, '</div>')
    res.add(0, '</div>')
    res.add(0, '</div>')
    return str(res)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.grid(['A', 'B'])


class GraphSvG(AresHtml.Html):
  """
  Python Wrapper to a DIV tag with a SVG

  Default class parameters
    - CSS Default Class = span4 (for the DIV component)
    - width, height = 960, 500 (for the SVG component)
  """
  cssCls = 'span4'
  width, height = 100, 400
  reference = 'https://www.w3schools.com/html/html5_svg.asp'
  icon = 'fa fa-pie-chart'

  def __repr__(self):
    """ Return the String representation of a DIV containing a SVG tag """
    item = AresItem.Item('<div class="panel panel-success" style="width:%s%%;height:%spx;">' % (self.width, self.height))
    item.add(1, '<div class="panel-heading"><strong><i class="%s" aria-hidden="true"></i>&nbsp;%s</strong></div>' % (self.icon, self.headerBox))
    item.add(1, '<div class="panel-body" style="width:100%%;height:100%%;" %s>' % self.strAttr())
    item.add(1, '<svg style="width:100%;height:100%;"></svg>')
    item.add(0, '</div>')
    item.add(0, '</div>')
    return str(item)

  @property
  def jqId(self):
    """ Return the javascript SVG reference """
    return '$("#%s svg")' % self.htmlId


class Graph(AresHtml.Html):
  """
  Wrapper to create a graph container

  Default class parameters
    - CSS Default Class = span4 (for the DIV component)
  """
  cssCls = 'span4'
  reference = 'http://getbootstrap.com/2.3.2/scaffolding.html'

  def __repr__(self):
    """ Return the Graph container for D3 and DVD3 """
    return '<div %s></div>\n' % self.strAttr()


class Network(AresHtml.Html):
  """
  Wrapper to create a Network graph container

  Default class parameters
    - CSS Default Class = container-fluid
  """
  dim = None
  cssCls = 'container-fluid'

  def __repr__(self):
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
  title, alias = 'Home', 'tabs'
  cssCls = 'nav nav-tabs'

  def __repr__(self):
    """ Return the HTML representation of a Tabular object """
    item = AresItem.Item('<ul %s>' % self.strAttr())
    item.add(1, '<li class="active"><a href="#">%s</a></li>' % self.title)
    for val in self.vals:
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

  def __repr__(self):
    """ Return the HTML representation of a Tabular object """
    doubleDotsPath = "/".join([".." for i in range(self.doubleDots)])
    return ' <img src="%s/static/images/%s" class="img-responsive" %s> ' % (doubleDotsPath, self.vals, self.strAttr())

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.img("../../../static/images/sample_img.jpg")



if __name__ == '__main__':
  obj = Tabs(0, ['!', '2'])
  print(obj)


