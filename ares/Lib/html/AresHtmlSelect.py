"""

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs

class SelectDropDown(AresHtml.Html):
  """

  """
  alias, cssCls = 'dropdown', ['btn', 'btn-success']
  references = ['http://getbootstrap.com/docs/4.0/components/dropdowns/']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def __init__(self, aresObj, title, vals, cssCls=None, cssAttr=None):
    """ Instantiate the Drop Down button """
    super(SelectDropDown, self).__init__(aresObj, list(vals), cssCls, cssAttr)
    self.title = title
    self.disableItems = {}

  def addCategory(self, items, level, vals):
    """ Add recursively the sub categories """
    for value, hyperlink in vals:
      if isinstance(hyperlink, list):
        items.add(level, '<li class="dropdown-submenu"><a href="#" class="drilldown">%s<span class="caret"></span></a>' % value)
        items.add(level, '<ul class="dropdown-menu">')
        self.addCategory(items, level+1, hyperlink)
        items.add(level, '</ul></li>')
      else:
        if (hyperlink, value) in self.disableItems:
          items.add(level, '<li><a class="dropdown-item disabled" tabindex="-1" href="%s">%s</a></li>' % (hyperlink, value))
        else:
          items.add(level, '<li><a class="dropdown-item" tabindex="-1" href="%s">%s</a></li>' % (hyperlink, value))

  def disable(self, value, hyperlink):
    """ Disable an item from the dropdown box """
    self.disableItems[(hyperlink, value)] = True

  def __str__(self):
    """  String representation of a Drop Down item """
    items = AresItem.Item('<div class="dropdown">')
    items.add(1, '<button %s type="button" data-toggle="dropdown">%s' % (self.strAttr(), self.title))
    items.add(2, '<span class="caret"></span>')
    items.add(2, '</button>')
    items.add(1, '<ul class="dropdown-menu">')
    self.addCategory(items, 2, self.vals)
    items.add(1, "</ul>")
    items.add(0, "</div>")
    return str(items)