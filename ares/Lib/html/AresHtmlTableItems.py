""" Python Module to set the underlying HTML table constituents
@Author: Olivier Nogues

"""

import json
from ares.Lib import AresHtml


class Td(AresHtml.Html):
  """ Python class for the TD objects """
  colspan, rowspan = 1, 1

  def __init__(self, aresObj, vals, isheader=False, cssCls=None, cssAttr=None, sortBy=None):
    super(Td, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.cssCls = [] if cssCls is None else cssCls
    self.cssAttr = [] if cssAttr is None else cssCls
    self.tag = 'th' if isheader else 'td'

  def __str__(self):
    if self.colspan > 1:
      self.attr['colspan'] = self.colspan
    if self.rowspan > 1:
      self.attr['rowspan'] = self.rowspan
    withId = 'title' in self.attr
    return '<%s %s>%s</%s>' % (self.tag, self.strAttr(withId=withId), self.vals, self.tag)

  def mouseOver(self, bgcolor, fontColor='#FFFFFF'):
    """ Change the behaviour of the cell """
    self.attr['onMouseOver'] = "this.style.background='%s';this.style.color='%s'" % (bgcolor, fontColor)
    self.attr['onMouseOut'] = "this.style.background='#FFFFFF';this.style.color='#000000'"


