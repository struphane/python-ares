"""

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from flask import render_template_string


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
    self.jsFrg = ['%s = $(this).text().trim();' % self.htmlId]

  def setDefault(self, value):
    """ Set a selected default value """
    self.aresObj.jsGlobal.add("%s = '%s';" % (self.htmlId, value))

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return self.htmlId

  def addCategory(self, items, level, vals):
    """ Add recursively the sub categories """
    for value, hyperlink in vals:
      if value is None:
        # Special keywork to put a delimiter
        # or a header if the hyperlink information is not None
        if hyperlink is not None:
          items.add(level, '<h6 class="dropdown-header">%s</h6>' % hyperlink)
        else:
          items.add(level, '<div class="dropdown-divider"></div>')
        continue

      if isinstance(hyperlink, list):
        items.add(level, '<li class="dropdown-submenu">')
        items.add(level, '<a href="#" class="dropdown-toggle dropdown-item" data-toggle="dropdown">%s</a>' % value)
        items.add(level, '<ul class="dropdown-menu">')
        self.addCategory(items, level+1, hyperlink)
        items.add(level, '</ul></li>')
      else:
        hyperLinkVal = hyperlink if hyperlink is not None else '#'
        if (hyperlink, value) in self.disableItems:
          items.add(level, '<li><a class="dropdown-item disabled" href="%s">%s</a></li>' % (hyperLinkVal, value))
        else:
          items.add(level, '<li><a class="dropdown-item" href="%s">%s</a></li>' % (hyperLinkVal, value))

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

  def link(self, jsEvent):
    """ Change the component to use javascript functions """
    self.jsFrg.append(jsEvent)
    self.js('click', ";".join(self.jsFrg))


class SelectDropDownAjax(SelectDropDown):
  """
  This object will allow you to interact with the data and to request new set of data.
  This will not work locally, in order to get something locally you need to change your object to be a
  simple SelectDropDown


  """
  alias, cssCls = 'ajaxDropdown', ['btn', 'btn-success']
  references = ['http://getbootstrap.com/docs/4.0/components/dropdowns/']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def targetScript(self, script):
    self.script = script

  def click(self, htmlObjects):
    """ Call the ajax service and update the corresponding objects on the page """
    url = render_template_string("{{ url_for( 'ares.ajaxCall', report_name='%s', script='%s' ) }}" % (self.aresObj.http["REPORT_NAME"], self.script))
    self.js('click', '''$.ajax({url: '%s',
          success: function(result){var resultObj = JSON.parse(result);$('#%s').html(resultObj['data']); }});''' % (url, htmlObjects[0].htmlId))