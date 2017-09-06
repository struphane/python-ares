""" Python Module to define all the HTML component dedicated to display tables

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Table(AresHtml.Html):
  """
  Python Wrapper to the HTML TABLE, TH, TR, TD tags
  using recordSet as input

  Default class parameters
    - CSS Default Class = table

  """
  cssCls, alias = 'table', 'table'
  refernce = 'https://www.w3schools.com/css/css_table.asp'
  filt, filtId = None, None
  linkedObjs = None

  def __init__(self, htmlId, headerBox, vals, header=None, cssCls=None):
    """

    """
    super(Table, self).__init__(htmlId, vals, cssCls)
    self.headerBox = headerBox
    self.recordSetId = id(vals)
    self.recordSetHeader = []
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    else: # we have a header on several lines, nothing to do
      self.header = header
    for headerLine in self.header:
      for col in headerLine:
        self.recordSetHeader.append('{ data: "%s", title: "%s"}' % (col.get("key", col.get("colName")), col.get("colName")))
    self.rowTmpl = "\n".join(["<td>%%(%s)s</td>" % col for col in self.header])

  def filters(self, colsDict):
    """ Store the different filters possible on the recordSet """
    items = AresItem.Item()
    self.filtId = {}
    for colName, idCol in colsDict.items():
      filterId = '%s_%s' % (self.htmlId, idCol)
      items.add(0, '<div class="form-group">')
      items.add(1, '<label for="%s">%s:</label>' % (filterId, colName))
      items.add(1, "<input type='text' id='%s' name='%s' style='width:100%%'>" % (filterId, filterId))
      items.add(0, '</div>')
      #items.add(0, "%s: <input id='%s' name='%s' type='text'>" % (colName, filterId, filterId))
      self.filtId[filterId] = idCol
    self.filt = items

  def __str__(self):
    """ Return the string representation of a HTML table """
    item = AresItem.Item(None, self.incIndent)

    if self.headerBox is not None:
      item.add(0, '<div class="panel panel-success">')
      item.add(1, '<div class="panel-heading"><strong><i class="fa fa-table" aria-hidden="true"></i>&nbsp;%s</strong></div>' % self.headerBox)
      item.add(1, '<div class="panel-body">')
    if self.filt is not None:
      item.join(self.filt)
    item.add(0, '<table %s></table>' % self.strAttr())
    if self.headerBox is not None:
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
      for val in row.values():
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

  def jsLinkTo(self, htmlObjs):
    """ Send the data to the different HTML objects in order to update them """
    if not self.linkedObjs:
      self.linkedObjs = []
    for htmlObj in htmlObjs:
      self.linkedObjs.append(htmlObj.update(self.getData()))

  def onLoadFnc(self):
    """ Return a String with the Javascript method to put in the HTML report """
    #item = AresItem.Item("var %s;" % self.htmlId)
    item = AresItem.Item("$(document).ready(function() {")
    if self.linkedObjs is not None:
      item.add(1, '''
                    %s.DataTable(
                      {
                        data: recordSet_%s ,
                        columns: [
                                    %s
                              ],
                        fixedHeader: true,
                        fnDrawCallback: function( oSettings ) {
                                            // Add the linked functions here
                                            %s
                                        }
                      }
                    ) ;
                  ''' % (self.jqId, self.recordSetId, ",".join(self.recordSetHeader), "\n".join(self.linkedObjs)))
    else:
      item.add(1, '''
                  %s = %s.DataTable(
                                     {
                                        data: recordSet_%s ,
                                        columns: [
                                                    %s
                                              ],
                                        fixedHeader: true
                                     }
                  ) ;''' % (self.htmlId, self.jqId, self.recordSetId, ",".join(self.recordSetHeader)))
    if self.filtId is not None:
      item.add(1, "$('%s').keyup(function(){" % ", ".join(["#%s" % id for id in self.filtId]))
      item.add(2, "%s.draw() ;" % self.htmlId)
      item.add(1, "} );")
    item.add(0, "} );")

    if self.filtId is not None:
      # Add the event on the filters
      item.add(0, "$.fn.dataTable.ext.search.push(")
      item.add(1, "function(settings, data, dataIndex){")
      item.add(2, "if( ( data[1].includes($('#table_1_CCY').val()) ) || ($('#table_1_CCY').val() == '')) return true ;")
      item.add(2, "return false ;")
      item.add(1, "}")
      item.add(0, ") ;")
    return str(item)
