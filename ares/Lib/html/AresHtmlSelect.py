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
        hyperLinkVal = hyperlink if hyperlink is not None else '#'
        if (hyperlink, value) in self.disableItems:
          items.add(level, '<li><a class="dropdown-item disabled" tabindex="-1" href="%s">%s</a></li>' % (hyperLinkVal, value))
        else:
          items.add(level, '<li><a class="dropdown-item" tabindex="-1" href="%s">%s</a></li>' % (hyperLinkVal, value))

  def disable(self, value, hyperlink):
    """ Disable an item from the dropdown box """
    self.disableItems[(hyperlink, value)] = True

  @property
  def jqId(self):
    """
    Property to get the Jquery ID of a python HTML object
    The use of ' instead of " is because the dumps will add some \ and it will not be correctly taken into account
    by the javascript layer
    """
    return "$('#%s > li a').not('.drilldown, .disabled')" % self.htmlId

  def __str__(self):
    """  String representation of a Drop Down item """
    items = AresItem.Item('<div class="dropdown">')
    items.add(1, '<button class="%s" type="button" data-toggle="dropdown">%s' % (self.getClass(), self.title))
    items.add(3, '<span class="caret"></span>')
    items.add(2, '</button>')
    items.add(1, '<ul class="dropdown-menu" id="%s">' % self.htmlId)
    self.addCategory(items, 2, self.vals)
    items.add(1, "</ul>")
    items.add(0, "</div>")
    return str(items)

  def click(self, htmlObject):
    """ Change the component to use javascript functions """
    evenType = 'click'
    jsDef = "console.log($(this).text()) ;" #% self.htmlId
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType,jsDef)

  def onLoadFnc(self):
    """ """
    return '''
              $('.dropdown-submenu a.drilldown').on("click", function(e){
                $(this).next('ul').toggle();
                e.stopPropagation();
                e.preventDefault();
              });
           '''