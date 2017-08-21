""" Python Module to define all the HTML component dedicated to display plain text

"""

import json
import locale

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Text(AresHtml.Html):
  """ Python Wrapper to the FONT HTNL Tag """
  reference = 'https://www.w3schools.com/tags/tag_font.asp'
  alias = 'text'
  htmlComp = None

  def __init__(self, htmlId, vals, cssCls=None, htmlComp=None):
    super(Text, self).__init__(htmlId, vals, cssCls)
    self.htmlComp = htmlComp

  def __repr__(self):
    """ Return the String representation of a Text HTML tag """
    html = '<font %s>%s</font>' % (self.strAttr(), self.vals)
    if self.htmlComp is not None:
      html = html.format(*self.htmlComp)
    return html

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.text("My dummy text")


class Code(AresHtml.Html):
  """ Python Wrapper to the Bootsrap CODE Tag """
  reference = 'https://v4-alpha.getbootstrap.com/content/code/'
  alias = 'code'
  htmlComp = None

  def __init__(self, htmlId, vals, cssCls=None, htmlComp=None):
    super(Code, self).__init__(htmlId, vals, cssCls)
    self.htmlComp = htmlComp

  def __repr__(self):
    """ Return the String representation of a Code HTML tag """
    html = '<pre><code %s>%s</code></pre>' % (self.strAttr(), self.vals)
    if self.htmlComp is not None:
      html = html.format(*self.htmlComp)
    return html

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.code("def myFct(): pass")


class Paragraph(AresHtml.Html):
  """ Python Wrapper to the HTML P Tag """
  reference = "https://www.w3schools.com/html/html_styles.asp"
  alias = 'paragraph'
  htmlComp = None

  def __init__(self, htmlId, vals, cssCls=None, htmlComp=None):
    super(Paragraph, self).__init__(htmlId, vals, cssCls)
    self.htmlComp = htmlComp

  def __repr__(self):
    """ Return the String representation of a Code HTML tag """
    val = " ".join([str(val) for val in self.vals]) if isinstance(self.vals, list) else self.vals
    html = '<p %s>%s</p>' % (self.strAttr(), val)
    if self.htmlComp is not None:
      html = html.format(*self.htmlComp)
    return html

  @classmethod
  def aresExample(cls, aresObj):
    aresObj.text("My text")
    return aresObj.paragraph("My Paragraph")


class Title(AresHtml.Html):
  """ Python Wrapper to the HTML H1 Tag """
  dim, alias = 1, 'title'
  default = {'color': '#398438', 'font-family': 'anchorjs-icons', 'font-style': 'normal', 'font-varian': 'normal', 'font-weight': 'normal', 'line-height': 'inherit'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'

  def addStyle(self, name, value):
    """ Add the style to the Title object """
    if self.style is None:
      self.style = dict(self.default)
    self.style[name] = value

  def __repr__(self):
    """ Return a header HTML Tag """
    if not hasattr(self, 'style'):
      self.style = dict(self.default)
    styleStr = ";".join(["%s:%s" % (key, val) for key, val in self.style.items()])
    items = AresItem.Item('<H%s class="page-header" %s style="%s">' % (self.dim, self.strAttr(), styleStr))
    items.add(1, '<a class="anchorjs-link " style="%s">%s</a>' % (styleStr, self.vals))
    items.add(0, '</H%s>' % self.dim)
    return str(items)

  def onLoadFnc(self):
    """ Activate the Jquery Tooltips """
    return "$( document ).tooltip();"

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title("Level 1 Title")


class Title2(Title):
  """ Python Wrapper to the HTML H2 Tag """
  dim, alias = 2, 'title2'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title2("Level 2 Title")


class Title3(Title):
  """ Python Wrapper to the HTML H3 Tag """
  dim, alias = 3, 'title3'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title3("Level 3 Title")


class Title4(Title):
  """ Python Wrapper to the HTML H4 Tag """
  dim, alias = 4, 'title4'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.title4("Level 4 Title")


class Newline(AresHtml.Html):
  """ Python Wrapper to the HTML BR tag """
  reference = 'https://www.w3schools.com/tags/tag_br.asp'
  alias = 'newline'

  def __repr__(self):
    """ Return the String representation of a new line tag """
    return '<br />'

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.newline()


class Line(AresHtml.Html):
  """ Python Wrapper to the HTML HR tag """
  reference = 'https://www.w3schools.com/tags/tag_hr.asp'
  alias = 'line'

  def __repr__(self):
    """ Return the String representation of a line tag """
    return '<hr %s/><hr %s/>' % (self.strAttr(), self.strAttr())

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.line()


class Icon(AresHtml.Html):
  """
  """
  reference = 'http://fontawesome.io/icons/'
  alias = 'icon'

  def __repr__(self):
    """ Return the String representation of a line tag """
    return '<i class="fa fa-%s" style="cursor:pointer" aria-hidden="true" %s></i>' % (self.vals, self.strAttr())

  def deleteLink(self, reportName, fileName, folders):
    """ Delete the file or the folder in the dedicated folder """
    if fileName is None:
      self.post('click', "../delete_folder/%s" % reportName, json.dumps({'SOURCE_PATH': "/".join(folders)}), 'location.reload();')
    else:
      self.post('click', "../delete_file/%s" % reportName, json.dumps({'SOURCE_PATH': "/".join(folders), 'FILE_NAME': fileName}), 'location.reload();')
    return self


class Numeric(AresHtml.Html):
  """ Reprsents a figure in a nice display """
  alias = 'number'
  reference = ''

  def __repr__(self):
    """ Return the String representation of a line tag """
    locale.setlocale(locale.LC_ALL, '')
    html = "<font %s>{:,d}/font>" % self.strAttr()
    return html.format(self.vals)

if __name__ == '__main__':
  obj = Title(0, 'Reports Environment (Beta)')
  #print(obj.jsEvents())
  print('\n'.join(obj.onLoad()))
  #print(obj.__repr__())

  Numeric(1, 34455656)
  objText = Paragraph(0, "Youpi {0}", htmlComp=[Numeric(1, 34455656)])
  print(objText.__repr__())
