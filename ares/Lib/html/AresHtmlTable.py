""" Python Module to define all the HTML component dedicated to display tables

"""

import json

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs
from ares.Lib.html import AresHtmlContainer
from flask import render_template_string
from Libs import AresChartsService

class Td(AresHtml.Html):
  """ Python class for the TD objects """
  colspan, rowspan = 1, 1


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
    withId = 'title' in self.attr
    return '<%s %s>%s</%s>' % (self.tag, self.strAttr(withId=withId), self.vals, self.tag)

  def mouseOver(self, bgcolor, fontColor='#FFFFFF'):
    """ Change the behaviour of the cell """
    self.attr['onMouseOver'] = "this.style.background='%s';this.style.color='%s'" % (bgcolor, fontColor)
    self.attr['onMouseOut'] = "this.style.background='#FFFFFF';this.style.color='#000000'"


class DataTable(AresHtml.Html):
  """ Python wrapper for the Javascript Datatable object """
  cssCls, alias = ['table'], 'table'
  references = ['https://datatables.net/reference/index',
                'https://datatables.net/reference/option/',
                'https://datatables.net/reference/option/ajax.data',
                'https://datatables.net/reference/option/drawCallback',
                'https://datatables.net/extensions/buttons/examples/initialisation/custom.html',
                'https://datatables.net/examples/api/multi_filter_select.html']
  reqCss = ['dataTables']
  reqJs = ['bootstrap', 'dataTables']
  __callBackWrapper = {
      'initComplete': "function(settings, json) { %s }",
      'createdRow': "function ( row, data, index ) { %s }",
      'rowCallback': "function ( row, data, index ) { %s }",
  }

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
    self.withFooter = False

  def option(self, keyOption, value):
    """ Add the different options to the datatable """
    if keyOption in ['data', 'ajax', 'buttons', 'columnDefs']:
      raise Exception("%s should be added using the dedicated function" % keyOption)

    self.__options[keyOption] = value

  def columnDefs(self, columnDefList):
    """ Set the column definition in the Datatable """
    self.__options['columnDefs'] = json.dumps(columnDefList)

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
    if callBackName not in self.__options:
      self.__options[callBackName] = []
    self.__options[callBackName].append(jsFnc)

  def callBackHideHeader(self):
    """ Callback to hide the table header """
    self.callBacks('initComplete', "$('#%s thead').find('tr:last').hide();" % self.htmlId)

  def callBackTreeStructure(self):
    """ Callback to hide the table header """
    self.callBacks('initComplete', "alert('%s');" % self.htmlId)

  def callBackCreateRow(self, fnc):
    """
    Calback to change a cell
      if ( parseFloat(data['VAL']) > 30 ) {
                                //alert(data['VAL']);
                                $('td', row).eq(0).addClass('btn-info');
                            }

    """
    self.callBacks('createdRow', fnc)

  def callBackCreateCellThreshold(self, colName, threshold, dstColIndex, cssCls):
    """  Change the cell according to a float threshold """
    self.callBacks('createdRow',
                   "if ( parseFloat(data['%s']) > %s ) {$('td', row).eq(%s).addClass('%s'); }" % (colName, threshold, dstColIndex, cssCls))

  def callBackCreateRowThreshold(self, colName, threshold, cssCls):
    """  Change the row according to a float threshold """
    self.callBacks('createdRow',
                   "if ( parseFloat(data['%s']) > %s ) {$(row).addClass('%s'); }" % (colName, threshold, cssCls))

  def callBackCreateRowHideThreshold(self, colName, threshold):
    """  Change the row according to a float threshold """
    self.callBacks('createdRow',
                   "if ( parseFloat(data['%s']) > %s ) {$(row).hide(); }" % (colName, threshold))

  def callBackCreateRowHideFlag(self, colName, value):
    """  Change the row according to tag """
    self.callBacks('createdRow',
                   "if (data['%s'] == '%s') {$(row).hide(); }" % (colName, value))

  def callBackFooterColumns(self, colNames):
    """  """
    self.withFooter = True
    self.callBacks('initComplete',
                   '''
                      this.api().columns().every( function () {
                            var column = this;
                            var select = $('<select><option value=""></option></select>').appendTo( $(column.footer()).empty() )
                                .on( 'change', function () {
                                    var val = $.fn.dataTable.util.escapeRegex( $(this).val());
                                    column.search( val ? '^'+val+'$' : '', true, false ).draw();
                                } );

                            column.data().unique().sort().each( function ( d, j ) {
                              select.append('<option value=' + d+ '>' + d +'</option>' )
                            } );
                      } );
                   ''')

  def callBackRow(self, colName, value, bgColor):
    """ Row Call back wrapper to change the background color """
    self.callBacks('rowCallback',
                   "if (data['%s'] == '%s') {$(row).css('background-color', '%s'); }" % (colName, value, bgColor))

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

  def click(self, jsFnc, colIndex=None, colVal=None):
    """ Add a Click event feature on the row or cell level

    The below example will display the column script from the row
    rowData[0] is a javascript dictionary with key and values

    For example, you can add the below to display the element from the first column of the selected row:
        alert( 'You clicked on ' + rowData[0].script + ' row' );
    """
    eventLevel, colTag = ('tr:has(td)', '') if colIndex is None else ('tr td', "['%s']" % colVal)
    if colIndex is not None:
      filterCol = "if (this._DT_CellIndex.column == %s) {var rowData = %s.row(this).data()%s;%s}" % (colIndex, self.htmlId, colTag, jsFnc)
    else:
      filterCol = 'var rowData = %s.row(this).data()%s;%s' % (self.htmlId, colTag, jsFnc)
    self.aresObj.jsFnc.add("%s.on('click', '%s', function () {%s ;});" % (self.jqId, eventLevel, filterCol))

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

    if self.withFooter:
      item.add(1, "<tfoot>")
      item.add(2, "<tr>")
      for col in self.header[-1]:
        if col.get("visible", True):
          item.add(3, "<th>%s</th>" % col.get("colName"))
      item.add(2, "</tr>")
      item.add(1, "</tfoot>")
      item.add(1, "<tbody>")
      item.add(1, "</tbody>")
    item.add(0, '</table>')

    if self.headerBox is not None:
      item = AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox, properties=self.references)

    # Add the javascript dynamique part to the DataTabe
    options = []
    for key, val in self.__options.items():
      if isinstance(val, list):
        if key in self.__callBackWrapper:
          options.append("%s: %s" % (key, self.__callBackWrapper[key] % ";".join(val)))
      else:
        options.append("%s: %s" % (key, val))
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
    self.cssPivotRows = {'font-weight': 'bold'}
    self.__rows_attr = {'rows': {}}
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    self.__data = [[Td(aresObj, header['colName'], True) for header in self.header[-1]]]
    self.tdCssCls = tdCssCls
    self.tdCssAttr = tdCssAttr
    for val in vals:
      row = []
      for header in self.header[-1]:
        cellVal = val.get(self.recKey(header), self.dflt)
        if cellVal is not None:
          row.append(Td(aresObj, cellVal, cssCls=self.tdCssCls, cssAttr=self.tdCssAttr))
      self.__data.append(row)

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))

  def pivot(self, keys, vals):
    """ """
    header = self.__data[0]
    vals = AresChartsService.toPivotTable(self.vals, keys, vals)
    self.__data = [header]
    self.__rows_hidden = {}
    for i, val in enumerate(vals):
      row, indexCol = [], i+1
      #
      if not indexCol in self.__rows_attr['rows']:
        self.__rows_attr['rows'][indexCol] = {'name': val['_id']}
      else:
        self.__rows_attr['rows'][indexCol]['name'] = val['_id']
      self.__rows_attr['rows'][indexCol]['data-index'] = val['level']

      if 'class' in self.__rows_attr['rows'][indexCol]:
        self.__rows_attr['rows'][indexCol]['class'].extend(val['cssCls'])
      else:
        self.__rows_attr['rows'][indexCol]['class'] = val['cssCls']

      if val.get('_parent', 0) == 0:
        if 'css' in self.__rows_attr['rows'][indexCol]:
          self.__rows_attr['rows'][indexCol]['css'].update({'display': 'None'})
        else:
          self.__rows_attr['rows'][indexCol]['css'] = {'display': 'None'}

      #
      if val.get('_hasChildren', 0) == 1:
        self.__rows_attr['rows'][indexCol]['class'].append('details')
        if 'css' in self.__rows_attr['rows'][indexCol]:
          self.__rows_attr['rows'][indexCol]['css'].update(self.cssPivotRows)
        else:
          self.__rows_attr['rows'][indexCol]['css'] = self.cssPivotRows
      for j, header in enumerate(self.header[-1]):
        cellVal = val.get(self.recKey(header), self.dflt)
        attrCss = dict(self.tdCssAttr) if self.tdCssAttr is not None else {}
        if cellVal is not None:
          if j == 0:
            attrCss['padding-left'] = '%spx' % (val['level'] * 20)
          row.append(Td(self.aresObj, cellVal, cssCls=self.tdCssCls, cssAttr=attrCss))
      self.__data.append(row)

    self.aresObj.jsOnLoadFnc.add(
      '''
      $( ".details > td:first-child" ).click(function() {
        var trObj = $(this).closest('tr');
        var children_data_id = trObj.data('index') + 1;
        var trName = trObj.attr('name');
        var isVisible = $(this).hasClass('changed');
        $(this).toggleClass('changed');
        $('#%s > tbody  > tr').each(function() {
          var trId = $(this).data('index');
          var trHasParent = $(this).hasClass(trName);
          if (isVisible) {
            if ((trId >= children_data_id) && trHasParent ) {
              if ($(this).hasClass('details')){
                var firstTd = $(this).find('td:first-child');
                if  (firstTd.hasClass('changed')) {
                  $(this).find('td:first-child').removeClass('changed');}
              }
              $(this).hide() ;
            }
         } else {
            if ((trId == children_data_id) && trHasParent ) {
              $(this).toggle() ;
            }
          }
          //alert($(this).attr('name'));
        } );


        //var trObj = $(this).closest('tr');
        //var children_data_id = trObj.data('index') + 1;
        //alert(children_data_id);
        //var isVisible = $( "." +  trObj.attr('name') + "[data-index=" + children_data_id + "]").is(':hidden');
        //if (isVisible) {
         // $( "." + trObj.attr('name')).hide() ;
        //} else {
        //  $( "." + trObj.attr('name') + "[data-index=" + children_data_id + "]").show() ;
       // }
        //$( "." + trObj.attr('name') + "[data-index=" + children_data_id + "]").show() ;
        //$(this).toggleClass('changed');
      });
      ''' % self.htmlId)

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
    for attrCod in ['name', 'id', 'data-index', 'onmouseover', 'onMouseOut']:
      if attrCod in self.__rows_attr:
        trAttr.append('%s="%s"' % (attrCod, self.__rows_attr[attrCod]))
    strTrAttr = " ".join(trAttr)
    for row in self.__rows_attr['rows']:
      attr = self.__rows_attr['rows'][row]
      trRes = []
      if 'css' in attr:
        trRes.append('style="%s"' % ";".join(["%s:%s" % (key, val) for key, val in attr["css"].items()]))
      if 'class' in attr:
        trRes.append('class="%s"' % " ".join(attr['class']))
      for attrCod in ['name', 'id', 'data-index', 'onmouseover', 'onMouseOut']:
        if attrCod in attr:
          trRes.append('%s="%s"' % (attrCod, attr[attrCod]))
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

  def cssRowMouseHover(self, bgColor, fontCOlor, rowNum=None):
    if rowNum is None:
      row = self.__rows_attr
    else:
      if not rowNum in self.__rows_attr['rows']:
        self.__rows_attr['rows'][rowNum] = {}
      row = self.__rows_attr['rows'][rowNum]
    row['onmouseover'] = "this.style.background='%s';this.style.color='%s'" % (bgColor, fontCOlor)
    row['onMouseOut'] = "this.style.background='#FFFFFF';this.style.color='#000000'"

  def cssPivotAggRow(self, attr):
    """  """
    self.cssPivotRows = attr
