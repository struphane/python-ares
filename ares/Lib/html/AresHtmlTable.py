""" Python Module to define all the HTML component dedicated to display tables

"""

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs
from ares.Lib.html import AresHtmlContainer
from flask import render_template_string


class Td(AresHtml.Html):
  """ Python class for the TD objects """
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


class DataTable(AresHtml.Html):
  """ Python wrapper for the Javascript Datatable object """
  cssCls, alias = ['table'], 'table'
  references = ['https://datatables.net/reference/index',
                'https://datatables.net/reference/option/',
                'https://datatables.net/reference/option/ajax.data',
                'https://datatables.net/reference/option/drawCallback',
                'https://datatables.net/extensions/buttons/examples/initialisation/custom.html']
  reqCss = ['dataTables']
  reqJs = ['bootstrap', 'dataTables']

  def __init__(self, aresObj, headerBox, vals, header=None, cssCls=None, cssAttr=None):
    super(DataTable, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.aresObj.jsGlobal.add(self.htmlId) # table has to be registered as a global variable in js
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
    self.__options = {'pageLength': 50} # The object with all the underlying table options
    self.data("recordSet_%s" % self.recordSetId) # Add the Javascript data to the recordSet
    self.option('columns', "[ %s ]" % ",".join(self.recordSetHeader))

  def option(self, keyOption, value):
    """ Add the different options to the datatable """
    if keyOption in ['data', 'ajax', 'buttons']:
      raise Exception("%s should be added using the dedicated function" % keyOption)

    self.__options[keyOption] = value

  def ajax(self, jsDic):
    """ Add the Ajax feature to load the data from an ajax service """
    self.__options['ajax'] = jsDic

  def data(self, jsFnc):
    """ Add the data or ajax.data fields to the options """
    self.__options['data'] = jsFnc

  def callBacks(self, callBackName, jsFnc):
    """
    Add the function to call when a user will create a row.
    Please have a look at the documentation if you want to use some specific callback function in your table.

    The signature and the code should be in javascript
      https://datatables.net/reference/option/drawCallback
      https://datatables.net/reference/option/initComplete

    Example of callback functions
      $('#%s thead').find('tr:last').hide();
    """
    self.__options[callBackName] = jsFnc

  def callBackHideHeader(self):
    """ Callback to hide the table header """
    self.callBacks('initComplete', "function(settings, json) {$('#%s thead').find('tr:last').hide();}" % self.htmlId)

  def buttons(self, jsParameters, dom=None):
    """ Add the parameters dedicated to display buttons on the top of the table"""
    if dom is not None:
      self.__options['dom'] = "'%s'" % dom
    self.__options['buttons'] = jsParameters

  def buttonAction(self, title, fnc):
    """ Add simple action https://datatables.net/extensions/buttons/examples/initialisation/custom.html """
    self.__options['dom'] = "'Bfrtip'"
    self.__options['buttons'] = "[{ text: '%s', action: function (e, dt, node, config ) {%s ;} }]" % (title, fnc)

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
    self.aresObj.jsFnc.add('''
      %s.on('contextmenu', 'tr', function (e) {
          var posX = $(this).offset().left,
              posY = $(this).offset().top;
          var rowData = %s.rows($(this)[0]._DT_RowIndex).data();
          $('#context-menu').css({top: posY - $(document).scrollTop(), left: posX - $(document).scrollLeft()});
          $('#context-menu').empty() ;
          $('#context-menu').html('%s') ;
          $('#context-menu').show() ;
          }
      );
      ''' % (self.jqId, self.htmlId, strItems))

  def click(self, jsFnc, onTheRowOnly=True):
    """ Add a Click event feature on the row or cell level

    The below example will display the column script from the row
    rowData[0] is a javascript dictionary with key and values

    For example, you can add the below to display the element from the first column of the selected row:
        alert( 'You clicked on ' + rowData[0].script + ' row' );
    """
    eventLevel = 'tr' if onTheRowOnly else 'td'
    self.aresObj.jsFnc.add('''
      %s.on('click', '%s', function () {
          var rowData = %s.rows($(this)[0]._DT_RowIndex).data();
          %s
      });
      ''' % (self.jqId, eventLevel, self.htmlId, jsFnc))

  def __str__(self):
    """ Return the string representation of a HTML table """
    item = AresItem.Item(None, self.incIndent)
    #if self.filt is not None:
    #  item.join(self.filt)
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

    # Add the javascript dynamique part to the DataTabe
    options = ["%s: %s" % (key, val) for key, val in self.__options.items()]
    self.aresObj.jsFnc.add('%s = %s.DataTable({ %s }) ;' % (self.htmlId, self.jqId, ",".join(options)))
    return str(item)

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))


class SimpleTable(AresHtml.Html):
  """ Python wrapper for the table HTML object """
  cssCls, alias = ['table'], 'table'
  references = ['https://www.w3schools.com/html/html_tables.asp',
                'https://www.w3schools.com/css/css_table.asp',
                'https://api.jquery.com/dblclick/']
  reqCss = ['bootstrap', 'jquery']
  reqJs = ['bootstrap', 'jquery']
  dflt = None

  def __init__(self, aresObj, headerBox, vals, header=None, cssCls=None, cssAttr=None, tdCssCls=None, tdCssAttr=None):
    """ Create an Simple Table object """
    super(SimpleTable, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = headerBox
    self.header = header
    self.__rows_attr = {'rows': {}}
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    self.__data = [[Td(aresObj, header['colName'], True) for header in self.header[-1]]]
    for val in vals:
      row = []
      for header in self.header[-1]:
        cellVal = val.get(self.recKey(header), self.dflt)
        if cellVal is not None:
          row.append(Td(aresObj, cellVal, cssCls=tdCssCls, cssAttr=tdCssAttr))
      self.__data.append(row)

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))

  def getCell(self, row, col):
    """ Returns the underlying cell object """
    return self.__data[row][col]

  def addRowsAttr(self, name, value, rowNum=None):
    """ Set an attribute to the TR HTML object """
    if rowNum is None:
      row = self.__rows_attr
    else:
      if not rowNum in self.__rows_attr['rows']:
        self.__rows_attr['rows'][rowNum] = {}
      row = self.__rows_attr['rows'][rowNum]

    if name == 'css': # Section for the Style attributes
      if not 'css' in row:
        row['css'] = value
      else:
        row['css'].update(value)
    elif name == 'class': # Section dedicated to manage the CSS classes
      row['class'].add(value)
    else: # Section for all the other attributes
      row[name] = value

  def __str__(self):
    """  Returns the string representation of a HTML Table """
    trAttr, trSpecialAttr = [], {}
    if 'css' in self.__rows_attr:
      trAttr.append('style="%s"' % ";".join(["%s:%s" % (key, val) for key, val in self.__rows_attr["css"].items()]))
    if 'class' in self.__rows_attr:
      trAttr.append('class="%s"' % " ".join(self.__rows_attr['class']))
    strTrAttr = " ".join(trAttr)
    for row in self.__rows_attr['rows']:
      attr = self.__rows_attr['rows'][row]
      trRes = []
      if 'css' in attr:
        trRes.append('style="%s"' % ";".join(["%s:%s" % (key, val) for key, val in attr["css"].items()]))
      if 'class' in attr:
        trRes.append('class="%s"' % " ".join(attr['class']))
      trSpecialAttr[row] = " ".join(trRes)

    html = ["<thead>"]
    html.append("<tr %s>%s</tr>" % (trSpecialAttr[0] if 0 in trSpecialAttr else strTrAttr, "".join([str(td) for td in self.__data[0]])))
    html.append("</thead>")
    html.append("<tbody>")
    for i, row in enumerate(self.__data[1:]):
      html.append("<tr %s>%s</tr>" % (trSpecialAttr[i+1] if i+1 in trSpecialAttr else strTrAttr, "".join([str(td) for td in row])))
    html.append("</tbody>")
    return "<table %s>%s</table>" % (self.strAttr(), "".join(html))

  def cell_dblclick(self, jsFnc):
    """ Add an event on the cells, $(this).html() will return the selected value """
    self.aresObj.jsFnc(AresJs.JQueryEvents(self.htmlId, "$('#%s td,th')" % self.htmlId, 'dblclick', jsFnc))

  def row_dblclick(self, jsFnc):
    """ Add an event on the cells, $(this).html() will return the selected value """
    self.aresObj.jsFnc(AresJs.JQueryEvents(self.htmlId, "$('#%s tr')" % self.htmlId, 'dblclick', jsFnc))

  def update_cell(self):
    """ Update a cell in the table """
    jsFnc = '''
                var html = '<div id="dialog" title="update value">' ;
                html = html + '<div class="form-group">';
                html = html + '<label for="formgroupexampleinput">example label</label>';
                html = html + '<input id="temp_cell" type="text" class="form-control">';
                html = html + '</div>';
                html = html + '<button type="submit" id="temp_submit" class="btn btn-primary">submit</button>' ;
                html = html + '</div>';

                $('body').append(html) ;
                $('#temp_cell').val($(event.target).html());
                $("#dialog").dialog();

                // Update the data to the table
                $( "#temp_submit" ).on( "click", { item: $(event.target) }, function (event){
                    event.data.item.html($('#temp_cell').val());
                    $( "#dialog" ).remove();
                });

            '''
    self.aresObj.jsFnc.add(AresJs.JQueryEvents(self.htmlId, "$('#%s td')" % self.htmlId, 'dblclick', jsFnc))
