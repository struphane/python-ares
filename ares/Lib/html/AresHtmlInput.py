"""


"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs


class InputText(AresHtml.Html):
  """
  Python wrapper to the HTML INPUT component

  Input value should be a String

  Default class parameters
    - CSS Default Class = form-control
  """
  cssCls, alias = ['form-control'], 'input'
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap']
  inputType = "text"
  css = {'width': '100%', 'height': '32px'}

  def autocomplete(self, values):
    """ Fill the auto completion box with a data source """
    self.jsEvent['autocomplete'] = AresJs.JQueryEvents(self.htmlId, self.jqId, 'autocomplete', 'source: %s' % values)

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.attr['value'] = dflt

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return '%s.val()' % self.jqId

  def __str__(self):
    """ Return the String representation of a HTML Input object """
    self.attr['type'] = self.inputType
    item = AresItem.Item('<div class="form-group">', self.incIndent)
    item.add(1, '<label for="%s">%s:</label>' % (self.vals.replace(" ", "").lower(), self.vals))
    item.add(2, '<input %s>' %  self.strAttr())
    item.add(0, '</div>')
    return str(item)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.input("Input text...")


class InputInt(InputText):
  """ """
  references = ['https://www.alsacreations.com/tuto/lire/1409-formulaire-html5-type-number.html']
  inputType = "number"


class InputRange(InputText):
  """ """
  references = ['https://www.alsacreations.com/tuto/lire/1410-formulaire-html5-type-range.html']
  inputType = "range"


class DatePicker(AresHtml.Html):
  """
  Wrapper to a Jquery Date picker object

  This component is built with
    - P
    - INPUT

  """
  references = ['https://jqueryui.com/datepicker/']
  alias = 'date'
  cssCls = ['datepicker']
  dflt = ''
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.dflt = dflt

  def __str__(self):
    """ Return the String representation of a Date picker object """
    if '-' in self.dflt:
      return '<p><strong>%s: </strong><input type="text" %s value="%s"></p>' % (self.vals, self.strAttr(), self.dflt)
    return '<p><strong>%s: </strong><input type="text" style="width:100%%;height:32px" %s></p>' % (self.vals, self.strAttr())

  def onLoadFnc(self):
    """ Start the Date picker transformation when the document is loaded """
    return AresItem.Item.indents(2, "$( function() {%s.datepicker({dateFormat: 'yy-mm-dd'} ); } );" % self.jqId)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.date()
