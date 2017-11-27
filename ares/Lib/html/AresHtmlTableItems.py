""" Python Module to set the underlying HTML table constituents
@Author: Olivier Nogues

"""

import json
from ares.Lib import AresHtml


class Td(AresHtml.Html):
  """ Python class for the TD objects """

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, sortBy=None, rowspan=1, colspan=1, title=None):
    super(Td, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.colspan, self.rowspan = rowspan, colspan
    if title is not None:
      self.attr['title'] = title

  def __str__(self):
    if self.colspan > 1:
      self.attr['colspan'] = self.colspan
    if self.rowspan > 1:
      self.attr['rowspan'] = self.rowspan
    withId = 'id' in self.attr
    return '<td %s valign="middle">%s</td>' % (self.strAttr(withId), self.vals)

  def mouseOver(self, bgcolor, fontColor='#FFFFFF'):
    """ Change the behaviour of the cell """
    self.attr['onMouseOver'] = "this.style.background='%s';this.style.color='%s'" % (bgcolor, fontColor)
    self.attr['onMouseOut'] = "this.style.background='#FFFFFF';this.style.color='#000000'"


class Th(AresHtml.Html):
  """ Python class for the TD objects """

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, rowspan=1, colspan=1, title=None):
    super(Th, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.colspan, self.rowspan = rowspan, colspan,
    if title is not None:
      self.attr['title'] = title

  def __str__(self):
    if self.colspan > 1:
      self.attr['colspan'] = self.colspan
    if self.rowspan > 1:
      self.attr['rowspan'] = self.rowspan
    return '<th %s>%s</th>' % (self.strAttr(False), self.vals)


class ThwithDivSpan(AresHtml.Html):
  """ Python class for the TD objects """

  def __init__(self, aresObj, vals, cssCls=None, cssAttr=None, rowspan=1, colspan=1, title=None):
    super(ThwithDivSpan, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.colspan, self.rowspan = rowspan, colspan
    if title is not None:
      self.attr['title'] = title

  def __str__(self):
    if self.colspan > 1:
      self.attr['colspan'] = self.colspan
    if self.rowspan > 1:
      self.attr['rowspan'] = self.rowspan
    return '<th %s><div><span>%s</span></div></th>' % (self.strAttr(False), self.vals)
