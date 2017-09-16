""" Python Module to define all the HTML component dedicated to display tables


"""

from ares.Lib import AresHtml
from ares.Lib import AresItem


class Table(AresHtml.Html):
  """
  Python Wrapper to the HTML TABLE
  In order to build dynamic tables we use the javascript module DataTable

  The python RecordSet will be used in the __init__ even if the datatable
  will use the javascript reference of the recordSet object registered by Ares

  Default class parameters
    - CSS Default Class = table

  """
  cssCls, alias = 'table', 'table'
  refernce = 'https://www.w3schools.com/css/css_table.asp'
  filt, filtId = None, None
  linkedObjs = None
  pageLength = 50

  def __init__(self, aresObj, headerBox, vals, header=None, cssCls=None):
    """

    """
    super(Table, self).__init__(aresObj, vals, cssCls)
    self.headerBox = headerBox
    self.recordSetId = id(vals)
    self.recordSetHeader = []
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    else: # we have a header on several lines, nothing to do
      self.header = header
    for col in self.header[-1]:
      self.recordSetHeader.append('{ data: "%s", title: "%s"}' % (self.recKey(col), col.get("colName")))

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))

  def filters(self, cols):
    """ Store the different filters possible on the recordSet """
    items = AresItem.Item()
    self.filtId = {}
    for colName in cols:
      filterId = '%s_%s' % (self.htmlId, colName.replace(" ", ""))
      items.add(0, '<div class="form-group">')
      items.add(1, '<label for="%s">%s:</label>' % (filterId, colName))
      items.add(1, "<input type='text' id='%s' class='filter_%s' style='width:100%%'>" % (filterId, self.htmlId))
      items.add(0, '</div>')
      self.filtId[filterId] = colName
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
    item.add(0, '<table %s>' % self.strAttr())

    if len(self.header) > 1:
      item.add(1, "<thead>")
      for headerLine in self.header[:-1]:
        item.add(2, "<tr>")
        for col in headerLine:
          rowspan = " rowspan='%s'" % col['rowspan'] if col.get("rowspan", 1) > 1 else ''
          colspan = " colspan='%s'" % col['colspan'] if col.get("colspan", 1) > 1 else ''
          item.add(3, "<td%s%s>%s</td>" % (rowspan, colspan, col.get("colName")))
        item.add(2, "</tr>")
      item.add(2, "<tr>")
      # This row will be changed by the DataTable creation
      # It should correspond to the column that we will then use to populate the table
      for col in self.header[-1]:
        item.add(3, "<td>%s</td>" % col.get("colName"))
      item.add(2, "</tr>")
      item.add(1, "</thead>")
    item.add(0, '</table>')

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

    # Retrieve the list of all the columns objects
    # Those objects should be taken into account for any special javascript function
    colObj = []
    for headerLine in self.header:
      for col in headerLine:
        if col.get('type') == 'object':
          colObj.append(self.recKey(col))
    # Second Loop to extract the Javascript fragements
    # This will be added to the HTML page
    if colObj:
      for row in self.vals:
        for col in colObj:
          rawCol = "__%s" % col
          if hasattr(row[rawCol], 'jsEvent'):
            getattr(row[rawCol], 'jsEvents')(jsEventFnc)
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
                        pageLength: %s,
                        columns: [
                                    %s,
                              ],

                        dom: 'Bfrtip',
                                        buttons: [
                                              {
                                                  extend: 'colvis',
                                                  collectionLayout: 'fixed two-column'
                                              }
                                        ],

                        fixedHeader: true,
                        fnDrawCallback: function( oSettings ) {
                                            // Add the linked functions here
                                            %s
                                        }
                      }
                    ) ;
                  ''' % (self.jqId, self.recordSetId, self.pageLength, ",".join(self.recordSetHeader), "\n".join(self.linkedObjs)))
    else:
      item.add(1, '''
                  // createdRow
                  %s = %s.DataTable(
                                     {
                                        responsive: true,
                                        pageLength: %s,
                                        data: recordSet_%s ,
                                        columns: [
                                                    %s
                                              ],
                                        dom: 'Bfrtip',
                                        buttons: [
                                              {
                                                  extend: 'colvis',
                                                  collectionLayout: 'fixed two-column'
                                              }
                                        ],

                                        //headerCallback( thead, data, start, end, display ) {
                                        //      alert(display.toSource());
                                        //},

                                     }
                  ) ;

                  ''' % (self.htmlId, self.jqId, self.pageLength, self.recordSetId, ",".join(self.recordSetHeader)))
    if self.filtId is not None:
      item.add(1, "$('.filter_%s').keyup(function(){" % self.htmlId)
      item.add(2, "%s.draw() ;" % self.htmlId)
      item.add(1, "} );")
    item.add(0, "} );")

    if self.filtId is not None:
      # Add the event on the filters
      item.add(0, "$.fn.dataTable.ext.search.push(")
      item.add(1, "function(settings, data, dataIndex){")
      item.add(2, "var validLine = true ;")
      for filtId, colName in self.filtId.items():
        for headerLine in self.header:
          for i, col in enumerate(headerLine):
            if colName == col.get("colName"):
              item.add(2, "if ( ( $('#%s').val() != '') && ( validLine != false ) ) {" % filtId)
              item.add(3, "if ( data[%s].includes( $('#%s').val() ) ) {" % (i, filtId))
              item.add(4, "validLine = true ; ")
              item.add(3, "} else { validLine = false ; }")
              item.add(2, "}")
      item.add(2, "return validLine ;")
      item.add(1, "}")
      item.add(0, ") ;")
    return str(item)
