"""

"""

from ares.Lib import AresHtml


class Hr(AresHtml.Html):
  """ HTML object for the HR tags """
  cssCls, alias = ['table'], 'table'
  __css = {'display': 'block', 'margin-top': '1.5em', 'margin-bottom': '2.5em',
           'margin-left': 'auto', 'margin-right': 'auto', 'border-style': 'inset',
           'border-width': '1px', 'color': '#398438', 'box-shadow': '0 0 10px 1px #398438'}
  references = ['https://www.w3schools.com/tags/tag_hr.asp']

  def __str__(self):
    return '<hr %s/>' % self.strAttr()


class Newline(AresHtml.Html):
  """ Python Wrapper to the HTML BR tag """
  references = ['https://www.w3schools.com/tags/tag_br.asp']
  alias = 'newline'

  def __str__(self):
    """ Return the String representation of a new line tag """
    return '<br />'


