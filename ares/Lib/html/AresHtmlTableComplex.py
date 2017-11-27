""" Python Module to set the HTML tables
@Author: Olivier Nogues

http://jimmybonney.com/articles/column_header_rotation_css/

"""

import json

from ares.Lib import AresHtml
from ares.Lib import AresJs

from ares.Lib.html import AresHtmlContainer
from ares.Lib.html import AresHtmlText
from ares.Lib.html import AresHtmlTableItems

from Libs import AresChartsService

from flask import render_template_string


class TableComplex(AresHtml.Html):
  """ Python wrapper for the table HTML object

  This module will allow users to create bespoke tables with specific and complex features
  This will not use the usual javascript datatable.js module for the display so it will require some
  efforts to get the same look like.

  Nevertheless it will be easier to add more bespoke features
  """
  cssCls, alias = ['table'], 'table'
  references = ['https://www.w3schools.com/html/html_tables.asp',
                'https://www.w3schools.com/css/css_table.asp',
                'https://api.jquery.com/dblclick/']
  reqCss = ['bootstrap', 'jquery']
  reqJs = ['bootstrap', 'jquery']

  def __init__(self, aresObj, headerBox, vals, header=None, cssCls=None, cssAttr=None, tdCssCls=None, tdCssAttr=None):
    """ Create an Simple Table object """
    super(TableComplex, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = headerBox
    self.header = header
    self.cssPivotRows = {'font-weight': 'bold'}
    self.__rows_attr = {'rows': {'ALL': {}}}
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    self.__data = [[AresHtmlTableItems.Td(aresObj, header['colName'], True) for header in self.header[-1]]]
    self.tdCssCls = tdCssCls
    self.tdCssAttr = tdCssAttr
    for val in vals:
      row = []
      for header in self.header[-1]:
        cellVal = val.get(self.recKey(header), self.dflt)
        if cellVal is not None:
          row.append(AresHtmlTableItems.Td(aresObj, cellVal, cssCls=self.tdCssCls, cssAttr=self.tdCssAttr))
      self.__data.append(row)

  def addCols(self, keys, vals, colNames=None):
    """  Add static columns to the table object """

  def doc(self):
    """ Return the user documentation """
    return '''
           '''

  def addRows(self, vals=None):
    """ Add static rows to the table object """

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))

  def pivot(self, keys, vals, filters=None):
    """ """
    mapHeader = dict([(self.recKey(hdr), hdr['colName']) for hdr in self.header[-1]])
    self.__data = [[AresHtmlTableItems.Td(self.aresObj, mapHeader[header], True, cssAttr={'background': '#225D32', 'text-align': 'center',
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
          row.append(AresHtmlTableItems.Td(self.aresObj, cellVal, cssCls=self.tdCssCls, cssAttr=attrCss))
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


class TableBase(AresHtml.Html):
  """

  """
  # , 'table-striped', 'table-hover', 'table-responsive', 'table-header-rotated'
  # table-sm
  cssCls, alias = ['table', 'table-striped', 'table-responsive', 'table-header-rotated', 'nowrap'], 'table'
  references = ['https://www.w3schools.com/html/html_tables.asp',
                'https://www.w3schools.com/css/css_table.asp',
                'https://api.jquery.com/dblclick/']
  reqCss = ['bootstrap', 'jquery']
  reqJs = ['bootstrap', 'jquery']
  dflt = '' # Default value for a cell in the table

  def __init__(self, aresObj, headerBox, vals, header, cssCls=None, cssAttr=None, tdCssCls=None, tdCssAttr=None, globalSortBy=None):
    """ Instantiate the table object

    :param aresObj: the main object with your report details
    :param headerBox: The title of the box where the table will be displayed
    :param vals: The data to be displayed in your table
    :param header: The header section of your table
    :param cssCls: The generic CSS style to be applied to your table object
    :param cssAttr: The specific CSS attributes to be added
    :param tdCssCls: The CSS classes to be applied to your td tags (cells)
    :param tdCssAttr: the CSS specific properties to be applied to your td tags (cells)
    :return:
    """
    aresObj.suppRec(vals) # This function will only remove the reference to the main report, objects now below to the table
    super(TableBase, self).__init__(aresObj, vals, cssCls, cssAttr)
    self.headerBox = headerBox
    self.header = header
    self.buttons = []
    self.tbody = '<tbody>'
    self.cssPivotRows = {'font-weight': 'bold'}
    self.__rows_attr = {'rows': {}, 'ALL': {}}
    if header is not None and not isinstance(header[0], list): # we haven one line of header, we convert it to a list of one header
      self.header = [header]
    self.hdrLines = len(header)
    self.__data = []
    for headerLine in self.header:
      row = []
      for i, header in enumerate(headerLine):
        cellTh = AresHtmlTableItems.Th(aresObj, header['colName'], title=header.get('dsc'))
        cellTh.addAttr('name', "%s_col_%s" % (self.htmlId, i))
        row.append(cellTh)
      self.__data.append(row)
    self.tdCssCls = tdCssCls
    self.tdCssAttr = tdCssAttr
    for val in vals:
      row = []
      for i, header in enumerate(self.header[-1]):
        colId = self.recKey(header)
        cellVal = val.get(colId, self.dflt)
        cellTd = AresHtmlTableItems.Td(aresObj, cellVal, cssCls=self.tdCssCls, cssAttr=self.tdCssAttr, title=val.get('dsc_%s' % colId))
        cellTd.addAttr('name', "%s_col_%s" % (self.htmlId, i))
        row.append(cellTd)
      self.__data.append(row)

  def fixedHeader(self, height):
    """ Fix the header in the Table """
    self.addClass('fixed-header')
    self.attr.get('css', {})['height'] = "%spx" % (height + 100)
    self.tbody = "<tbody style='height:%spx'>" % height

  def mouveHover(self, backgroundColor, fontColor):
    self.aresObj.jsGlobal.add("%s_originalBackground" % self.htmlId)
    self.aresObj.jsGlobal.add("%s_originalColor" % self.htmlId)
    self.aresObj.jsFnc.add('''
        %s.on( 'mouseover', 'tbody > tr', function () {
            if ($(this).css('background-color') != '%s') {
              %s_originalBackground = $(this).css('background-color') ;
              %s_originalColor = $(this).css('color') ;
            }
            $(this).css('background-color', '%s');
            $(this).css('color', '%s');
        });
       ''' % (self.jqId, backgroundColor, self.htmlId, self.htmlId, backgroundColor, fontColor) )

    self.aresObj.jsFnc.add('''
        %s.on( 'mouseout', 'tbody > tr', function () {
            $(this).css('background-color', %s_originalBackground);
            $(this).css('color', %s_originalColor);
        });
       ''' % (self.jqId, self.htmlId, self.htmlId))

  def recKey(self, col):
    """ Return the record Key taken into accounr th possible user options """
    return col.get("key", col.get("colName"))

  def addRows(self, vals=None, dflt=None, pos=None):
    """ Add static rows to the table object """
    dflt = self.dflt if dflt is None else dflt
    for val in vals:
      row = []
      for i, header in enumerate(self.header[-1]):
        cellTd = AresHtmlTableItems.Td(self.aresObj, val.get(self.recKey(header), dflt), cssCls=self.tdCssCls, cssAttr={'color': 'blue'})
        cellTd.addAttr('name', "%s_col_%s" % (self.htmlId, i))
        row.append(cellTd)
      if pos is not None:
        self.__data.insert(pos, row)
        pos += 1
      else:
        self.__data.append(row)

  def addClassCol(self, colNumbers, classname, fromRow=None):
    """

    :param colNumber: Column number
    :param classname: The className to add to the cell
    :return:
    """
    fromRow = self.hdrLines if fromRow is None else fromRow
    for colNumber in colNumbers:
      for i, row in enumerate(self.__data[fromRow:]):
        row[colNumber].addClass(classname)

  def hideRows(self, rowNumbers, ButtonLabel):
    """
    :param rowNumber: The row numbers to be hidden in the table
    :return:
    """
    for rowNumber in rowNumbers:
      self.__rows_attr['rows'][rowNumber] = {'css': {'display': 'none'}}

    idButton = "_".join(map(lambda x: str(x), rowNumbers))
    self.buttons.append("<button id='%s_button_rows_%s' class='btn btn-success' type='button' style='margin-left:5px;margin-bottom:10px'>%s</button>" % (self.htmlId, idButton, ButtonLabel))
    self.aresObj.jsOnLoadFnc.add('''
          $('#%s_button_rows_%s').on('click', function (event){
            var rows = %s;
            var headerSize = %s ;
            var trTable = $('#%s tr');
            trTable.eq(rows[0] + headerSize).toggle() ;
            if ( trTable.eq(rows[0] + headerSize).css('display') == 'none') {
              for (idx in rows) {
                trTable.eq(rows[idx] + headerSize).hide() ;
              }
            }
            else {
              for (idx in rows) {
                trTable.eq(rows[idx] + headerSize).show() ;
              }
            }

          });
      ''' % (self.htmlId, idButton, json.dumps(rowNumbers), self.hdrLines, self.htmlId))

  def callBackCreateCellThreshold(self, colNumbers, threshold, digit=2, fromRow=None):
    """

    :param colNumber: Column number
    :param classname: The className to add to the cell
    :return:
    """
    fromRow = self.hdrLines if fromRow is None else fromRow
    for row in self.__data[fromRow:]:
      for colNumber in colNumbers:
        if row[colNumber].vals >= threshold:
          row[colNumber].addAttr('css', {'color': 'green'})
        else:
          row[colNumber].addAttr('css', {'color': 'red'})
    for colNumber in colNumbers:
      self.aresObj.jsOnLoadFnc.add('$("td[name=%s_col_%s]").each(function() { $(this).html(parseFloat($(this).html()).formatMoney(%s, ",", ".")) })' % (self.htmlId, colNumber, digit))

  def addAttrCol(self, colNumbers, name, value, fromRow=None):
    """

    :param colNumber: Column number
    :param classname: The className to add to the cell
    :return:
    """
    fromRow = self.hdrLines if fromRow is None else fromRow
    for colNumber in colNumbers:
      for i, row in enumerate(self.__data[fromRow:]):
        row[colNumber].addAttr(name, value)

  def hideCol(self, colNumbers):
    """
    :param colNumber: The column number to be impacted
    :return:
    """
    self.addAttrCol(colNumbers, 'css', {'display': 'none'}, 0)

  def addButtonShow(self, colNumbers, title):
    """

    :param colNumber:
    :return:
    """
    idButton = "_".join(map(lambda x: str(x), colNumbers))
    self.buttons.append("<button id='%s_button_%s' class='btn btn-success' type='button' style='margin-left:5px;margin-bottom:10px'>%s</button>" % (self.htmlId, idButton, title))
    self.aresObj.jsOnLoadFnc.add('''
          $('#%s_button_%s').on('click', function (event){
            var colsIndex = %s ;
            var col_def = '%s_col_';
            $('[name=' + col_def + colsIndex[0] + ']').toggle() ;
            if ( $('[name=' + col_def + colsIndex[0] + ']').css('display') == 'none') {
              for (col in colsIndex) {
                $('[name=' + col_def + colsIndex[col] + ']').hide() ;
              }
            }
            else {
              for (col in colsIndex) {
                $('[name=' + col_def + colsIndex[col] + ']').show() ;
              }
            }
          });
      ''' % (self.htmlId, idButton, json.dumps(colNumbers), self.htmlId))

  def addButtonGrpShow(self, colNumber, groupColNumber, title):
    """

    :param colNumber:
    :param groupColNumber:
    :param title:
    :return:
    """
    idButton = colNumber
    self.buttons.append("<button id='%s_button_grp_%s' class='btn btn-success' type='button' style='margin-left:5px;margin-bottom:10px'>%s</button>" % (self.htmlId, idButton, title))
    self.aresObj.jsOnLoadFnc.add('''
          $('#%s_button_grp_%s').on('click', function (event){
            var pivot_id = %s ;
            var col_def = '%s_col_';
            var cols = %s ;
            $('[name=' + col_def + pivot_id + ']').toggle() ;
            if ( $('[name=' + col_def + pivot_id + ']').css('display') == 'none') {
              for (col in cols) {
                $('[name=' + col_def + cols[col] + ']').hide() ;
              }
            }
            else {
              for (col in cols) {
                $('[name=' + col_def + cols[col] + ']').show() ;
              }
            }
          });

    ''' % (self.htmlId, idButton, colNumber, self.htmlId, json.dumps(groupColNumber)))

  def selectableRow(self):
    """ Change the table to have selectable columns """
    self.aresObj.jsGlobal.add("%s_bgcolors = {} ;" % self.htmlId)
    self.aresObj.jsOnLoadFnc.add('''
          $('#%(htmlId)s tr').on('click', function (event){
              var trId = $(this).index() ;
              if( !(trId in %(htmlId)s_bgcolors) ) {
                %(htmlId)s_bgcolors[trId] = %(htmlId)s_originalBackground ;
                %(htmlId)s_originalBackground = 'rgb(105, 163, 112)' ;
                $(this).css( { 'background-color': 'rgb(105, 163, 112)' } ) ;
              } else
              {
                %(htmlId)s_originalBackground = %(htmlId)s_bgcolors[trId];
                $(this).css( { 'background-color': %(htmlId)s_bgcolors[trId] } );
                delete %(htmlId)s_bgcolors[trId];
              }
          })''' % {'htmlId': self.htmlId})

  def __str__(self):
    """  Returns the string representation of a HTML Table """
    self.mouveHover('#BFFCA6', 'black')
    trAttr = []
    if 'css' in self.__rows_attr['ALL']:
      trAttr.append('style="%s"' % ";".join(["%s:%s" % (key, val) for key, val in self.__rows_attr['ALL']["css"].items()]))
    for attrCod in ['onmouseover', 'onMouseOut', 'class']:
      if attrCod in self.__rows_attr['ALL']:
        trAttr.append('%s="%s"' %(attrCod, " ".join(self.__rows_attr['ALL'][attrCod])))
    for attrCod in ['name', 'id', 'data-index']:
      if attrCod in self.__rows_attr['ALL']:
        trAttr.append('%s="%s"' % (attrCod, self.__rows_attr['ALL'][attrCod]))
    strTrAttr = " ".join(trAttr)
    self.aresObj.jsFnc.add('$("#%s > thead > tr > th").tooltip(); $("#%s > tbody > tr > td").tooltip() ;' % (self.htmlId, self.htmlId))

    # Special extra part of some line in the table
    trSpecialAttr = {}
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
      for attrCod in ['data-index', 'name', 'id', 'title']:
        if attrCod in attr:
          if attrCod == 'data-index':
            trRes.append('%s=%s' % (attrCod, attr[attrCod]))
          else:
            trRes.append('%s="%s"' % (attrCod, attr[attrCod]))
      trSpecialAttr[row] = " ".join(trRes)

    # Build the table
    htmlButtons = []
    if self.buttons:
      for button in self.buttons:
        htmlButtons.append(button)
    html = ["<thead>"]
    for i in range(self.hdrLines):
      if i == (self.hdrLines-1):
        html.append("<tr class='thead-inverse' %s>%s</tr>" % (strTrAttr, "".join([str(th) for th in self.__data[i]])))
      else:
        html.append("<tr %s>%s</tr>" % (strTrAttr, "".join([str(th) for th in self.__data[i]])))
    html.append("</thead>")
    html.append(self.tbody)
    for i, row in enumerate(self.__data[self.hdrLines:]):
      cells = []
      for j, td in enumerate(row):
        if self.header[-1][j].get('aresType') == 'input' and td.vals != '':
          styleVals = "style='%s'" % self.header[-1][j].get('aresCssAttr') if self.header[-1][j].get('aresCssAttr') is not None else ''
          td.vals = "<input class='form-control' value='%s' %s>" % (td.vals, styleVals)
        elif self.header[-1][j].get('aresType') == 'internalLink' and td.vals != '':
          styleVals = "style='%s'" % self.header[-1][j].get('aresCssAttr') if self.header[-1][j].get('aresCssAttr') is not None else ''
          url = render_template_string('''{{ url_for(\'ares.run_report\', report_name=\'%s\', script_name=\'%s\') }}''' % (self.aresObj.reportName, self.header[-1][j]['script_name']))
          url = "%s?%s=%s" % (url, self.recKey(self.header[-1][j]), td.vals)
          td.vals = "<a href='%s' %s target='_blank'>%s</a>" % (url, styleVals, td.vals)
        cells.append(str(td))
      if i in trSpecialAttr:
        html.append("<tr %s %s>%s</tr>" % (strTrAttr, trSpecialAttr[i], "".join(cells)))
      else:
        html.append("<tr %s>%s</tr>" % (strTrAttr, "".join(cells)))
    html.append("</tbody>")
    item =  "%s<table %s>%s</table>" % ("".join(htmlButtons), self.strAttr(), "".join(html))
    if self.headerBox is not None:
      height = int(self.attr.get('css', {'height': '300px'})['height'].replace("px", ""))
      container = AresHtmlContainer.AresBox(self.htmlId, item, self.headerBox, properties=self.references)
      container.cssAttr['height'] = "%spx" % (height + 100)
      return str(container)

    return item