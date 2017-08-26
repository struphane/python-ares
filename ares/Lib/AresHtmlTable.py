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
  filt, filtId = None, None

  def __init__(self, htmlId, header, vals, cssCls=None):
    """  """
    super(Table, self).__init__(htmlId, vals, cssCls)
    self.headerBox = header

  def filters(self, colsDict):
    """ Store the different filters possible on the recordSet """
    items = AresItem.Item()
    self.filtId = {}
    for colName, idCol in colsDict.items():
      filterId = '%s_%s' % (self.htmlId, idCol)

      items.add(0, '<div class="form-group">')
      items.add(1, '<label for="%s">%s:</label>' % (filterId, colName))
      items.add(2, "<input type='text' id='%s' name='%s' style='width:100%%'>" % (filterId, filterId))
      items.add(0, '</div>')

      #items.add(0, "%s: <input id='%s' name='%s' type='text'>" % (colName, filterId, filterId))
      self.filtId[filterId] = idCol
    self.filt = items

  def __str__(self):
    """ Return the String representation of a HTML table """
    item = AresItem.Item('<div class="panel panel-success">', self.incIndent)
    item.add(1, '<div class="panel-heading"><strong><i class="fa fa-table" aria-hidden="true"></i>&nbsp;%s</strong></div>' % self.headerBox)
    item.add(1, '<div class="panel-body">')
    if self.filt is not None:
      item.join(self.filt)
    item.add(1,'<table %s>' % self.strAttr())

    # Header
    item.add(1, '<thead>')
    header = self.vals.get("header")
    if header is None: # no header
      header = []
    elif not isinstance(header[0], list): # one-line header > I convert to a list of header lines (to process the same way as multiline header)
      header = [header]
    for headerLine in header:
      item.add(2, "<tr>")
      for col in headerLine:
        if isinstance(col, tuple):
          item.add(3, "<th %s>%s</th>" % (col[1], col[0]))
        else:
          item.add(3, "<th>%s</th>" % col)
      item.add(2, "</tr>")
    item.add(1, "</thead>")

    # Body
    item.add(1, '<tbody>')
    for row in self.vals.get("body", []):
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
    if isinstance(newRecordSet, str):
      # In this case we assume that data are received from a String
      # Rows should be # delimited
      # Columns should be , delimited
      item.add(0, "%s.split('#').forEach(function(element){" % newRecordSet)
      item.add(1, "%s.row.add(element.split(',')).draw(false) ;" % (self.htmlId))
    else:
      # here we assume that we receive a list of list to add to the table
      item.add(0, "%s.forEach(function(element){" % newRecordSet)
      item.add(1, "%s.row.add(element).draw(false) ;" % (self.htmlId))
    item.add(0, "}) ;")
    return str(item)

  def getData(self):
    """
    Returns a javascript recordSet
    This line should not have ; at the end as it is only a fragment that will be added to the
    middle of another javascript line
    """
    return "getRecordSetFromTable('%s')" % self.htmlId

  @classmethod
  def aresExample(cls, aresObj):
    return aresObj.table('Table Example', [["Node Code", "Ptf Code", 'IR Delta'], ["GBCSA", 31415, 24683]])

  def onLoadFnc(self):
    """ Return a String with the Javascript method to put in the HTML report """
    item = AresItem.Item("var %s;" % self.htmlId)
    item.add(0, "$(document).ready(function() {")
    item.add(1, '''
                  %s = %s.DataTable(
                    {"fnDrawCallback": function( oSettings ) {
                                          // Add the linked functions here
                                        }
                    }
                  ) ;
                ''' % (self.htmlId, self.jqId))
    if self.filtId is not None:
      item.add(1, "$('%s').keyup(function(){" % ", ".join(["#%s" % id for id in self.filtId]))
      item.add(2, "%s.draw() ;" % self.htmlId)
      item.add(1, "} );")
    item.add(0, "} );")

    if self.filtId is not None:
      # Add the event on the filters
      item.add(0, "$.fn.dataTable.ext.search.push(")
      item.add(1, "function(settings, data, dataIndex){")
      item.add(2, "if( ( data[1].includes($('#tablerec_1_CCY').val()) ) || ($('#tablerec_1_CCY').val() == '')) return true ;")
      item.add(2, "return false ;")
      item.add(1, "}")
      item.add(0, ") ;")
    return str(item)


class TableRec(Table):
  """
  Python wrqpper of the HTMO version using recordSet as input.
  No difference witht the parent class except the fact that the input is based on something bigger than the ones thet
  we will potentially dusplay

  """
  cssCls, alias = 'table', 'tableRec'
  reference = ''

  def __init__(self, htmlId, headerBox, vals, header, cssCls=None):
    """ Create a Python HTNL table based on a recordSet """
    super(TableRec, self).__init__(htmlId, headerBox, vals, cssCls)
    self.header = header
    self.rowTmpl = "\n".join(["<td>%%(%s)s</td>" % col for col in self.header])

  def __str__(self):
    """ Return the string representation of a HTML table """
    item = AresItem.Item(None, self.incIndent)
    if self.headerBox is not None:
      item.add(0, '<div class="panel panel-success">')
      item.add(1, '<div class="panel-heading"><strong><i class="fa fa-table" aria-hidden="true"></i>&nbsp;%s</strong></div>' % self.headerBox)
      item.add(1, '<div class="panel-body">')
    if self.filt is not None:
      item.join(self.filt)
    item.add(0, '<table %s>' % self.strAttr())
    item.add(1, '<thead>')
    item.add(2, '<tr>')
    for col in self.header:
      item.add(3, '<th>%s</th>' % self.header[col])
    item.add(2, '</tr>')
    item.add(1, '</thead>')
    item.add(1, '<tbody>')
    for rec in self.vals:
      item.add(1, '<tr>')
      item.add(2, self.rowTmpl % rec)
      item.add(1, '</tr>')
    item.add(1, '</tbody>')
    item.add(0, '</table>')
    if self.headerBox is not None:
      item.add(0, '</div>')
      item.add(0, '</div>')
    return str(item)