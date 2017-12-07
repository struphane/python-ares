""" Python Module to define all the HTML component dedicated to display tables
@Author: Olivier Nogues

TODO in this module the simple table should be remove
A decorator will be added to this class to mention to users that going forward it should not be used anymore

#TODO Split the Datatable into 3 tables Table, TablePivot and TableAgg
"""

import json
import operator

from ares.Lib import AresHtml
from ares.Lib import AresItem
from ares.Lib.html import AresHtmlContainer

from flask import render_template_string
from Libs import AresChartsService


class DataTable(AresHtml.Html):
  """ Python wrapper for the Javascript Datatable object """
  __cssCls, alias = ['table', 'table-sm', 'nowrap'], 'table'
  references = ['https://datatables.net/reference/index',
                'https://datatables.net/reference/option/',
                'https://datatables.net/reference/option/ajax.data',
                'https://datatables.net/reference/option/drawCallback',
                'https://datatables.net/extensions/buttons/examples/initialisation/custom.html',
                'https://datatables.net/examples/api/multi_filter_select.html',
                'https://datatables.net/extensions/fixedcolumns/examples/initialisation/size_fluid.html',
                'https://stackoverflow.com/questions/42569531/span-rows-of-a-table-with-mousedown-and-drag-in-jquery',
                'https://datatables.net/examples/server_side/row_details.html']
  __reqCss = ['dataTables']
  __reqJs = ['dataTables']
  __callBackWrapper = {
      'initComplete': "function(settings, json) { %s }",
      'createdRow': "function ( row, data, index ) { %s }",
      'rowCallback': "function ( row, data, index ) { %s }",
      'footerCallback': "function ( row, data, start, end, display ) { %s }",
  }

  def __init__(self, aresObj, headerBox, vals, header=None, dataFilters=None, cssCls=None, cssAttr=None, sortBy=None):
    """

    :param aresObj:
    :param vals:
    :param isheader:
    :param cssCls:
    :param cssAttr:
    :param sortBy: Should be a tuple with (column name, asc / desc, number of items or Nene)
    :return:
    """
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
    self.sortBy = sortBy
    self.pivotLevel = 1
    if self.sortBy is not None:
      if self.sortBy[1].lower() == 'desc':
        sortedItems = sorted(recordSet, key=operator.itemgetter(self.sortBy[0]))
      else:
        sortedItems = sorted(recordSet, key=operator.itemgetter(self.sortBy[0]), reverse=True)
      if self.sortBy[2] not in ['', None]:
        sortedItems = sortedItems[:self.sortBy[2]]
      recordSet = sortedItems
    self.hiddenCols = []
    self.cssCls = list(self.__cssCls)
    self.theadCssCls = ['thead-inverse']
    self.reqCss = list(self.__reqCss)
    self.reqJs = list(self.__reqJs)
    self.pivotFilters, self.tableToolTips = {}, {}
    super(DataTable, self).__init__(aresObj, recordSet, cssCls, cssAttr)
    self.aresObj.jsGlobal.add(self.htmlId) # table has to be registered as a global variable in js
    self.headerBox = headerBox
    self.dataFilters = dataFilters
    self.recordSetHeader, self.jsMenu, self.recMap = [], [], {}
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    else: # we have a header on several lines, nothing to do
      self.header = header
    for i, col in enumerate(self.header[-1]):
      if 'dsc' in col:
        self.addToolTips(i, col['dsc'])
      if 'url' in col:
        # This will only work for static urls (not javascript tranalation for the time being)
        colKey = self.recKey(col)
        if 'report_name' in col['url'].get('cols', {}):
          self.recordSetHeader.append('''{ data: "%s", title: "%s", className: "%s", visible: %s,
                render: function (data, type, full, meta) {
                    var url = "run"; var cols = JSON.parse('%s');
                    rowParams = '' ;
                    for (var i in cols) {
                      if (cols[i] == 'FolderName') {url = url + '/' + full[cols[i]] ; }
                      else if (cols[i] == 'report_name') {}
                      else {rowParams = rowParams + '&' + cols[i].trim() + '=' + full[cols[i]];}
                    }
                    return '<a href="' + url + '?' + rowParams.substr(1) + '">' + data + '</a>';} }''' % (colKey, self.recMap.get(colKey, colKey), col.get("colName", ''),
                                                                                                          col.get("visible", 'true'), json.dumps(col['url']['cols'])))
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
          self.recordSetHeader.append('{ data: "%s", title: "%s", className: "%s", visible: %s}' % (self.recKey(col), col.get("colName"), col["className"], col.get("visible", 'true')))
        else:
          self.recordSetHeader.append('{ data: "%s", title: "%s", visible: %s}' % (self.recKey(col), col.get("colName"), col.get("visible", 'true')))
      self.recMap[self.recKey(col)] = col.get("colName")
    self.__options = {'pageLength': 50} # The object with all the underlying table options
    self.option('columns', "[ %s ]" % ",".join(self.recordSetHeader))
    self.withFooter, self.noPivot = False, True
    self.option('stateSave', 'true')
    self.tableUpdates = []
    self.mapDsc = {}
    for i, header in enumerate(self.header[-1]):
      if 'dsc' in header:
        self.mapDsc[self.recKey(header)] = (i, header['dsc'])

  def fixedHeader(self):
    """ Set the header to be fixed """
    self.aresObj.jsImports.add('dataTables-fixedHeader')
    self.aresObj.cssImport.add('dataTables-fixedHeader')
    self.option('fixedHeader', "{ headerOffset: 50 }")

  def fixedColumns(self, lenCols=1):
    """ Set some columns on the left to be fixed """
    self.aresObj.jsImports.add('dataTables-fixedColumns')
    self.aresObj.cssImport.add('dataTables-fixedColumns')
    self.option('fixedColumns', "{ leftColumns: 2 }")

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

  def agg(self, keys, vals, digit=0, isColStriped=True, colCenter=False):
    """ Simple data aggregation, no need in this function to store the result and the different levels """
    self.noPivot = False
    if isColStriped:
      self.addClass('table-striped')
    self.recordSetHeader = []
    self.tableToolTips = {}
    colToIndex = {}
    for i, col in enumerate(keys):
      colToIndex[col] = i
      if col in self.mapDsc:
        self.addToolTips(i+1, self.mapDsc[col][1])
      self.recordSetHeader.append('{ data: "%s", title: "%s" }' % (col, self.recMap.get(col, col)))
    for i, val in enumerate(vals):
      colToIndex[val] = i + len(keys)
      if val in self.mapDsc:
        self.addToolTips(i + len(keys), self.mapDsc[val][1])
      self.recordSetHeader.append("{ data: '%s', className: 'sum', title: '%s', render: $.fn.dataTable.render.number( ',', '.', %s ) }" % (val, self.recMap.get(val, val), digit))
    if self.sortBy is not None:
      self.order(colToIndex[self.sortBy[0]], self.sortBy[1])
    self.option('columns', "[ %s ]" % ",".join(self.recordSetHeader))
    rows = AresChartsService.toAggTable(self.vals, keys, vals, filters=self.pivotFilters)
    self.__options['data'] = json.dumps(rows)
    self.mouveHover('#BFFCA6', 'black')
    self.option('scrollCollapse', 'false')
    if colCenter:
      self.callBacks('rowCallback', ''' $('td:eq(0)', row).addClass('left_align') ;''')
    else:
      for i in range(len(keys)):
        self.callBacks('rowCallback', ''' $('td:eq(%s)', row).addClass('left_align') ;''' % i)
    if len(rows) < self.__options['pageLength']:
      self.__options['info'] = 'false'
      self.__options['bPaginate'] = 'false'

  def addCols(self, keys, vals, colNames=None):
    """ To add a static column to the table """
    colNames = keys if colNames is None else colNames
    for i, key in enumerate(keys):
      self.recordSetHeader.append('{ data: "%s", title: "%s", className: "static_col" }' % (key, colNames[i]))
    rows = json.loads(self.__options['data']) if 'data' in self.__options else self.vals
    for row in rows:
      for i, key in enumerate(keys):
        row[key] = vals[i]
    if 'data' in self.__options:
      self.__options['data'] = json.dumps(rows)
    self.option('columns', "[ %s ]" % ",".join(self.recordSetHeader))

  def pivot(self, keys, vals, colRenders=None, withUpDown=False, extendTable=False, digit=0, colCenter=False):
    """ Create the pivot table """
    self.noPivot = False
    self.__options["ordering"] = 'false'
    rows = AresChartsService.toPivotTable(self.vals, keys, vals, filters=self.pivotFilters)
    self.pivotLevel = len(keys)
    self.pivotKeys = keys
    self.__options['data'] = json.dumps(rows)
    self.recordSetHeader = []
    self.hiddenCols.extend([ '_id', '_leaf', 'level', '_hasChildren', '_parent'])
    self.tableToolTips = {}
    for i, col in enumerate([ '_id', '_leaf', 'level', '_hasChildren', '_parent'] + keys):
      if col in self.mapDsc:
        self.addToolTips(i, self.mapDsc[col][1])
      if colRenders is not None and col in colRenders:
        if 'url' in colRenders[col]:
          # This will only work for static urls (not javascript tranalation for the time being)
          colRenders[col]['url']['report_name'] = self.aresObj.http['REPORT_NAME']
          getParams = ",".join(["%s='%s'"% (key, val) for key, val in colRenders[col]['url'].items()])
          url = render_template_string('''{{ url_for(\'ares.run_report\', %s) }}''' % getParams)
          self.recordSetHeader.append('''{ "data": "%s", "title": "%s",
              "render": function (data, type, full, meta) {
                  var url = "%s"; var cols = JSON.parse('%s'); rowParams = '' ;
                  for (var i in cols) {rowParams = rowParams + '&' + cols[i] + '=' + full[cols[i]];}
                  if (url.indexOf("?") !== -1) {url = url + '&' + rowParams.substring(1) ;}
                  else {url = url + '?' + rowParams.substring(1) ;}
                  return '<a href="' + url + '">' + data + '</a>';} }''' % (col, self.recMap.get(col, col), url, json.dumps(colRenders[col]['cols'])))
      else:
        self.recordSetHeader.append('{ "data": "%s", "title": "%s" }' % (col, self.recMap.get(col, col)))
    for i, col in enumerate(vals):
      if col in self.mapDsc:
        self.addToolTips(i + len(keys), self.mapDsc[col][1])
      if withUpDown:
        self.recordSetHeader.append('''{ data: "%s", title: "%s",  className: 'sum',
          render: function (data, type, full, meta) {
            val = parseFloat(data);
            if (val < 0) {
              return "<i class='fa fa-arrow-down' aria-hidden='true' style='color:red'>&nbsp;" + parseFloat(data).formatMoney(%s, ',', '.') + "</i>" ;}
            return "<i class='fa fa-arrow-up' aria-hidden='true' style='color:green'>&nbsp;" + parseFloat(data).formatMoney(%s, ',', '.') + "</i>" ; } }
        ''' % (col, self.recMap.get(col, col), digit, digit))
      else:
        self.recordSetHeader.append('''{ data: "%s", title: "%s",  className: 'sum',
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
    if colCenter:
      self.callBacks('rowCallback', ''' $('td:eq(0)', row).addClass('left_align') ;''')
    else:
      for i in range(len(keys)):
        self.callBacks('rowCallback', ''' $('td:eq(%s)', row).addClass('left_align') ;''' % i)
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

  def addPivotFilter(self, fileCod, fileName):
    """ Simple function to add filter rules in the pivot logic based on a text file """
    if not fileName.startswith("filterTable_"):
      raise Exception("%s should start with the name filterTable_" % fileName)

    self.pivotFilterFileName = fileName
    self.pivotFilterFileCode = fileCod
    for rec in self.aresObj.files[fileName]:
      self.pivotFilters[rec['COL_ID']] = rec['COL_VALS'].split("|")

  def addToolTips(self, col, dsc):
    """  Function to add a tooltip on the column headers """
    self.tableToolTips[col] = "$('#%s > thead > tr > th:eq(%s)').attr('title', '%s')" % (self.htmlId, col, dsc)

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

  def callBackCreateCellNumber(self, dstColIndex, digit=2):
    """  Change the cell according to a float threshold """
    self.callBacks('createdRow', "$('td', row).eq(%s).html( parseFloat( $('td', row).eq(%s).html()).formatMoney(%s, ',', '.'))" % (dstColIndex, dstColIndex, digit))

  def callBackCreateCellNumberColor(self, dstColIndex, digit=2):
    """  Change the cell according to a float threshold """
    self.callBacks('createdRow', '''
      var val = parseFloat($('td', row).eq(%s).html()) ;
      if (val > 0) { $('td', row).eq(%s).html( val.formatMoney(%s, ',', '.') ).css('color', 'green') }
      else { $('td', row).eq(%s).html( val.formatMoney(%s, ',', '.') ).css('color', 'green') } 
      ''' % (dstColIndex, dstColIndex, digit, dstColIndex, digit))

  def callBackCreateUrl(self, dstColIndex, scriptName, extraCols=None):
    """

    :param dstColIndex: The index of the main column with the hyperlink
    :param scriptName: The script name to be called
    :param extraCols: The list wiht the extra columns to be added to the URL
    :return:
    """
    url = render_template_string('''{{ url_for('ares.run_report', report_name='%s', script_name='%s') }}''' % (self.aresObj.reportName, scriptName))
    self.callBacks('createdRow', '''
      var content = $('td', row).eq(%s).html() ;
      var extraCols = %s ;
      var header = %s ;
      var colsVar = [] ;
      var contentUrl = content;
      if (extraCols != null) {
        for (var item in extraCols) {
          var colNum = extraCols[item] ;
          colsVar.push(header[colNum].key + "=" + $('td', row).eq(colNum).html())
        } ;
        contentUrl = content + "&" + colsVar.join('&') ;
      }
      $('td', row).eq(%s).html("<a href='%s?%s="+ contentUrl + "'>" + content + "</a>")
      ''' % (dstColIndex, json.dumps(extraCols), self.header[-1], json.dumps(dstColIndex), url, self.recKey(self.header[-1][dstColIndex])))

  def callBackCreateSlider(self, dstColIndex):
    """ Add a slider object in the cell """
    self.callBacks('createdRow', ''' 
      var rowValue = parseFloat( $('td', row).eq(%s).html() ) ; 
      $('td', row).eq(%s).html( "<div id='%s_slider_" + index + "'>"+ rowValue + "</div>" )
      $( function() { var rowValue = parseFloat( $( "#%s_slider_" + index ).html() ) ; $( "#%s_slider_" + index ).slider( {value: rowValue} ); } );
      ''' % (dstColIndex, dstColIndex, self.htmlId, self.htmlId, self.htmlId))
   #self.aresObj.jsOnLoadFnc.add('$( function() { $( "#%s" ).slider(); } );')

  def callBackCreateButton(self, dstColIndex):
    """ Add a button to the data table cell """
    self.callBacks('createdRow', ''' 
      var content = parseFloat( $('td', row).eq(%s).html() ) ;
      $('td', row).eq(%s).html( "<button class='btn'>" + content + "</button>" )
      ''' % (dstColIndex, dstColIndex))
    self.aresObj.jsOnLoadFnc.add('$( function() { $( "[name=slider]" ).slider(); } );')

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

  def callBackSumFooter(self, digit=2):
    """ """
    self.withFooter = True
    self.callBacks('footerCallback',
                   '''
                      var api = this.api();
                      api.columns('.sum', { page: 'current' } ).every(function (el) {
                          var sum = this.data().reduce(function (a, b) {var x = parseFloat(a) || 0; var y = parseFloat(b) || 0;return x + y; }, 0);
                      var result;
                      var sum = sum / %s ;
                      if (sum < 0) {result = "<font style='color:red'>" + sum.formatMoney(%s, ',', '.') + "</font>" ;}
                      result = "<font style='color:green'>" + sum.formatMoney(%s, ',', '.') + "</font>";
                      $(this.footer()).html(result);
                      } );
                   ''' % (self.pivotLevel, digit, digit))

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

  def callBackHeaderColumnsTootips(self):
    """ To add a header on the datatable headers - in progress """
    self.__options["ordering"] = 'false'
    self.callBacks('initComplete',
                   '''
                      this.api().columns().every( function (el) {
                            var column = this;
                            $('td', this).tooltip( {placement : '', html : true, content: 'youpi'}) ;
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

  def allowOverride(self):
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
                  $this.css({'color': '#2807ff'});
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
                      pageTotal = pageTotal / %s ; // for the pivot table
                      // Update footer
                      $( api.column( colNumber[i] ).footer() ).html('$' + pageTotal + ' ( $'+ total +' total)');
                    }
                    ''' % (json.dumps(colNumber), self.pivotLevel))

  def search(self, flag):
    """ Display or not the search item """
    self.__options['searching'] = json.dumps(flag)

  def addRows(self, vals=None):
    """ Add a button to add an entry to the Data Table

    vals - should be a list of dictionaries
    """
    if vals is None:
      self.__options['dom'] = "'Bfrtip'"
      emptyCol = dict([(self.recKey(col), '') for col in self.header[-1]])
      self.addButton("{ text: 'Add Row', className: 'btn btn-success', action: function (e, dt, node, config ) {%s.row.add( %s ).draw( false ) ;} }" % (self.htmlId, json.dumps(emptyCol)))
    else:
      self.tableUpdates.append("%s.rows.add( %s ).draw( false ).nodes().to$().addClass('static_row')" % (self.htmlId, json.dumps(vals)))

  # def addRow(self, rec, level, hasChild=False):
  #   """ Add a row """
  #   if hasChild:
  #     rec.update({'_hasChildren': 1, '_leaf': level, '_parent': 1})
  #     rec['cssCls'] = []
  #     for i, key in enumerate(self.pivotKeys):
  #       if i < level:
  #         rec[key] = ''
  #       elif i == level:
  #   else:
  #     rec.update({'_hasChildren': '0', '_leaf': 1, '_parent': 1})
  #
  #
  #   pivotTable.addRows([{'_hasChildren': 0, 'cssCls': ['SelfFundingInstalments', 'SelfFundingInstalmentsYoupi'], 'level': 1,
  #                      '_leaf': 1, '_parent': 0, 'TTTT': 0, '_id': 'SelfFundingInstalmentsWESTPAC', 'TYPE': '', 'ISSUER': 'Youpi', 'Aurelie': ''}])
  #   pivotTable.addRows([{'_hasChildren': 1, 'cssCls': ['Youpi'], 'level': 0,
  #                        '_leaf': 0, '_parent': 1, 'TTTT': 0, '_id': 'SelfFundingInstalmentsWESTPAC', 'TYPE': 'Youpi', 'ISSUER': '', 'Aurelie': ''}])
  #   pivotTable.addRows([{'_hasChildren': 0, 'cssCls': ['Youpi', 'YoupiSuper'], 'level': 1,
  #                        '_leaf': 1, '_parent': 0, 'TTTT': 0, '_id': 'SelfFundingInstalmentsWESTPAC', 'TYPE': '', 'ISSUER': 'Super', 'Aurelie': ''}])

  def __str__(self):
    """ Return the string representation of a HTML table """
    if self.noPivot:
      self.addClass('table-striped')
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
      if len(self.header) > 1:
        for col in self.header[-1]:
          if col.get("visible", True):
            item.add(3, "<th>%s</th>" % col.get("colName"))
      else:
        for _ in self.recordSetHeader:
          item.add(2, "<th></th>")
      item.add(2, "</tr>")
      item.add(1, "</tfoot>")
    item.add(1, "<tbody>")
    item.add(1, "</tbody>")
    item.add(0, '</table>')
    if self.sortBy is not None and self.sortBy[2] not in [None, '']:
      sortType = 'worst' if self.sortBy[1] == 'desc' else 'top'
      item.add(0, '<a id="sort_%s" href="#" style="font-size:10px;text-decoration:none;font-style: italic;cursor:default"><i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Display the %s %s data based on %s</a><br/>' % (self.htmlId, sortType, self.sortBy[2], self.sortBy[0]))
    if self.pivotFilters:
      item.add(0, '<a id="filter_%s" href="#" style="font-size:10px;text-decoration:none;font-style: italic"><i class="fa fa-filter" aria-hidden="true"></i>&nbsp;Static filters applied on the recordSet</a><br/>' % self.htmlId)
      self.aresObj.jsOnLoadFnc.add('''
        $('#filter_%s').click(function () {
            var internalTableId = '%s' ;
            $("#popup-black-background").show();
            $("#popup-chart").empty();
            $("#popup-chart").append('<div class="logo_small">Filter configuration</div>');
            $("#popup-chart").append('<input type="text" class="form-control" id="filename_' + internalTableId + '" value="%s">');
            $("#popup-chart").append('<input type="hidden" class="form-control" id="fileCode_' + internalTableId + '" value="%s">');

            var filters = %s;
            for(key in filters){
              $("#popup-chart").append('<div style="text-align:left;width:90%%;height:30px;margin-left:5%%;margin-right:5%%;margin-top:10px">' + key + '<input class="form-control" id="filter_new_' + key + '_'+ internalTableId +'" style="width:60%%;display:inline;margin-left:5px;margin-right:5px;height:35px" type="text"><button id="filter_add_'+ key + '_' + internalTableId + '" class="btn btn-success">add</button>&nbsp;<button id="filter_del_'+ key + '_' + internalTableId + '" class="btn btn-danger">remove</button></div>');
              var selectbox = $('<select name="filter_val_' + internalTableId + '" id="'+ key +'" size="4" style="width:90%%;padding-left:5%%;padding-right:5%%;margin-top:10px">');
              for (val in filters[key]){
                selectbox.append($('<option>').text(filters[key][val]).val(filters[key][val]));
              }
              $("#popup-chart").append(selectbox);
              $("#popup-chart").append("<BR>") ;

              $("#filter_add_"+ key + "_" + internalTableId).click({srcInput: '#filter_new_' + key + '_' + internalTableId, selectBox:'#'+ key}, function(event) {
                  var newItem = $(event.data.srcInput).val();
                  $(event.data.selectBox).append($('<option>').text(newItem).val(newItem));
              });

              $("#filter_del_"+ key + "_" + internalTableId).click({selectBox:'#'+ key}, function(event) {
                  $(event.data.selectBox +" option:selected").remove();
              });
            }

            $("#popup-chart").append("<br/><input id='filter_valid_" + internalTableId + "' type='submit' class='btn btn-success' value='Save'><br/><br/>")
            $("#popup-chart").show();

            $("#popup-black-background").click(function() {
              $("#popup-black-background").hide();
              $("#popup-chart").hide();
            });

            $("#filter_valid_"+ internalTableId).click(function() {
              var content = [];
              $("select[name=filter_val_" + internalTableId + "]").each(function (i, el) {
                var row = [$(el).attr('id')] ;
                var values = [];
                $('#' + $(el).attr('id') + ' option').each(function(){
                  values.push($(this).text());
                });
                row.push(values.join("|"));
                content.push(row.join("#"));
              });

              $.post("../../ajax/_AresReports/SrvSaveToFile", {fileName: $('#filename_' + internalTableId).val(), fileCode: $('#fileCode_' + internalTableId).val(), reportName: '%s', rows: content.join("\\n"), folder: 'static'}, function(data) {
                  var res = JSON.parse(data) ;
                  var data = res.data ;
                  var status = res.status ;
                  $("#popup-black-background").hide();
                  $("#popup-chart").hide();
                  $("#popup-chart").empty();
                  display(data);
              } );
            });

        });
      ''' % (self.htmlId, self.htmlId, self.pivotFilterFileName, self.pivotFilterFileCode, json.dumps(self.pivotFilters), self.aresObj.reportName))

    if self.headerBox is not None:
      item = AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox, properties=self.references)
      if 'width' in self.attr.get('css', {}):
        item.cssAttr['width'] = self.attr['css']['width']

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

    headerToolTips = []
    if  self.tableToolTips:
      headerToolTips = []
      for toolTips in self.tableToolTips.values():
        headerToolTips.append(toolTips)
      headerToolTips.append('$("#%s > thead > tr > th").tooltip()' % self.htmlId)
    self.aresObj.jsFnc.add('%s = %s.DataTable({ %s }) ; %s; %s ;' % (self.htmlId, self.jqId, ",".join(options), ";".join(self.tableUpdates), ";".join(headerToolTips)))
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

  def order(self, colIndex, typeOrd):
    """ Set the table order according to a column in the table """
    self.option("order", json.dumps([[colIndex, {'desc': 'asc', 'asc': 'desc'}.get(typeOrd, typeOrd)]]))


class DataTablePivot(DataTable):
  """

  """

  def setKeys(self, keys, selected=None):
    self.chartKeys = [self.header[key] for key in keys]

  def setVals(self, vals, selected=None):
    self.chartVals = [self.header[val] for val in vals]


class DataTableAgg(DataTable):
  """

  """

  def setKeys(self, keys, selected=None):
    self.chartKeys = [self.header[key] for key in keys]

  def setVals(self, vals, selected=None):
    self.chartVals = [self.header[val] for val in vals]


class DataTableHyr(DataTable):
  """

  """

  def setKeys(self, keys, selected=None):
    self.chartKeys = [self.header[key] for key in keys]

  def setVals(self, vals, selected=None):
    self.chartVals = [self.header[val] for val in vals]