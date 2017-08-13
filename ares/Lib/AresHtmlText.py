""" Python Module to define all the HTML component dedicated to display plain text

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Text(AresHtml.Html):
  """ Python Wrapper to the FONT HTNL Tag """
  reference = 'https://www.w3schools.com/tags/tag_font.asp'
  alias = 'text'

  def __repr__(self):
    """ Return the String representation of a Text HTML tag """
    return '<font %s>%s</font>' % (self.strAttr(), self.vals)


class Code(AresHtml.Html):
  """ Python Wrapper to the Bootsrap CODE Tag """
  reference = 'https://v4-alpha.getbootstrap.com/content/code/'
  alias = 'code'

  def __repr__(self):
    """ Return the String representation of a Code HTML tag """
    return '<pre><code %s>%s</code></pre>' % (self.strAttr(), self.vals)


class Paragraph(AresHtml.Html):
  """ Python Wrapper to the HTML P Tag """
  reference = "https://www.w3schools.com/html/html_styles.asp"
  alias = 'paragraph'

  def __repr__(self):
    """ Return the HTML string for a paragraph including or not some other html object """
    val = " ".join([str(val) for val in self.vals]) if isinstance(self.vals, list) else self.vals
    return '<p %s>%s</p>' % (self.strAttr(), val)


class Title(AresHtml.Html):
  """ Python Wrapper to the HTML H1 Tag """
  dim, alias = 1, 'title'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none', 'text-align': 'center'}
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
    items = AresItem.Item('<H%s %s style="%s">' % (self.dim, self.strAttr(), styleStr))
    items.add(1, '<a style="%s">%s</a>' % (styleStr, self.vals))
    items.add(0, '</H%s>' % self.dim)
    return str(items)

  def onLoadFnc(self):
    """ Activate the Jquery Tooltips """
    return "$( document ).tooltip();"


class Title2(Title):
  """ Python Wrapper to the HTML H2 Tag """
  dim, alias = 2, 'title2'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'


class Title3(Title):
  """ Python Wrapper to the HTML H3 Tag """
  dim, alias = 3, 'title3'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'


class Title4(Title):
  """ Python Wrapper to the HTML H4 Tag """
  dim, alias = 4, 'title4'
  default = {'color': '#398438', 'cursor': 'pointer', 'text-decoration': 'none'}
  reference = 'https://www.w3schools.com/tags/tag_hn.asp'


class Newline(AresHtml.Html):
  """ Python Wrapper to the HTML BR tag """
  reference = 'https://www.w3schools.com/tags/tag_br.asp'
  alias = 'newline'

  def __repr__(self):
    """ Return the String representation of a new line tag """
    return '<br />'


class Line(AresHtml.Html):
  """ Python Wrapper to the HTML HR tag """
  reference = 'https://www.w3schools.com/tags/tag_hr.asp'
  alias = 'line'

  def __repr__(self):
    """ Return the String representation of a line tag """
    return '<hr %s/><hr %s/>' % (self.strAttr(), self.strAttr())



if __name__ == '__main__':
  obj = Title(0, 'Reports Environment (Beta)')
  #print(obj.jsEvents())
  print('\n'.join(obj.onLoad()))
  #print(obj.__repr__())
