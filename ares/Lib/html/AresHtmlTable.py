""" Python Module to define all the HTML component dedicated to display tables


"""

import os

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib.html import AresHtmlContainer

from flask import render_template_string

class Td(AresHtml.Html):
  """

  """
  colspan = 1
  rowspan = 1

  def __init__(self, aresObj, vals, isheader=False, cssCls=None, cssAttr=None):
    super(Td, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.cssCls = [] if cssCls is None else cssCls
    self.cssAttr = [] if cssAttr is None else cssCls
    self.tag = 'th' if isheader else 'td'

  def __str__(self):
    if self.colspan > 1:
      self.attr['colspan'] = self.colspan
    if self.rowspan > 1:
      self.attr['rowspan'] = self.rowspan
    return '<%s %s>%s</%s>' % (self.tag, self.strAttr(withId=False), self.vals, self.tag)


class Table(AresHtml.Html):
  """
  Python Wrapper to the HTML TABLE
  In order to build dynamic tables we use the javascript module DataTable

  The python RecordSet will be used in the __init__ even if the datatable
  will use the javascript reference of the recordSet object registered by Ares

  Default class parameters
    - CSS Default Class = table

  The only parameter defined during the Datatable definition are
      - data: data will be attached directly to the recordSet
      - pageLength: This will be set by default to 50 but it can be changed in the object by changing pageLength
      - columns: This will be deduced automatically from the header definition

  For more details regarding the datatable configuration please refer directly to the
  web page. All the documentation will be available
  """
  cssCls, alias = 'table', 'table'
  reference = 'https://datatables.net/'
  filt, filtId = None, None
  linkedObjs = None
  pageLength = 50
  jsTableConf, jsClick, jsInitCallBack = '', '', ''
  reqCss = ['dataTables']
  reqJs = ['bootstrap', 'dataTables']

  def __init__(self, aresObj, headerBox, vals, header=None, cssCls=None, cssAttr=None):
    """

    """
    super(Table, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.aresObj.jsGlobal[self.htmlId] = True # table has to be registered as a global variable in js
    self.headerBox = headerBox
    self.recordSetId = id(vals)
    self.recordSetHeader, self.jsMenu = [], []
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    else: # we have a header on several lines, nothing to do
      self.header = header
    for col in self.header[-1]:
      if col.get("visible", True):
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

    #
    #
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
        if col.get("visible", True):
          item.add(3, "<td>%s</td>" % col.get("colName"))
      item.add(2, "</tr>")
      item.add(1, "</thead>")
    item.add(0, '</table>')

    if self.headerBox is not None:
      item = AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox)
    return str(item)

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


  # ------------------------------------------------------------------------------------------------------------
  #                                           Javascript Events section
  # ------------------------------------------------------------------------------------------------------------
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
          if rawCol in row and hasattr(row[rawCol], 'jsEvent'):
            getattr(row[rawCol], 'jsEvents')(jsEventFnc)
    return jsEventFnc

  def jsUpdate(self, jsDataVar='data'):
    """
    Function to update the table from a javascript function.
    By default the usual javascript function will use the variable data in the signature.
    """
    item = AresItem.Item("%s.clear();" % self.htmlId)
    item.add(0, "%s.forEach(function(element){" % jsDataVar)
    item.add(1, "%s.row.add(element).draw(false) ;" % (self.htmlId))
    item.add(0, "}) ;")
    return str(item)

  def jsLinkTo(self, htmlObjs):
    """ Send the data to the different HTML objects in order to update them """
    if not self.linkedObjs:
      self.linkedObjs = []
    for htmlObj in htmlObjs:
      self.linkedObjs.append(htmlObj.update(self.getData()))

  def jsConfFromFile(self, fileName, attr=None):
    """ Load some extra parameters from a javascript file """
    configFile = open(os.path.join(self.aresObj.http["DIRECTORY"], 'js', fileName))
    content = configFile.read()
    configFile.close()
    self.jsTableConf = content % attr if attr is not None else content

  def onLoadFnc(self):
    """ Return a String with the Javascript method to put in the HTML report """
    #item = AresItem.Item("var %s;" % self.htmlId)
    item = AresItem.Item("$(document).ready(function() {")
    itemsPerPage = "pageLength: %s," % self.pageLength if self.pageLength is not None else ''
    if self.linkedObjs is not None:
      item.add(1, '''
                    %s.DataTable(
                      {
                        data: recordSet_%s ,
                        %s
                        columns: [
                                    %s,
                              ],
                        %s
                       // fnDrawCallback: function( oSettings ) {
                       //                     // Add the linked functions here
                       //                     %s
                       //                 }
                       // "\n".join(self.linkedObjs)
                      }
                    ) ;

                  %s

                  %s
                  ''' % (self.jqId, self.recordSetId, itemsPerPage, ",".join(self.recordSetHeader),
                         self.jsTableConf, "\n".join(self.jsMenu), self.jsClick))
    else:
      item.add(1, '''
                  // createdRow
                  // responsive: true,
                  %s = %s.DataTable(
                                     {
                                        //sDom: 'l<"H"Rf>t<"F"ip>',
                                        %s
                                        data: recordSet_%s ,
                                        columns: [
                                                    %s
                                              ],

                                        %s

                                        //headerCallback( thead, data, start, end, display ) {
                                        //      alert(display.toSource());
                                        //},

                                        %s

                                     }
                  ) ;



                  %s

                  %s
                  ''' % (self.htmlId, self.jqId, itemsPerPage, self.recordSetId, ",".join(self.recordSetHeader),
                         self.jsTableConf, self.jsInitCallBack, "\n".join(self.jsMenu), self.jsClick))
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

  def click(self, jsFnc):
    """
    Add a Click event feature

    The below example will display the column script from the row
    rowData[0] is a javascript dictionary with key and values

    $('#%s').on('click', 'tr', function () {
        var rowData = %s.rows($(this)[0]._DT_RowIndex).data();
        alert( 'You clicked on ' + rowData[0].script + ' row' );
        }
    );
    """
    self.jsClick = '''
      $('#%s').on('click', 'tr', function () {
          var rowData = %s.rows($(this)[0]._DT_RowIndex).data();
          %s
          }
      );
      ''' % (self.htmlId, self.htmlId, jsFnc)

  def initCallBack(self, js="$('#%s thead').find('tr:last').hide();"):
    """

    Call Back once the table is loaded
      $('#%s thead').find('tr:last').hide();

    """
    self.jsInitCallBack = '''
      fnInitComplete: function(oSettings) {
        %s
      },
      ''' % js % self.htmlId

  def contextMenu(self, contextMenu, attrList=None):
    """
    Add a Click event feature

    The below example will display the column script from the row
    rowData[0] is a javascript dictionary with key and values

    $('#%s').on('click', 'tr', function () {
        var rowData = %s.rows($(this)[0]._DT_RowIndex).data();
        alert( 'You clicked on ' + rowData[0].script + ' row' );
        }
    );
    """
    items, staticVars, sizeAttr = [], [], 0
    if attrList is not None:
      sizeAttr = len(attrList)
      if attrList is not None:
        staticVars = ["VAR%s='%s'" % (i, val) for i, val in enumerate(attrList)]
    for menu, script, keys in contextMenu:
      vars = ["VAR%s=' + rowData[0].%s +'" % (i + sizeAttr, key) for i, key in enumerate(keys)]
      vars.extend(staticVars)
      items.append('''<a href="{{ url_for('ares.run_report', report_name='%s', script_name='%s' )}}?%s" class="btn btn-secondary" style="width:100%%; height:30px">%s</a>''' % (self.aresObj.http['REPORT_NAME'], script, "&".join(vars), menu))
    strItems = render_template_string("".join(items))
    self.jsMenu.append('''
      $('#%s').on('contextmenu', 'tr', function (e) {
          var posX = $(this).offset().left,
              posY = $(this).offset().top;
          var rowData = %s.rows($(this)[0]._DT_RowIndex).data();
          $('#context-menu').css({top: posY - $(document).scrollTop(), left: posX - $(document).scrollLeft()});
          $('#context-menu').empty() ;
          $('#context-menu').html('%s') ;
          $('#context-menu').show() ;
          }
      );
      ''' % (self.htmlId, self.htmlId, strItems))


class DataTable(AresHtml.Html):
  """

  """
  cssCls, alias = 'table', 'table'
  reference = 'https://datatables.net/'
  reqCss = ['dataTables']
  reqJs = ['bootstrap', 'dataTables']

  __context = {}


class SimpleTable(AresHtml.Html):
  """

  """
  cssCls, alias = 'table', 'table'
  references = ['https://www.w3schools.com/html/html_tables.asp',
                'https://www.w3schools.com/css/css_table.asp',
                ]

  reqCss = ['bootstrap']
  reqJs = ['bootstrap']
  dflt = ''

  def __init__(self, aresObj, headerBox, vals, header=None, cssCls=None, cssAttr=None, tdCssCls=None, tdCssAttr=None):
    """  """
    super(SimpleTable, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = headerBox
    self.header = header
    self.__rows_attr = {}
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    self.__data = [[Td(aresObj, header['colName'], True) for header in self.header[-1]]]
    for val in vals:
      self.__data.append([Td(aresObj, val.get(self.recKey(header), self.dflt), cssCls=tdCssCls, cssAttr=tdCssAttr) for header in self.header[-1]])

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))

  def getCell(self, row, col):
    """ Returns the underlying cell object """
    return self.__data[row][col]

  def addRowsAttr(self, name, value):
    """ Set an attribute to the TR HTML object """
    if name == 'css': # Section for the Style attributes
      if not 'css' in self.attr:
        self.__rows_attr['css'] = value
      else:
        self.__rows_attr['css'].update(value)
    elif name == 'class': # Section dedicated to manage the CSS classes
      self.__rows_attr['class'].add(value)
    else: # Section for all the other attributes
      self.__rows_attr[name] = value

  def __str__(self):
    """  Returns the string representation of a HTML Table """
    html = ["<thead>"]
    html.append("<tr>%s</tr>" % "".join([str(td) for td in self.__data[0]]))
    html.append("</thead>")
    html.append("<tbody>")
    for row in self.__data[1:]:
      html.append("<tr>%s</tr>" % "".join([str(td) for td in row]))
    html.append("</tbody>")
    return "<table %s>%s</table>" % (self.strAttr(), "".join(html))