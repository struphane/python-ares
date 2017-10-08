"""

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs

class Radio(AresHtml.Html):
  """

  """
  alias, cssCls = 'radio', None
  references = ['https://www.w3schools.com/bootstrap/bootstrap_forms_inputs.asp']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def __init__(self, aresObj, recordSet, col=None, cssCls=None, cssAttr=None):
    """ Instantiate a Python Radio button """
    if col is not None:
      vals = set([])
      for rec in recordSet:
        if col in rec:
          vals.add(rec[col])
    else:
      vals = set(recordSet)
    super(Radio, self).__init__(aresObj, list(vals), cssCls, cssAttr)
    self.selected = None
    self.col = col

  def select(self, val):
    """ Change the selected value """
    self.selected = val
    self.aresObj.jsGlobal["radio_val_%s = %s" % (self.htmlId, val)] = True

  def __str__(self):
    """ Return a basic HTML radio component """
    items = AresItem.Item('<div class="btn-group" data-toggle="buttons">')
    for val in self.vals:
      if self.selected == val:
        items.add(1, '<label class="btn btn-success active" name="%s">' % self.htmlId)
        items.add(2, '%s<input type="radio" value="%s" checked autocomplete="off">' % (val, val))
      else:
        items.add(1, '<label class="btn btn-info" name="%s">' % self.htmlId)
        items.add(2, '%s<input type="radio" value="%s" autocomplete="off">' % (val, val))
      items.add(2, '<span class="awesomeicon fa fa-check">&nbsp;</span>')
      items.add(1, "</label>")
    items.add(0, "</div>")
    return str(items)

  @property
  def jqId(self):
    """
    Property to get the Jquery ID of a python HTML object
    The use of ' instead of " is because the dumps will add some \ and it will not be correctly taken into account
    by the javascript layer
    """
    return "$('label[name=%s]')" % self.htmlId

  #@property
  #def val(self):
  #  """ Property to get the jquery value of the HTML objec in a python HTML object """
  #  return 'getSelectRadio(event, %s)' % self.jqId

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return "radio_val_%s" % self.htmlId

  def clickTest(self, htmlObjects):
    """ Pure Javascript method to update other components in the page """
    evenType = 'mouseup'
    jsDef = "\n".join([htmlObject.jsUpdate() for htmlObject in htmlObjects])
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType,jsDef)

  def click(self, htmlObjects):
    """ Pure Javascript method to update other components in the page """
    evenType = 'mouseup'
    jsDef = ["radio_val_%s = $(event.currentTarget).text().trim();" % self.htmlId]
    for htmlObject in htmlObjects:
      jsDef.append(htmlObject.jsUpdate())
    self.jsEvent[evenType] = AresJs.JQueryEvents(self.htmlId, self.jqId, evenType, "\n".join(jsDef))