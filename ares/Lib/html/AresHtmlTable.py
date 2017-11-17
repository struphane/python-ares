""" Python Module to define all the HTML component dedicated to display tables
@Author: Olivier Nogues

TODO in this module the simple table should be remove
A decorator will be added to this class to mention to users that going forward it should not be used anymore

"""

import json

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib import AresJs
from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlText

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
  cssCls, alias = ['table', 'table-striped', 'table-sm', 'nowrap'], 'table'
  references = ['https://datatables.net/reference/index',
                'https://datatables.net/reference/option/',
                'https://datatables.net/reference/option/ajax.data',
                'https://datatables.net/reference/option/drawCallback',
                'https://datatables.net/extensions/buttons/examples/initialisation/custom.html',
                'https://datatables.net/examples/api/multi_filter_select.html',
                'https://datatables.net/extensions/fixedcolumns/examples/initialisation/size_fluid.html',
                'https://stackoverflow.com/questions/42569531/span-rows-of-a-table-with-mousedown-and-drag-in-jquery']
  __reqCss = ['dataTables']
  __reqJs = ['dataTables']
  __callBackWrapper = {
      'initComplete': "function(settings, json) { %s }",
      'createdRow': "function ( row, data, index ) { %s }",
      'rowCallback': "function ( row, data, index ) { %s }",
      'footerCallback': "function ( row, data, start, end, display ) { %s }",
  }

  def __init__(self, aresObj, headerBox, vals, header=None, dataFilters=None, cssCls=None, cssAttr=None):
    self.theadCssCls = ['thead-inverse']
    self.reqCss = list(self.__reqCss)
    self.reqJs = list(self.__reqJs)
    self.pivotFilters = {}
    if dataFilters is not None:
      recordSet = []
      for rec in vals:
        for col, val in dataFilters.items():
          if not rec[col] in val:
            break

        else:
          recordSet.append(rec)
    else:
      recordSet = vals
    super(DataTable, self).__init__(aresObj, recordSet, cssCls, cssAttr)
    self.aresObj.jsGlobal.add(self.htmlId) # table has to be registered as a global variable in js
    self.headerBox = headerBox
    self.dataFilters = dataFilters
    self.recordSetHeader, self.jsMenu, self.recMap = [], [], {}
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    else: # we have a header on several lines, nothing to do
      self.header = header
    for col in self.header[-1]:
      if 'url' in col:
        # This will only work for static urls (not javascript tranalation for the time being)
        colKey = self.recKey(col)
        if 'report_name' in col['url'].get('cols', {}):
          self.recordSetHeader.append('''{ data: "%s", title: "%s",
                render: function (data, type, full, meta) {
                    var url = "run"; var cols = JSON.parse('%s');
                    rowParams = '' ;
                    for (var i in cols) {
                      rowParams = rowParams + '&' + cols[i] + '=' + full[cols[i]];
                      if (cols[i] == 'FolderName') {url = url + '/' + full[cols[i]] ; }
                    }
                    return '<a href="' + url + '">' + data + '</a>';} }''' % (colKey, self.recMap.get(colKey, colKey), json.dumps(col['url']['cols'])))
        else:
          if not 'report_name' in col['url']:
            col['url']['report_name'] = self.aresObj.http['REPORT_NAME']
          url = render_template_string('''{{ url_for(\'ares.run_report\', %s) }}''' % ",".join(["%s='%s'"% (key, val) for key, val in col['url'].items()]))
          if 'cols' in col['url']:
            self.recordSetHeader.append('''{ data: "%s", title: "%s",
                render: function (data, type, full, meta) {
                    var url = "%s"; var cols = JSON.parse('%s');
                    rowParams = '' ;
                    for (var i in cols) {rowParams = rowParams + '&' + cols[i] + '=' + full[cols[i]]; }
                    if (url.indexOf("?") !== -1) {url = url + '&' + rowParams.substring(1) ;}
                    else {url = url + '?' + rowParams.substring(1) ;}
                    return '<a href="' + url + '">' + data + '</a>';} }''' % (colKey, self.recMap.get(colKey, colKey), url, json.dumps(col['url']['cols'])))
          else:
            self.recordSetHeader.append('''{ data: "%s", title: "%s", render: function (data, type, full, meta) {return '<a href="%s">' + data + '</a>';} }''' % (colKey, self.recMap.get(colKey, colKey), url))
      #elif hasattr(self.aresObj, col.get('aresFnc', '')):
        # This part should use existing Python object to then be included to the Javascript Data Table object
        # The idea is to try as much as possible to have only one definition of the HTML components
        #colKey = self.recKey(col)
        #htmlObj = getattr(self.aresObj, col['aresFnc'])("{value: '+ data + '}")
        #self.recordSetHeader.append(
        #  ''' { data: "%s", title: "%s", render: function (data, type, full, meta) {'%s'} } ''' % (colKey, self.recMap.get(colKey, colKey), htmlObj) )
      else:
        # default value for a header definition
        # the className is an optional parameter and it might define a specific class if needed
        if 'className' in col:
          self.recordSetHeader.append('{ data: "%s", title: "%s", className="%s"}' % (self.recKey(col), col.get("colName"), col["className"]))
        else:
          self.recordSetHeader.append('{ data: "%s", title: "%s"}' % (self.recKey(col), col.get("colName")))
      self.recMap[self.recKey(col)] = col.get("colName")
    self.__options = {'pageLength': 50} # The object with all the underlying table options
    self.option('columns', "[ %s ]" % ",".join(self.recordSetHeader))
    self.withFooter, self.noPivot = False, True
    self.option('stateSave', 'true')

  def colReOrdering(self):
    """ Include the column reordering Datatable plugin """
    self.aresObj.cssImport.add('dataTables-col-order')
    self.aresObj.jsImports.add('dataTables-col-order')
    self.option('colReorder', 'true')

  def selectable(self):
    """ Include the select Datatable plugin """
    self.aresObj.cssImport.add('dataTables-select')
    self.aresObj.jsImports.add('dataTables-select')
    self.option('select', 'true')

  def scrollX(self):
    """ Set the horizontal scrollbar """
    self.option('scrollX', "true")

  def autoWidth(self, flag=True):
    """ Set the autowith flag in the datatable """
    if flag:
      self.option('autoWidth', "true")
    else:
      self.option('autoWidth', "false")

  def doc(self):
    """ Html content for the class table documentation """
    return '''
      This module is dedicated to display javascript tables.
      This componenet is a wrapper to the javazcript module datatable. You can get more details on this component
       on the datatable website. All the features of the existing datatable are available in the python interace 
  
       Please do not hesitate to liaise with us if you have implemented cool stullf that you think should be shared; 
       Indeed we will be happy to move this going forward to the new wrapper. Thus all our users will benefit from 
       your changes.
      '''

  def cssNoCenterCol(self, colsId):
    """ Change the style of the defined columns to remove the center """
    for colId in colsId:
      self.callBacks('rowCallback', ''' $('td:eq(%s)', row).addClass('left_align') ;''' % colId)

  def agg(self, keys, vals, digit=0):
    """ Simple data aggregation, no need in this function to store the result and the different levels """
    self.noPivot = False
    self.recordSetHeader = []
    for col in keys:
      self.recordSetHeader.append('{ data: "%s", title: "%s" }' % (col, self.recMap.get(col, col)))
    for val in vals:
      self.recordSetHeader.append("{ data: '%s', className: 'sum', title: '%s', render: $.fn.dataTable.render.number( ',', '.', %s ) }" % (val, self.recMap.get(val, val), digit))
    self.option('columns', "[ %s ]" % ",".join(self.recordSetHeader))
    self.__options["ordering"] = 'false'
    rows = AresChartsService.toAggTable(self.vals, keys, vals, filters=self.pivotFilters)
    self.__options['data'] = json.dumps(rows)
    if len(rows) < self.__options['pageLength']:
      self.__options['info'] = 'false'
      self.__options['bPaginate'] = 'false'

  def addCols(self, keys, vals, colNames=None):
    """ To add a static column to the table """
    colNames = keys if colNames is None else colNames
    for i, key in enumerate(keys):
      self.recordSetHeader.append('{ data: "%s", title: "%s", className: "static_col" }' % (key, colNames[i]))
    rows = json.loads(self.__options['data'])
    for row in rows:
      for i, key in enumerate(keys):
        row[key] = vals[i]
    self.__options['data'] = json.dumps(rows)
    self.option('columns', "[ %s ]" % ",".join(self.recordSetHeader))

  def pivot(self, keys, vals, colRenders=None, withUpDown=False, extendTable=False, digit=0):
    """ Create the pivot table """
    self.noPivot = False
    self.__options["ordering"] = 'false'
    rows = AresChartsService.toPivotTable(self.vals, keys, vals, filters=self.pivotFilters)
    self.__options['data'] = json.dumps(rows)
    self.recordSetHeader = []
    for col in [ '_id', '_leaf', 'level', '_hasChildren', '_parent'] + keys:
      if colRenders is not None and col in colRenders:
        if 'url' in colRenders[col]:
          # This will only work for static urls (not javascript tranalation for the time being)
          colRenders[col]['url']['report_name'] = self.aresObj.http['REPORT_NAME']
          getParams = ",".join(["%s='%s'"% (key, val) for key, val in colRenders[col]['url'].items()])
          url = render_template_string('''{{ url_for(\'ares.run_report\', %s) }}''' % getParams)
          self.recordSetHeader.append('''{ data: "%s", title: "%s",
              render: function (data, type, full, meta) {
                  var url = "%s"; var cols = JSON.parse('%s'); rowParams = '' ;
                  for (var i in cols) {rowParams = rowParams + '&' + cols[i] + '=' + full[cols[i]];}
                  if (url.indexOf("?") !== -1) {url = url + '&' + rowParams.substring(1) ;}
                  else {url = url + '?' + rowParams.substring(1) ;}
                  return '<a href="' + url + '">' + data + '</a>';} }''' % (col, self.recMap.get(col, col), url, json.dumps(colRenders[col]['cols'])))
      else:
        self.recordSetHeader.append('{ data: "%s", title: "%s" }' % (col, self.recMap.get(col, col)))
    for col in vals:
      if withUpDown:
        self.recordSetHeader.append('''{ data: "%s", title: "%s",  className: 'sum',
          render: function (data, type, full, meta) {
            val = parseFloat(data);
            if (val < 0) {
              return "<i class='fa fa-arrow-down' aria-hidden='true' style='color:red'>&nbsp;" + parseFloat(data).formatMoney(%s, ',', '.') + "</i>" ;}
            return "<i class='fa fa-arrow-up' aria-hidden='true' style='color:green'>&nbsp;" + parseFloat(data).formatMoney(%s, ',', '.') + "</i>" ; } }
        ''' % (col, self.recMap.get(col, col), digit, digit))
      else:
        self.recordSetHeader.append('''{ data: "%s", title: "%s",
          render: function (data, type, full, meta) {
            val = parseFloat(data);
            if (val < 0) {
              return "<font style='color:red'>" + parseFloat(data).formatMoney(%s, ',', '.') + "</font>" ;
            }
            return "<font style='color:green'>" + parseFloat(data).formatMoney(%s, ',', '.') + "</font>" ; } }
        ''' % (col, self.recMap.get(col, col), digit, digit))
    if len(rows) < self.__options['pageLength']:
      self.__options['info'] = 'false'
      self.__options['bPaginate'] = 'false'
    self.option('columns', "[ %s ]" % ",".join(self.recordSetHeader))
    self.hideColumns([0, 1, 2, 3, 4])
    self.option('scrollCollapse', 'false')
    self.option('paging', 'false')
    self.option('scrollY', "'50vh'")
    self.mouveHover('#BFFCA6', 'black')
    self.callBacks('rowCallback', ''' $('td:eq(0)', row).addClass('left_align') ;''')
    #self.option('order', "[[0, 'asc']]") # default behaviour anyway
    if not extendTable:
      self.callBackCreateRowHideFlag('_leaf', '1')
      self.callBackCreateRowHideFlag('_parent', '0')
      self.callBackCreateRowFlag('_hasChildren', 0, 'details')
      self.callBacks('rowCallback', '''if ( parseFloat(data['_hasChildren']) > 0 ) {$(row).addClass('details'); } ;
                                     if ( data.level > 0) {$('td:eq(0)', $(row)).css('padding-left', 25 * data.level + 'px') ;}''')
    else:
      self.callBacks('rowCallback', '''if ( parseFloat(data['_hasChildren']) > 0 ) {$(row).addClass('details'); $('td:eq(0)', row).toggleClass('changed');} ;
                                     if ( data.level > 0) {$('td:eq(0)', $(row)).css('padding-left', 25 * data.level + 'px') ;}''')
    self.click('''
                var currentTable = %s;
                var trObj = $(this).closest('tr');
                var trName = $('td:eq(0)', trObj).html();
                var trId = currentTable.row(trObj).data()._id;
                var trLevel = currentTable.row(trObj).data().level + 1;
                if (!$(this).hasClass('changed')) {
                  $(this).toggleClass('changed');
                  var nextTr = $(trObj).next();
                  while( currentTable.row(nextTr.index()).data()._id.startsWith(trId) ) {
                    if ( trLevel == currentTable.row(nextTr.index()).data().level ) {
                      nextTr.show();
                    }
                    nextTr = $(nextTr).next();
                  }
               }
               else
               {
                  $(this).toggleClass('changed');
                  var nextTr = $(trObj).next();
                  while( currentTable.row(nextTr.index()).data()._id.startsWith(trId) ) {
                    nextTr.hide();
                    $('td:eq(0)', nextTr).removeClass('changed');
                    nextTr = $(nextTr).next();
                  }

               }
               ''' % self.htmlId, colIndex=5)

  def addPivotFilter(self, fileName):
    """ Simple function to add filter rules in the pivot logic based on a text file """
    if not fileName.startswith("filterTable_"):
      raise Exception("%s should start with the name filterTable_" % fileName)

    for rec in self.aresObj.files[fileName]:
      self.pivotFilters[rec['COL_ID']] = rec['COL_VALS'].split("|")

  def option(self, keyOption, value):
    """ Add the different options to the datatable """
    if keyOption in ['data', 'ajax', 'buttons', 'columnDefs']:
      raise Exception("%s should be added using the dedicated function" % keyOption)

    self.__options[keyOption] = value

  def columnDefs(self, columnDefList):
    """ Set the column definition in the Datatable """
    self.__options['columnDefs'] = json.dumps(columnDefList)

  def hideColumns(self, colIndices):
    self.__options['columnDefs'] = "[{ 'visible': false, 'targets': [%s], 'searchable': false, 'className': 'dt_right'}]" % ",".join([str(i) for i in colIndices])

  def ajax(self, jsDic):
    """ Add the Ajax feature to load the data from an ajax service """
    self.__options['ajax'] = jsDic

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

  #--------------------------------------------------------------------------------------------------------------
  #
  #   Dedicated to wrap the section createdRow
  #--------------------------------------------------------------------------------------------------------------
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

  def callBackNumHeatMap(self, colName, dstColIndex):
    """  Change the cell according to a float threshold """
    self.callBacks('createdRow',
                   "if ( parseFloat(data['%s']) > 0 ) {$('td', row).eq(%s).addClass('green_cell'); } else {$('td', row).eq(%s).addClass('red_cell');}" % (colName, dstColIndex, dstColIndex))

  def callBackCreateCellFlag(self, colName, val, dstColIndex, cssCls):
    """  Change the cell according to a float threshold """
    self.callBacks('createdRow',
                   "if ( data['%s'] == '%s' ) {$('td', row).eq(%s).addClass('%s'); }" % (colName, val, dstColIndex, cssCls))

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

  def callBackFooterColumns(self):
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

  def callBackCreateRowFlag(self, colName, val, cssCls):
    """  Change the cell according to a float threshold """
    self.callBacks('createdRow',
                   "if ( parseFloat(data['%s']) > %s ) {$(row).addClass('%s'); }" % (colName, val, cssCls))

  # def callBackSumFooter(self):
  #   """ """
  #   self.withFooter = True
  #   self.callBacks('footerCallback',
  #                  '''
  #                     var api = this.api();
  #                     api.columns('.sum', { page: 'current' } ).every(function () {
  #                     var sum = this.data().reduce(function (a, b) {
  #                         var x = parseFloat(a) || 0; var y = parseFloat(b) || 0;return x + y; }, 0);
  #                     $(this.footer()).html(sum);
  #                     } );
  #                  ''')

  def callBackHeaderColumns(self):
    """  """
    self.withFooter = True
    self.__options["ordering"] = 'false'
    self.callBacks('initComplete',
                   '''
                      this.api().columns().every( function () {
                            var column = this;
                            var select = $('<br/><select><option value=""></option></select>').appendTo( $(column.header()) )
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

  #--------------------------------------------------------------------------------------------------------------
  #
  #   Dedicated to wrap the section buttons
  #--------------------------------------------------------------------------------------------------------------
  def addButton(self, jsDict):
    """ Internal function to add a button to the datatable """
    if not 'buttons' in self.__options:
      self.aresObj.cssImport.add('dataTables-export')
      self.aresObj.jsImports.add('dataTables-export')
      self.__options['buttons'] = [jsDict]
    else:
      self.__options['buttons'].append(jsDict)

  def buttons(self, jsParameters, dom=None):
    """ Add the parameters dedicated to display buttons on the top of the table"""
    if dom is not None:
      self.__options['dom'] = "'%s'" % dom
    self.addButton(jsParameters)

  def buttonAction(self, title, fnc):
    """ Add simple action https://datatables.net/extensions/buttons/examples/initialisation/custom.html """
    self.__options['dom'] = "'Bfrtip'"
    self.addButton("{ text: '%s', action: function (e, dt, node, config ) {%s ;} }" % (title, fnc))

  def buttonRemoveCols(self):
    """ Add simple action https://datatables.net/extensions/buttons/examples/initialisation/custom.html """
    self.__options['dom'] = "'Bfrtip'"
    self.addButton(
      "{ text: 'Remove Rows', action: function (e, dt, node, config ) { %s.row('.selected').remove().draw( false ) ;} }" % self.htmlId)

  def buttonExport(self):
    """ Add common data export """
    self.__options['dom'] = "'Bfrtip'"
    for button, name in [('copyHtml5', 'copy'), ('csvHtml5', 'csv'), ('excelHtml5', 'excel')]:
      self.addButton("{extend: '%s', text: '%s', className: 'btn btn-success btn-xs'}" % (button, name))

  def buttonSumSelection(self):
    """ Add sum on selected items """
    self.__options['dom'] = "'Bfrtip'"
    self.addButton('''
      { text: 'Sum selection', 
         action: function () { 
            var result = 0 ;
            var countCells = 0 ;
            %s.cells('.blue-border').every( function () {
                  result += parseFloat(this.data()) ;
                  countCells += 1
              }
            ) ;
            display("sum:" + result + ", count: " + countCells + ", average: " + result / countCells) ;
         }
       }''' % self.htmlId)

  def selectRows(self):
    """ """
    self.aresObj.jsFnc.add(
      '''%s.on('click', 'tr', function() {
            if ( $(this).hasClass('selected') ) { $(this).removeClass('selected'); }
            else {
              //%s.$('tr.selected').removeClass('selected');
              $(this).addClass('selected'); }
            } );''' % (self.jqId, self.htmlId))

  def selectCells(self):
    """ """
    self.aresObj.jsFnc.add(
      '''%s.on('click', 'tr td', function() {
            var table = %s ;
            var cell = table.cell(this).node() ;
            if ( $(cell).hasClass('blue-border') ) { $(cell).removeClass('blue-border'); }
            else { $(cell).addClass('blue-border'); } } );''' % (self.jqId, self.htmlId))

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

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return "%s.data().toArray()" % self.htmlId

  def dblClickOvr(self):
    """ Override a cell in the datatabble """
    self.aresObj.jsFnc.add('''
        %s.on('dblclick', 'tr td', function () {
          var $this = $(this);
          var curValue = $this.text();
          var $input = $('<input>', {
              value: $this.text(),
              type: 'text',
              blur: function() {
                 $this.text(this.value);
                 if (curValue != $this.text()) {
                  $this.css({'color': '#b3b300'});
                  var cell = %s.cell( $this );
                  cell.data( this.value ).draw();
                 }
              },
              keyup: function(e) {
                 if (e.which === 13) $input.blur();
              }
          }).appendTo( $this.empty() ).focus();
            
        });
        ''' % (self.jqId, self.htmlId))

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

  def mouseSelect(self):
    """ """
    self.aresObj.jsGlobal.add("isMouseDown = false ;")
    self.aresObj.jsFnc.add("%s.on('mousedown', 'td', function () {isMouseDown = true;});" % (self.jqId))
    self.aresObj.jsFnc.add("%s.on('mouseover', 'td', function () { var cell = %s.cell(this).node() ; ;if (isMouseDown) {$(cell).addClass('blue-border') ;} });" % (self.jqId, self.htmlId))
    self.aresObj.jsFnc.add("%s.on('mouseup', 'td', function () {isMouseDown = false;});" % (self.jqId))

  def mouveHover(self, backgroundColor, fontColor):
    self.aresObj.jsGlobal.add("%s_originalBackground" % self.htmlId)
    self.aresObj.jsGlobal.add("%s_originalColor" % self.htmlId)
    self.aresObj.jsFnc.add('''
        %s.on( 'mouseover', 'tr', function () {
            if ($(this).css('background-color') != '%s') {
              %s_originalBackground = $(this).css('background-color') ;
              %s_originalColor = $(this).css('color') ;
            }
            $(this).css('background-color', '%s');
            $(this).css('color', '%s');
        });
       ''' % (self.jqId, backgroundColor, self.htmlId, self.htmlId, backgroundColor, fontColor) )

    self.aresObj.jsFnc.add('''
        %s.on( 'mouseout', 'tr', function () {
            $(this).css('background-color', %s_originalBackground);
            $(this).css('color', %s_originalColor);
        });
       ''' % (self.jqId, self.htmlId, self.htmlId))

  def callBackFooterSum(self, colNumber):
    """ Add a footer with a sum on the datatable """
    self.withFooter = True
    self.callBacks('footerCallback',
                   '''
                    var api = this.api(), data;
                    var colNumber = %s;
                    // Remove the formatting to get integer data for summation
                    var intVal = function (i) {return typeof i === 'string' ?i.replace(/[\$,]/g, '')*1 :typeof i === 'number' ?i : 0;};

                    for (i in colNumber) {
                      // Total over all pages
                      total = api.column( colNumber[i] ).data().reduce( function (a, b) {return intVal(a) + intVal(b);}, 0 );

                      // Total over this page
                      pageTotal = api.column( colNumber[i], { page: 'current'} ).data().reduce( function (a, b) {return intVal(a) + intVal(b);}, 0 );

                      // Update footer
                      $( api.column( colNumber[i] ).footer() ).html('$' + pageTotal + ' ( $'+ total +' total)');
                    }
                    ''' % json.dumps(colNumber))

  def search(self, flag):
    """ Display or not the search item """
    self.__options['searching'] = json.dumps(flag)

  def addRow(self):
    """ Add a button to add an entry to the Data Table """
    self.__options['dom'] = "'Bfrtip'"
    emptyCol = dict([(self.recKey(col), '') for col in self.header[-1]])
    self.addButton("{ text: 'Add Row', className: 'btn btn-success', action: function (e, dt, node, config ) {%s.row.add( %s ).draw( false ) ;} }" % (self.htmlId, json.dumps(emptyCol)))

  def __str__(self):
    """ Return the string representation of a HTML table """
    if self.noPivot:
      self.__options['data'] = json.dumps(self.vals)
      if len(self.vals) < self.__options['pageLength']:
        self.__options['info'] = 'false'
        self.__options['paginate'] = 'false'
        self.__options['searching'] = 'false'
    item = AresItem.Item(None, self.incIndent)
    item.add(0, '<table %s>' % self.strAttr())
    if len(self.header) > 1:
      item.add(1, "<thead class='%s' style='white-space: nowrap;'>" % " ".join(self.theadCssCls))
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
    else:
      item.add(1, "<thead class='%s' style='white-space: nowrap;'></thead>" % " ".join(self.theadCssCls))
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
    if self.pivotFilters:
      item.add(0, '<a id="filter_%s" href="#" style="font-size:10px;text-decoration:none;font-style: italic"><i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Static Data filter applied on the recordSet</a>' % self.htmlId)
      self.aresObj.jsOnLoadFnc.add('''
        $('#filter_%s').click(function () {
            $("#popup-black-background").show();
            $("#popup-chart").show();

            $("#popup-black-background").click(function() {
              $("#popup-black-background").hide();
              $("#popup-chart").hide();
            });
        });
      ''' % self.htmlId)
    if self.headerBox is not None:
      item = AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox, properties=self.references)

    # Add the javascript dynamique part to the DataTabe
    options = []
    for key, val in self.__options.items():
      if isinstance(val, list):
        if key in self.__callBackWrapper:
          options.append("%s: %s" % (key, self.__callBackWrapper[key] % ";".join(val)))
        else:
          options.append("%s: [%s]" % (key, ",".join(val)))
      else:
        options.append("%s: %s" % (key, val))
    self.aresObj.jsFnc.add('%s = %s.DataTable({ %s }) ;' % (self.htmlId, self.jqId, ",".join(options)))
    return str(item)

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))

  def setExtVals(self, cols, htmlObj):
    """  """
    self.aresObj.jsOnLoadFnc.add(
       '''
       $.fn.dataTable.ext.search.push(
                       function( settings, data, dataIndex ) {
                           if ( $.inArray( settings.nTable.getAttribute('id'), %s_allow_tables ) == -1 ){return true;}

                           var isValid = true ;
                           isValid = ((data[6] == %s) && (isValid == true))? true: false ;
                           return isValid;
                       }

       );
       ''' % (htmlObj[0].htmlId, htmlObj[0].htmlId))
    htmlObj[0].link("var oTable = $('#%s').dataTable(); oTable.fnDraw(); " % self.htmlId)
    htmlObj[0].allowTableFilter.append(self.htmlId)

  def order(self, colName, typeOrd):
    """ Set the table order according to a column in the table """
    self.option(json.dumps([[colName, typeOrd]]))


class SimpleTable(AresHtml.Html):
  """ Python wrapper for the table HTML object """
  cssCls, alias = ['table'], 'table'
  references = ['https://www.w3schools.com/html/html_tables.asp',
                'https://www.w3schools.com/css/css_table.asp',
                'https://api.jquery.com/dblclick/']
  reqCss = ['bootstrap', 'jquery']
  reqJs = ['bootstrap', 'jquery']
  dflt = None
  formatVals = True

  @AresHtml.deprecated
  def __init__(self, aresObj, headerBox, vals, header=None, cssCls=None, cssAttr=None, tdCssCls=None, tdCssAttr=None):
    """ Create an Simple Table object """
    super(SimpleTable, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = headerBox
    self.header = header
    self.cssPivotRows = {'font-weight': 'bold'}
    self.__rows_attr = {'rows': {'ALL': {}}}
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

  def pivot(self, keys, vals, filters=None):
    """ """
    mapHeader = dict([(self.recKey(hdr), hdr['colName']) for hdr in self.header[-1]])
    self.__data = [[Td(self.aresObj, mapHeader[header], True, cssAttr={'background': '#225D32', 'text-align': 'center',
                                                                       'color': 'white', 'font-weight': 'bold'}) for header in keys + vals]]
    rows = AresChartsService.toPivotTable(self.vals, keys, vals, filters)
    self.__rows_hidden = {}
    for i, val in enumerate(rows):
      if self.formatVals:
        for keyVal in vals:
          val[keyVal] = AresHtmlText.UpDown(self.aresObj, val[keyVal], val[keyVal])
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
    for attrCod in ['onmouseover', 'onMouseOut', 'class']:
      if attrCod in self.__rows_attr:
        trAttr.append('%s="%s"' %(attrCod, " ".join(self.__rows_attr[attrCod])))
    for attrCod in ['name', 'id', 'data-index']:
      if attrCod in self.__rows_attr:
        trAttr.append('%s="%s"' % (attrCod, self.__rows_attr[attrCod]))
    strTrAttr = " ".join(trAttr)

    # Special extra part of some line in the table
    for row in self.__rows_attr['rows']:
      attr = self.__rows_attr['rows'][row]
      trRes = []
      if 'css' in attr:
        trRes.append('style="%s"' % ";".join(["%s:%s" % (key, val) for key, val in attr["css"].items()]))
      for attrCod in ['onmouseover', 'onMouseOut', 'class']:
        # Here we consider those properties as ones that could be propagated to the extra defintiion
        # This will allow in the case of the pivot table to keep the onmouseover event for example
        if attrCod in self.__rows_attr:
          if attrCod in attr:
            attr[attrCod].extend(self.__rows_attr[attrCod])
          else:
            attr[attrCod] = self.__rows_attr[attrCod]
        if attrCod in attr:
          trRes.append('%s="%s"' % (attrCod, " ".join(set(attr[attrCod]))))
      for attrCod in ['data-index', 'name', 'id']:
        if attrCod in attr:
          if attrCod == 'data-index':
            trRes.append('%s=%s' % (attrCod, attr[attrCod]))
          else:
            trRes.append('%s="%s"' % (attrCod, attr[attrCod]))
      trSpecialAttr[row] = " ".join(trRes)

    # Build the table
    html = ["<thead>"]
    html.append("<tr %s>%s</tr>" % (trSpecialAttr[0] if 0 in trSpecialAttr else strTrAttr, "".join([str(td) for td in self.__data[0]])))
    html.append("</thead>")
    html.append("<tbody>")
    for i, row in enumerate(self.__data[1:]):
      html.append("<tr %s>%s</tr>" % (trSpecialAttr[i+1] if i+1 in trSpecialAttr else strTrAttr, "".join([str(td) for td in row])))
    html.append("</tbody>")
    item =  "<table %s>%s</table>" % (self.strAttr(), "".join(html))
    if self.headerBox is not None:
      return str(AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox, properties=self.references))

    return item

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

  def cssRowMouseHover(self, bgColor='#BDFFC2', fontColor='black', rowNum=None):
    if rowNum is None:
      row = self.__rows_attr
    else:
      if not rowNum in self.__rows_attr['rows']:
        self.__rows_attr['rows'][rowNum] = {}
      row = self.__rows_attr['rows'][rowNum]
    row['onmouseover'] = ["this.style.background='%s';this.style.color='%s'" % (bgColor, fontColor)]
    row['onMouseOut'] = ["this.style.background='#FFFFFF';this.style.color='#000000'"]

  def cssPivotAggRow(self, attr):
    """  """
    self.cssPivotRows = attr