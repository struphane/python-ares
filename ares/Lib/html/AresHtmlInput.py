"""


"""

import datetime

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresHtml


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
  __css = {'width': '100%', 'height': '32px'}

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, dflt='', htmllId=None):
    super(InputText, self).__init__(aresObj, vals,  cssCls, cssAttr)
    self.value = dflt
    if htmllId is not None:
      self.htmllId = htmllId

  def autocomplete(self, values):
    """ Fill the auto completion box with a data source """
    self.js('autocomplete', 'source: %s' % values)

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return '%s.val()' % self.jqId

  @AresHtml.deprecated
  def addVal(self, val):
    self.value = val

  def __str__(self):
    """ Return the String representation of a HTML Input object """
    self.attr['type'] = self.inputType
    self.attr['value'] = self.value
    item = AresItem.Item('<div class="form-group">', self.incIndent)
    item.add(1, '<label for="%s">%s:</label>' % (self.vals.replace(" ", "").lower(), self.vals))
    item.add(2, '<input %s>' %  self.strAttr())
    item.add(0, '</div>')
    return str(item)


class InputPass(InputText):
  """ Input text box for a password """
  references = ['https://developer.mozilla.org/fr/docs/Web/HTML/Element/Input/password']
  inputType = "password"
  __css = {'width': '100%', 'height': '32px'}


class InputInt(InputText):
  """ """
  references = ['https://www.alsacreations.com/tuto/lire/1409-formulaire-html5-type-number.html']
  inputType = "number"
  __css = {'width': '100%', 'height': '32px'}


class InputRange(InputText):
  """ """
  references = ['https://www.alsacreations.com/tuto/lire/1410-formulaire-html5-type-range.html']
  inputType = "range"
  __css = {'width': '100%', 'height': '32px'}


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

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, dflt='', htmllId=None):
    super(DatePicker, self).__init__(aresObj, vals,  cssCls, cssAttr)
    if dflt == '':
      cobDate = datetime.datetime.today()
      if cobDate.weekday() in [5, 6]:
        cobDate = cobDate - datetime.timedelta(days=1)
      self.value = cobDate.strftime('%Y-%m-%d')
    else:
      self.value = dflt
    if htmllId is not None:
      self.htmllId = htmllId

  def addVal(self, dflt):
    """ Add a default value to this object """
    self.value = dflt

  def __str__(self):
    """ Return the String representation of a Date picker object """
    if '-' in self.dflt:
      return '<p><strong>%s: </strong><input type="text" %s value="%s"></p>' % (self.vals, self.strAttr(), self.value)

    return '<p><strong>%s: </strong><input type="text" style="width:100%%;height:32px" %s></p>' % (self.vals, self.strAttr())

  def onLoadFnc(self):
    """ Start the Date picker transformation when the document is loaded """
    return AresItem.Item.indents(2, "$( function() {%s.datepicker({dateFormat: 'yy-mm-dd'} ).datepicker('setDate', '%s'); } );" % (self.jqId, self.value))

