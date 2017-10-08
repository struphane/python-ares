"""

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs

class SelectDropDown(AresHtml.Html):
  """

  """
  alias, cssCls = 'dropdown', None
  references = ['http://getbootstrap.com/docs/4.0/components/dropdowns/']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def __init__(self, aresObj, title, vals, cssCls=None, cssAttr=None):
    """ Instantiate the Drop Down button """
    super(SelectDropDown, self).__init__(aresObj, list(vals), cssCls, cssAttr)
    self.title = title

  def addCategory(self, items, level, vals):
    """ """
    for value, hyperlink in vals:
      if isinstance(hyperlink, list):
        items.add(level, '<li class="dropdown-submenu"><a tabindex="-1" href="#">%s</a><ul class="dropdown-menu">' % value)
        self.addCategory(items, level+1, hyperlink)
        items.add(level, '</ul></li>')
      else:
        items.add(level, '<li><a tabindex="-1" href="%s">%s</a></li>' % (hyperlink, value))


  def __str__(self):
    """  """
    items = AresItem.Item('<div class="dropdown">')
    items.add(1, '<button class="btn btn-default" type="button" data-toggle="dropdown">%s' % self.title)
    items.add(2, '<span class="caret"></span>')
    items.add(2, '</button>')
    items.add(1, '<ul class="dropdown-menu">')
    self.addCategory(items, 2, self.vals)
    items.add(1, "</ul>")
    items.add(0, "</div>")
    return str(items)