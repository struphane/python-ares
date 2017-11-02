""" Python Wrapper for the Radio items
@author: Olivier Nogues

"""

import json
from ares.Lib import AresHtml
from ares.Lib import AresItem

import re
regex = re.compile('[^a-zA-Z0-9_]')


class Radio(AresHtml.Html):
  """

  """
  alias, cssCls = 'radio', None
  references = ['https://www.w3schools.com/bootstrap/bootstrap_forms_inputs.asp']
  reqCss = ['bootstrap', 'font-awesome']
  reqJs = ['bootstrap', 'jquery']

  def __init__(self, aresObj, recordSet, col=None, cssCls=None, cssAttr=None, internalRef=None):
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
    self.internalRef = internalRef
    # To replace non alphanumeric characters https://stackoverflow.com/questions/20864893/javascript-replace-all-non-alpha-numeric-characters-new-lines-and-multiple-whi
    #.replace(/\W+/g, '')
    self.jsFrg = ["radio_val_%s = '$(this).text().trim()';" % self.htmlId]

  @property
  def htmlId(self):
    """ Property to get the HTML ID of a python HTML object """
    if self.internalRef is not None:
      return self.internalRef

    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  def setDefault(self, value):
    """ Set a selected default value """
    self.selected = regex.sub('', value.strip())
    self.aresObj.jsGlobal.add("radio_val_%s = '%s';" % (self.htmlId, self.selected))

  def select(self, val):
    """ Change the selected value """
    self.selected = regex.sub('', val.strip())
    self.aresObj.jsGlobal.add("radio_val_%s = '%s'" % (self.htmlId, self.selected))

  def __str__(self):
    """ Return a basic HTML radio component """
    items = AresItem.Item('<div %s class="btn-group" data-toggle="buttons">' % self.strAttr(False))
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

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return "radio_val_%s" % self.htmlId

  def jsFnc(self, js):
    """ Pure Javascript method to update other components in the page """
    self.js('mouseup', "radio_val_%s = $(event.currentTarget).text().trim(); %s" % (self.htmlId, js))

  def click(self, htmlObjects):
    """ Pure Javascript method to update other components in the page """
    evenType = 'mouseup'
    jsDef = ["radio_val_%s = $(event.currentTarget).text().trim();" % self.htmlId]
    for htmlObject in htmlObjects:
      jsDef.append(htmlObject.jsUpdate())
    self.js(evenType, "\n".join(jsDef))

  def link(self, jsEvent):
    """ Change the component to use javascript functions """
    jsFrg = list(self.jsFrg)
    jsFrg.append(jsEvent)
    self.js('mouseup', ";".join(jsFrg))