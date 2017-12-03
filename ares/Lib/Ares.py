# TODO: To use it to replace the redondant functions calls
# TODO: implement a decorator to wrap the current part in the functions

import os
import sys
import time
import inspect
import collections
import json

""" Report Interface

This module will be used to produce the final report
It will link the HTML generation with the Javascript and Graphs parts

Users will be able to create bespoke reports from this wrapper using the standard HTML functions from the
module LibReportHTML. There is no need in this section to write HTML string, this class will only struture the
component and allow users to change them.

Any new HTML component should be written in the module LibReportHtml.py

The Report Class will contain only information about formatting in order to produce the final String
report in the function html()

In Ares there is no Javascript and CSS module integrated.
Basically as long as your version of Jquery, NVD3 and D3 are recent enought to support the fragments of HTML and
javascript defined in the different classes. It is possible to test the different features in the AresWrapper module.

QUESTION: Should we call the html() function in the wrapper or should we let the user call it ?
"""
from importlib import import_module
from ares.Lib import AresImports
from ares.Lib import AresJs

from ares.Lib.html import AresHtmlData

def jsonDefault(obj):
  """ numpy.int64 is not JSON serializable, but users may use it in their report. """
  import numpy
  if isinstance(obj, numpy.integer): return int(obj)
  raise TypeError("%s (%s) is not JSON serializable" % (repr(obj), type(obj)))

aresFactory = None
if aresFactory is None:
  tmpFactory = {}
  for aresFolder in ["html", "graph"]:
    for script in os.listdir(os.path.join(os.getcwd(), 'ares', 'Lib', aresFolder)):
      if not script.endswith('py'):
        continue

      module = import_module("ares.Lib.%s.%s" % (aresFolder, script.replace('.py', '')))
      for name in dir(module):
        obj = getattr(module, name)
        if inspect.isclass(obj):
          tmpFactory[name] = obj
  # Atomic build of the factory
  aresFactory = tmpFactory

def htmlLocalHeader(cssFiles, javascriptFiles, jsGlobal, onLoad):
  """ Add the header to the report when we are producing a text file - namely local run """
  return '''
          <!DOCTYPE html>
          <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
          <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Local HTML Report</title>
            %s

            %s


            <script>
                function preloader() {
                    $('#loading').show();
                }

                function display(data){
                    $('#temp-message').html(data);
                    $('#temp-message').show();
                    $('#temp-message').fadeOut( 4000 );
                }

                $(window).scroll(function() {
                    $('#context-menu').hide() ;
                }) ;

                $(window).click(function() {
                    // Function to close the context menu
                    $("#context-menu").hide();
                });

                %s
                $(document).ready(function() {
                    %s
                    $('button[name="ares_close"]').click(function () {
                        var idEvent = $(this).attr('id').replace("_close", "") ;
                        $('#' + idEvent + '_main').remove() ;
                    });

                    $('button[name="ares_min"]').click(function () {
                        var idEvent = $(this).attr('id').replace("_min", "") ;
                        $('#' + idEvent).toggle() ;
                        if ($('#' + idEvent).is(":visible")) {
                            $(this).html('<i class="fa fa-window-minimize" aria-hidden="true"></i>') ;
                        }
                        else {
                            $(this).html('<i class="fa fa-window-maximize" aria-hidden="true"></i>') ;
                        }

                    });
                }) ;
            </script>
            <body oncontextmenu="return false;">
              <div id="page-content-wrapper">

         ''' % (cssFiles, javascriptFiles, jsGlobal, onLoad)

def htmlLocalFooter():
  """ Close all the HTML report and close the input text File - namely locally """
  return '''
            </div>
          </body>
          </html>

         '''

def convert_bytes(num):
  """
  this function will convert bytes to MB.... GB... etc
  """
  for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
      if num < 1024.0:
          return "%3.1f %s" % (num, x)
      num /= 1024.0

def isExcluded(rootPath, file=None, folders=None):
  """
  """
  if file is not None:
    if file.endswith('pyc') or file.endswith('.zip') or file in ('__pycache__', 'log_ares.dat', '.svn'):
      return True

  if folders is not None:
    folder = os.path.join(*folders)
    if '__pycache__' in folder or folder == rootPath or '.svn' in folder:
      return True
  else:
    if '__pycache__' in rootPath or '.svn' in rootPath or 'text-base' in rootPath:
      return True

  return False


class Report(object):
  """

  """

  # This list should not be changed
  definedNotif = {'SUCCESS': 'SuccessAlert', 'INFO': 'InfoAlert', 'WARNING': 'WarningAlert', 'DANGER': 'DangerAlert'}
  showNavMenu, withContainer = False, False

  def __init__(self, prefix=''):
    """ Instanciate the Ares object """
    # Internal variable that should not be used directly
    # Those variable will drive the report generation
    self.countItems, self.countNotif = 0, 0
    self.prefix, self.directory = prefix, None
    self.content = []
    self.currentTitleObj, self.navBarContent = {}, {'content': []}
    self.htmlItems, self.jsOnLoad, self.http = {}, [], {}
    self.notifications = collections.defaultdict(list)
    self.interruptReport = (False, None)
    #
    self.jsRegistered, self.jsGlobal, self.jsOnLoadFnc = {}, set(), set()
    self.jsGraphs, self.jsFnc, self.files = [], set(), {}
    self.jsImports, self.cssImport = set(['ares']), set(['ares'])
    self.jsLocalImports, self.cssLocalImports = set(), set()
    self.workers = {}
    self.fileMap = {}

  def structure(self):
    return self.content

  def addNavigationBar(self, width=25, cssCls=None):
    self.showNavMenu = True
    self.navBarContent.update({'width': width, 'cssCls': cssCls})

  def addNotification(self, notifType, title, value, cssCls=None, backgroundColor=None, closeButton=True):
    """ Add a user notfication to the report """
    notif = notifType.upper()
    if not notif in self.definedNotif:
      raise Exception("Notification Type should belong to one of the above category")

    alertCls = getattr(AresHtmlAlert, self.definedNotif[notif])
    alertObj = alertCls(self.countItems, title, value, self.countNotif, cssCls=cssCls, backgroundColor=backgroundColor, closeButton=closeButton)
    self.htmlItems[id(alertObj)] = alertObj
    self.content.append(id(alertObj))
    if notif == 'DANGER':
      self.interruptReport = (True, id(alertObj))  # we keep track of the object since this is the only thing we will display
    self.countItems += 1
    self.countNotif += 1
    return alertObj

  def item(self, itemId):
    """ Return the HTML object """
    return self.htmlItems[itemId]

  def add(self, htmlObj, fncName, inReport=True):
    """ Register the HTML component to the Ares object """
    if inReport:
      self.htmlItems[id(htmlObj)] = htmlObj
      self.content.append(id(htmlObj))
    return htmlObj

  def suppRec(self, recordSet):
    for rec in recordSet:
      for val in rec.values():
        if id(val) in self.content:
          del self.content[self.content.index(id(val))]

    return recordSet

  def supp(self, htmlObjs):
    """ Unregister the HTML component to the Ares object """
    if htmlObjs is None:
      return htmlObjs

    if isinstance(htmlObjs, list):
      for htmlObj in htmlObjs:
        if isinstance(htmlObj, list):
          for val in htmlObj:
            idObj = id(val)
            if idObj in self.content:
              del self.content[self.content.index(idObj)]
        else:
          idObj = id(htmlObj)
          if idObj in self.content:
              del self.content[self.content.index(idObj)]
    else:
      idObj = id(htmlObjs)
      if idObj in self.content:
        del self.content[self.content.index(idObj)]
    return htmlObjs

  def addTo(self, container, htmlObj):
    """ """
    self.supp(htmlObj)
    container.addVal(htmlObj)

  # ---------------------------------------------------------------------------------------------------------
  # Section dedicated to map the functions call to the HTML Component
  # This part is done in python 3 in order to ensure users will put the right type of objects
  # del self.content[self.content.index(val.htmlId)]
  # ---------------------------------------------------------------------------------------------------------
  def vignet(self, header, text, recordSet, fnc=None, col=None,  cssCls=None, cssAttr=None): return self.add(aresFactory['Vignet'](self, header, text, self.supp(recordSet), fnc, col, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def text(self, value, cssCls=None, htmlComp=None, cssAttr=None): return self.add(aresFactory['Text'](self, self.supp(value), cssCls, cssAttr, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def progressbar(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Progress'](self, self.supp(value), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def tick(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Tick'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def updown(self, value, delta, cssCls=None, cssAttr=None): return self.add(aresFactory['UpDown'](self, value, delta, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def code(self, value, cssCls=None, htmlComp=None, cssAttr=None): return self.add(aresFactory['Code'](self, self.supp(value), cssCls, cssAttr, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def preformat(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Preformat'](self, self.supp(value), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def blockquote(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['BlockQuote'](self, self.supp(value), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def paragraph(self, value, cssCls=None, htmlComp=None, cssAttr=None): return self.add(aresFactory['Paragraph'](self, self.supp(value), cssCls, cssAttr, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def dropzone(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['DropZone'](self, value, cssCls), cssAttr, sys._getframe().f_code.co_name)
  def dropfile(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['DropFile'](self, value, cssCls), cssAttr, sys._getframe().f_code.co_name)
  def line(self, cssCls=None, cssAttr=None): return self.add(aresFactory['Line'](self, '', cssCls, cssAttr), sys._getframe().f_code.co_name)
  def icon(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Icon'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def number(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Numeric'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def wiki(self, dataSourceName, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Wiki'](self, dataSourceName, value, cssCls, cssAttr), sys._getframe().f_code.co_name)

  #
  def newline(self, val=1, cssCls=None, cssAttr=None): return self.add(aresFactory['Newline'](self, val, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def hr(self, cssCls=None, cssAttr=None): return self.add(aresFactory['Hr'](self, '', cssCls, cssAttr), sys._getframe().f_code.co_name)

  # Select Section
  def dropdown(self, title, values, cssCls=None, cssAttr=None): return self.add(aresFactory['SelectDropDown'](self, title, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def ajaxDropdown(self, title, values, cssCls=None, cssAttr=None): return self.add(aresFactory['SelectDropDownAjax'](self, title, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def selectmulti(self, title, values, cssCls=None, cssAttr=None): return self.add(aresFactory['SelectMulti'](self, title, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)

  # Radio and Select Section
  def radio(self, recordSet, col=None, cssCls=None, cssAttr=None, checked=None, inReport=True): return self.add(aresFactory['Radio'](self, recordSet, col, cssCls=cssCls, cssAttr=cssAttr, checked=checked), sys._getframe().f_code.co_name, inReport=inReport)
  def select(self, recordSet, title, col=None, cssCls=None, cssAttr=None, selected=None, inReport=True): return self.add(aresFactory['Select'](self, recordSet, title, col, cssCls=cssCls, cssAttr=cssAttr, selected=selected), sys._getframe().f_code.co_name, inReport=inReport)


  # Title section
  def title(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Title'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title2(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Title2'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title3(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Title3'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title4(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Title4'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name) # Need to be linked to the NavBar


  # Button Section
  def refresh(self, value, recordSet, ajaxScript, withDataFiles=False, cssCls=None, cssAttr=None): return self.add(aresFactory['ButtonRefresh'](self, value, recordSet, ajaxScript, withDataFiles, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def remove(self, cssCls=None, cssAttr=None): return self.add(aresFactory['Button'](self, '', cssCls, cssAttr, 'remove'), sys._getframe().f_code.co_name)
  def download(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['ButtonDownload'](self, value, self.http['REPORT_NAME'], cssCls, cssAttr, 'download'), sys._getframe().f_code.co_name)
  def downloadAll(self, value='', cssCls=None, cssAttr=None): return self.add(aresFactory['ButtonDownloadEnv'](self, value, self.http['REPORT_NAME'], cssCls, cssAttr, 'suitcase'), sys._getframe().f_code.co_name)
  def button(self, value, cssCls=None, cssAttr=None, awsIcon=None): return self.add(aresFactory['Button'](self, value, cssCls, cssAttr, awsIcon), sys._getframe().f_code.co_name)
  def savetable(self, name, cssCls=None, cssAttr=None, awsIcon=None): return self.add(aresFactory['ButtonSaveTable'](self, name, cssCls, cssAttr, awsIcon), sys._getframe().f_code.co_name)
  def ok(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Button'](self, value, cssCls, cssAttr, 'check-square-o'), sys._getframe().f_code.co_name)

  # Meter
  def meter(self, value, headerBox=None, cssCls=None, cssAttr=None): return self.add(aresFactory['Meter'](self, headerBox, value, cssCls, cssAttr), sys._getframe().f_code.co_name)

  # Map
  def map(self, cssCls=None, cssAttr=None): return self.add(aresFactory['Map'](self, cssCls, cssAttr), sys._getframe().f_code.co_name)

  # Data
  def data(self, vals): return self.add(AresHtmlData.HtmlData(self, vals), sys._getframe().f_code.co_name)
  def datadic(self, vals): return self.add(AresHtmlData.HtmlDataDic(self, vals), sys._getframe().f_code.co_name)
  def recordset(self, vals): return self.add(AresHtmlData.HtmlDataRec(self, vals), sys._getframe().f_code.co_name)

  # Generic Action section
  def slider(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['Slider'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def date(self, label='Date', cssCls=None, cssAttr=None, dflt='', inReport=True): return self.add(aresFactory['DatePicker'](self, label, cssCls, cssAttr, dflt), sys._getframe().f_code.co_name, inReport)
  def textArea(self, value, cssCls=None, cssAttr=None): return self.add(aresFactory['TextArea'](self, value, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def generatePdf(self, fileName=None, cssCls=None, cssAttr=None): return self.add(aresFactory['GeneratePdf'](self, fileName, cssCls, cssAttr), sys._getframe().f_code.co_name)

  # Containers section
  def div(self, value='', cssCls=None, cssAttr=None, htmlComp=None, inReport=True): return self.add(aresFactory['Div'](self, value, cssCls, cssAttr, self.supp(htmlComp)), sys._getframe().f_code.co_name, inReport)
  def list(self, values, headerBox=None, cssCls=None, cssAttr=None): return self.add(aresFactory['List'](self, headerBox, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def listbadge(self, values, cssCls=None, cssAttr=None): return self.add(aresFactory['ListBadge'](self, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def tabs(self, values, cssCls=None, cssAttr=None): return self.add(aresFactory['Tabs'](self, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def select_group(self, values, cssCls=None, cssAttr=None): return self.add(aresFactory['SelectWithGroup'](self, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def container(self, header, values, cssCls=None, cssAttr=None): return self.add(aresFactory['Container'](self, header, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def row(self, values, cssCls=None, cssAttr=None): return self.add(aresFactory['Row'](self, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def col(self, values, cssCls=None, cssAttr=None): return self.add(aresFactory['Col'](self, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def img(self, values, cssCls=None, cssAttr=None): return self.add(aresFactory['Image'](self, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)
  def iframe(self, values, cssCls=None, cssAttr=None): return self.add(aresFactory['IFrame'](self, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)

  def table(self, values, header, headerBox=None, dataFilters=None, cssCls=None, cssAttr=None, globalSortBy=None): return self.add(aresFactory['DataTable'](self, headerBox, values, header, dataFilters, cssCls, cssAttr, globalSortBy), sys._getframe().f_code.co_name)

  # in progress
  def tablepivot(self, values, header, headerBox=None, dataFilters=None, cssCls=None, cssAttr=None, globalSortBy=None): return self.add(aresFactory['DataTablePivot'](self, headerBox, values, header, dataFilters, cssCls, cssAttr, globalSortBy), sys._getframe().f_code.co_name)
  def tableagg(self, values, header, headerBox=None, dataFilters=None, cssCls=None, cssAttr=None, globalSortBy=None): return self.add(aresFactory['DataTableAgg'](self, headerBox, values, header, dataFilters, cssCls, cssAttr, globalSortBy), sys._getframe().f_code.co_name)
  def tablehyr(self, values, header, headerBox=None, dataFilters=None, cssCls=None, cssAttr=None, globalSortBy=None): return self.add(aresFactory['DataTableHyr'](self, headerBox, values, header, dataFilters, cssCls, cssAttr, globalSortBy), sys._getframe().f_code.co_name)

  def tablebase(self, values, header, headerBox=None, cssCls=None, cssAttr=None, tdCssCls=None, tdCssAttr=None, globalSortBy=None): return self.add(aresFactory['TableBase'](self, headerBox, self.suppRec(values), header, cssCls, cssAttr, tdCssCls, tdCssAttr, globalSortBy), sys._getframe().f_code.co_name)
  def simpletable(self, values, header, headerBox=None, cssCls=None, cssAttr=None, tdCssCls=None, tdCssAttr=None, globalSortBy=None): return self.add(aresFactory['TableComplex'](self, headerBox, self.suppRec(values), header, cssCls, cssAttr, tdCssCls, tdCssAttr), sys._getframe().f_code.co_name)
  def pivot(self, values, header, headerBox=None, dataFilters=None, cssCls=None, cssAttr=None): return self.add(aresFactory['TablePivot'](self, headerBox, values, header, dataFilters, cssCls, cssAttr), sys._getframe().f_code.co_name)


  # Modal Section
  def modal(self, values, cssCls=None, cssAttr=None, btnCls=None): return self.add(aresFactory['Modal'](self, self.supp(values), cssCls, cssAttr, btnCls), sys._getframe().f_code.co_name)
  def fixedModal(self, values, cssCls=None, cssAttr=None): return self.add(aresFactory['FixedModal'](self, self.supp(values), cssCls, cssAttr), sys._getframe().f_code.co_name)


  # Chart section
  def bar(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3Bar'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def pie(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3Pie'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def donut(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3Donut'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def lineCumulative(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3LineCumulative'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def line(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3Line'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def forceDirected(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3ForceDirected'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def stackedArea(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3StackedArea'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def stackedAreaWithFocus(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3StackedAreaWithFocus'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def multiBar(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3MultiBars'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def lineChartFocus(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3LineWithFocus'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def horizBar(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3HorizontalBars'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def comboLineBar(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3ComboLineBar'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def scatter(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3ScatterChart'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def scatterline(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3ScatterPlusLineChart'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def wordcloud(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['WordCloud'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def sunburst(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3Sunburst'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def sparklineplus(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3SparkLinePlus'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def boxplot(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3PlotBox'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def candlestickbar(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3CandlestickBarChart'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def spider(self, values, header, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['D3SpiderChart'](self, headerBox, values, header, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def venn(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['NvD3Venn'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)

  # 3D charts
  def pie3D(self, values, header, chartKey=None, chartVal=None, headerBox=None, cssCls=None, cssAttr=None, mockData=False, inReport=True): return self.add(aresFactory['Donut3D'](self, headerBox, values, header, chartKey, chartVal, cssCls, cssAttr, mockData), sys._getframe().f_code.co_name, inReport)
  def vis3DSurface(self, values): return self.add(aresFactory['Vis3DSurfaceChart'](self, values), sys._getframe().f_code.co_name)

  # File HTML Section
  # def upload(self, values='', cssCls=None, cssAttr=None): return self.add(aresFactory['UploadFile'](self, values, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def upload(self, cssCls=None, cssAttr=None): return self.add(aresFactory['FileUploader'](self, '', cssCls, cssAttr), sys._getframe().f_code.co_name)
  def deployFiles(self, cssCls=None, cssAttr=None): return self.add(aresFactory['FileDeployer'](self, '', cssCls, cssAttr), sys._getframe().f_code.co_name)

  # Anchor section): return self.add(aresFactory['ScriptPage'](self, self.supp(value), attrs, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def input(self, value='', cssCls=None, cssAttr=None, dflt='', inReport=True): return self.add(aresFactory['InputText'](self, value, cssCls, cssAttr, dflt=dflt), sys._getframe().f_code.co_name, inReport=inReport)
  def pwd(self, value='', cssCls=None, cssAttr=None, dflt='', inReport=True): return self.add(aresFactory['InputPass'](self, value, cssCls, cssAttr, dflt=dflt), sys._getframe().f_code.co_name, inReport=inReport)
  def inputInt(self, value='', cssCls=None, cssAttr=None, dflt='', inReport=True): return self.add(aresFactory['InputInt'](self, value, cssCls, cssAttr, dflt=dflt), sys._getframe().f_code.co_name, inReport=inReport)
  def inputRange(self, value='', cssCls=None, cssAttr=None, dflt='', inReport=True): return self.add(aresFactory['InputRange'](self, value, cssCls, cssAttr, dflt=dflt), sys._getframe().f_code.co_name, inReport=inReport)

  # Anchor links
  def handleRequest(self, method, params, js="", cssCls=None): return self.add(aresFactory['HandleRequest'](self, method, params, js, cssCls), sys._getframe().f_code.co_name)
  def externalLink(self, value, url, cssCls=None, cssAttr=None): return self.add(aresFactory['ExternalLink'](self, self.supp(value), url, cssCls, cssAttr), sys._getframe().f_code.co_name)
  def anchor_download(self, value, **kwargs): return self.add(aresFactory['Download'](self, self.supp(value), **kwargs), sys._getframe().f_code.co_name)
  def internalLink(self, linkValue, script, attrs=None, cssCls=None, cssAttr=None, inReport=True): return self.add(aresFactory['InternalLink'](self, self.supp(linkValue), script, attrs, cssCls, cssAttr), sys._getframe().f_code.co_name, inReport=inReport)
  def downloadData(self, value, fileName=None, cssCls=None, cssAttr=None): return self.add(aresFactory['DownloadData'](self, value, fileName, cssCls, cssAttr), sys._getframe().f_code.co_name)

  # Designer objects
  def aresInput(self, cssCls=None, cssAttr=None): return self.add(aresFactory['TextInput'](self, 'Put your text here', cssCls, cssAttr), sys._getframe().f_code.co_name)
  def aresDataSource(self, cssCls=None, cssAttr=None): return self.add(aresFactory['DataSource'](self, 'Drop here', cssCls, cssAttr), sys._getframe().f_code.co_name)
  def aresDragItems(self, vals, cssCls=None, cssAttr=None): return self.add(aresFactory['DragItems'](self, vals, cssCls, cssAttr), sys._getframe().f_code.co_name)

  # HTML5 objects
  def webworker(self, htmlObj, jsFile): return self.add(aresFactory['WebWorker'](self, htmlObj, jsFile), sys._getframe().f_code.co_name)


  def changeSiteColor(self, bgColor, fontColor):
    """ To change from Ares the color of the nav bar and side bar """
    self.jsOnLoadFnc.add('''$('nav').css('background-color', '%s');
                            $('nav').css('color', '%s');
                            $('.navbar-brand').css('background-color', '%s');
                            $('.navbar-brand').css('color', '%s');
                            $('.dropdown-menu').css('background-color', '%s');
                            $('.dropdown-menu').css('color', '%s');
                            $('#sidebar-wrapper').css('background-color', '%s') ;
                            $('#sidebar-wrapper a').css('color', '%s') ;''' % (bgColor, fontColor,
                                                                               bgColor, fontColor,
                                                                               bgColor, fontColor,
                                                                               bgColor, fontColor))


  def getFoldersInfo(self, subfolders=None):
    """  """
    folders = {}
    if subfolders is not None:
      folderPath = os.path.join(self.http['DIRECTORY'], *subfolders)
    else:
      folderPath = self.http['DIRECTORY']
    for folder in os.listdir(folderPath):
      filePath = os.path.join(folderPath, folder)
      fileSize = convert_bytes(os.path.getsize(filePath))
      fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(filePath)))
      folders[folder] = {'SIZE': fileSize, 'LAST_MOD_DT': fileDate}
    return folders

  def getFiles(self, subfolders):
    """ return the list of files in a given directory structure """
    files = set()
    for pyFile in os.listdir(os.path.join(self.http['DIRECTORY'], *subfolders)):
      if isExcluded(self.http['DIRECTORY'], file=pyFile):
        continue

      files.add(pyFile)
    return files


  # --------------------------------------------------
  # Section dedicated to the file management
  #
  # From the Ares object the users will be able to only
  #   1. Read configuration files. This will return a python object (as configuration are supposed to be json object)
  #   2. Add and write a output file in the output section
  #   3. Read a file in the output file section
  # --------------------------------------------------
  def getStaticFile(self, fileName):
    """ Return the object in the Statics area with the views parameters """
    confFilg = open(os.path.join(self.http['DIRECTORY'], 'static', fileName))
    data = confFilg.read()
    confFilg.close()
    return data

  def listDataFrom(self, folder):
    """ List the file available in the folder in the output area """
    folders = []
    for (path, dirs, files) in os.walk(os.path.join(self.http['DIRECTORY'], 'data', folder)):
      for file in files:
        fileData =  self.getFileInfo(file, ['data', folder])
        fileData.update({'folderPath': folder, 'file': file})
        folders.append(fileData)
    return folders

  def getFileInfo(self, fileName, subfolders=None):
    """ Return the size and the last modification date of a given file on the server """
    if subfolders is None:
      filePath = self.http['DIRECTORY']
    else:
      filePath = os.path.join(self.http['DIRECTORY'], *subfolders)
    filePath = os.path.join(filePath, fileName)
    fileSize = convert_bytes(os.path.getsize(filePath))
    fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(filePath)))
    return {'SIZE': fileSize, 'LAST_MOD_DT': fileDate}

  def addCss(self, fileName):
    """ Add a CSS file to the header section """
    self.cssLocalImports.add("%s/css/%s" % (self.http['REPORT_NAME'], fileName))

  def addJs(self, fileName):
    """ Add a Js File to the header section """
    self.jsLocalImports.add("%s/js/%s" % (self.http['REPORT_NAME'], fileName))

  def html(self):
    """

    """
    onloadParts, htmlParts, jsGlobal, jsGraphs = [], [], [], []

    for objId in self.content:
      jsOnload, html, js = self.htmlItems[objId].html()
      for onloadFnc in jsOnload:
        onloadParts.append(onloadFnc)
      htmlParts.append(html)
      for jsType, jsFncs in js.items():
        if jsType == 'addGraph':
          continue

        else:
          jsGlobal.append("\n".join(jsFncs))

    # This has to come after the different HTML function for each of teh objects are called
    for ref in self.jsGlobal:
      jsGlobal.append("var %s ;" % ref)
    for ref, data in self.jsRegistered.items():
      jsGlobal.append("var recordSet_%s = %s ;" % (ref, json.dumps(data, default=jsonDefault)))

    for jsFnc in self.jsOnLoadFnc:
      onloadParts.append(str(jsFnc))

    for jsFnc in self.jsFnc:
      onloadParts.append(str(jsFnc))

    # Section dedicated to the javascript for all the charts
    importMng = AresImports.ImportManager()
    if self.jsGraphs:
      jsGraphs.append("nv.addGraph(function() {\n %s \n});" % "\n\n".join(self.jsGraphs))

    cssImports = importMng.cssResolve(self.cssImport, self.cssLocalImports)
    jsImports = importMng.jsResolve(self.jsImports, self.jsLocalImports)
    return cssImports, jsImports, "\n".join(onloadParts), "\n".join(htmlParts), "\n".join(jsGraphs), "\n".join(jsGlobal)
