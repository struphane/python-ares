""" Python Module to define all the HTML component dedicated to display tables

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Table(AresHtml.Html):
  """
  Python Wrapper to the HTML TABLE, TH, TR, TD tags

  Default class parameters
    - CSS Default Class = table

  """
  cssCls, alias = 'table', 'table'
  refernce = 'https://www.w3schools.com/css/css_table.asp'

  def __init__(self, htmlId, header, vals, cssCls=None):
    """  """
    super(Table, self).__init__(htmlId, vals, cssCls)
    self.headerBox = header

  def __repr__(self):
    """ Return the String representation of a HTML table """
    item = AresItem.Item('<div class="panel panel-success">', self.incIndent)
    item.add(1, '<div class="panel-heading"><strong><i class="fa fa-table" aria-hidden="true"></i>&nbsp;%s</strong></div>' % self.headerBox)
    item.add(1, '<div class="panel-body">')
    item.add(1,'<table %s>' % self.strAttr())
    item.add(1, '<thead>')
    item.add(2, '<tr>')
    for header in self.vals[0]:
      item.add(3, '<th>%s</th>' % header)
    item.add(2, '</tr>')
    item.add(1, '</thead>')
    item.add(1, '<tbody>')
    for row in self.vals[1:]:
      item.add(1, '<tr>')
      for val in row:
        item.add(2, "<td>%s</td>" % val)
      item.add(1, '</tr>')
    item.add(1, '</tbody>')
    item.add(0, '</table>')
    item.add(0, '</div>')
    item.add(0, '</div>')
    return str(item)

  def jsEvents(self, jsEventFnc=None):
    """ Function to get the Javascript methods for this object and all the underlying objects """
    if jsEventFnc is None:
      jsEventFnc = self.jsEventFnc
    for jEventType, jsEvent in self.jsEvent.items():
      jsEventFnc[jEventType].add(str(jsEvent))

    for row in self.vals:
      for val in row:
        if hasattr(val, 'jsEvent'):
          getattr(val, 'jsEvents')(jsEventFnc)
    return jsEventFnc

  def update(self, newRecordSet):
    """ Refresh the table object with the new recordSet Data """
    item = AresItem.Item("%s.clear();" % self.htmlId)
    item.add(0, "%s.split().forEach(function(element){" % newRecordSet)
    item.add(1, "%s.row.add([element]).draw(false) ;" % (self.htmlId))
    item.add(0, "}) ;")
    return str(item)

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.table('Table Example', [["Node Code", "Ptf Code", 'IR Delta'], ["GBCSA", 31415, 24683]])

  def onLoadFnc(self):
    """ Return a String with the Javascript method to put in the HTML report """
    item = AresItem.Item("var %s;" % self.htmlId)
    item.add(0, "$(document).ready(function() {%s = %s.DataTable();} );" % (self.htmlId, self.jqId) )
    return str(item)
