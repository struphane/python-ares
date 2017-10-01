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
# TODO: To use it to replace the redondant functions calls
# TODO: implement a decorator to wrap the current part in the functions

import os
import sys
import time
import inspect
import collections
import json

def jsonDefault(obj):
  """ numpy.int64 is not JSON serializable, but users may use it in their report. """
  import numpy
  if isinstance(obj, numpy.integer): return int(obj)
  raise TypeError("%s (%s) is not JSON serializable" % (repr(obj), type(obj)))

from click import echo

from ares.Lib import AresHtmlContainer
from ares.Lib import AresHtmlEvent
from ares.Lib import AresHtmlText
from ares.Lib import AresHtmlTable
from ares.Lib import AresHtmlGraph
from ares.Lib import AresHtmlAlert
from ares.Lib import AresHtmlModal
from ares.Lib import AresItem
from ares.Lib import AresHtmlHRef
from ares.Lib import AresHtmlButton
from ares.Lib import AresLog
from ares.Lib import AresJsModules
from ares.Lib import AresHtmlMeter
from ares.Lib import AresHtmlGraphWordCloud
from ares.Lib import AresHtmlAjaxCall
from ares.Lib import AresHtmlMap

def htmlLocalHeader(statisPath, cssFiles, javascriptFiles):
  """ Add the header to the report when we are producing a text file - namely local run """
  item = AresItem.Item('<!DOCTYPE html>')
  item.add(0, '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">')
  item.add(0, '<head>')
  item.add(1, '<meta charset="utf-8">')
  item.add(1, '<meta http-equiv="X-UA-Compatible" content="IE=edge">')
  item.add(1, '<meta name="viewport" content="width=device-width, initial-scale=1">')
  item.add(1, '<title>Local HTML Report</title>')
  for style in cssFiles:
    item.add(1, '<link rel="stylesheet" href="%s" type="text/css">' % os.path.join(statisPath, 'css', style))
  for javascript in javascriptFiles:
    item.add(1, '<script src="%s"></script>' % os.path.join(statisPath, 'js', javascript))
  return str(item)

def htmlLocalFooter():
  """ Close all the HTML report and close the input text File - namely locally """
  item = AresItem.Item(None)
  item.add(1, '</div>')
  item.add(0, '</body>')
  item.add(0, '</html>')
  return str(item)

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
    if file.endswith('pyc') or file.endswith('.zip') or file in ('__pycache__', 'log_ares.dat', '__init__.py', '.svn'):
      return True

  if folders is not None:
    folder = os.path.join(*folders)
    if '__pycache__' in folder or folder == rootPath or '.svn' in folder:
      return True
  else:
    if '__pycache__' in rootPath or '.svn' in rootPath or 'text-base' in rootPath:
      return True

  return False

def moduleFromAlias(alias):
  for aresModule in [AresHtmlText]:
      for name, cls in inspect.getmembers(aresModule):
        if inspect.isclass(cls) and cls.alias is not None and alias == cls.alias:
          return cls

  return None


class Report(object):
  """

  """

  # This list should not be changed
  definedNotif = {'SUCCESS': 'SuccessAlert', 'INFO': 'InfoAlert', 'WARNING': 'WarningAlert', 'DANGER': 'DangerAlert'}
  showNavMenu = False

  def __init__(self, prefix=''):
    """ Instanciate the Ares object """
    # Internal variable that should not be used directly
    # Those variable will drive the report generation
    self.countItems, self.countNotif = 0, 0
    self.prefix, self.directory = prefix, None
    self.content, self.jsGraph = [], []
    self.currentTitleObj, self.navBarContent = {}, {'content': []}
    self.htmlItems, self.jsOnLoad, self.http = {}, [], {}
    self.notifications = collections.defaultdict(list)
    self.interruptReport = (False, None)
    self.jsRegistered, self.jsGlobal, self.fileManager = {}, {}, {}
    self.jsImports, self.cssImport = set(['ares']), set(['ares'])

  def structure(self):
    return self.content

  def addNavigationBar(self, width=25, cssCls=None):
    self.showNavMenu = True
    self.navBarContent.update({'width': width, 'cssCls': cssCls})

  def addNotification(self, notifType, title, value, cssCls=None, backgroundColor=None, closeButton=True):
    """ Add a user notfication to the report """
    notif = notifType.upper()
    if not notif in self.definedNotif:
      echo("Notification %s not recognized !" % notif)
      echo("Allowed notification %s" % self.definedNotif.keys())
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

  def add(self, htmlObj, fncName):
    """ Register the HTML component to the Ares object """
    if fncName != htmlObj.alias:
      raise Exception("%s not register for the Ares function %s" % (htmlObj.alias, fncName))

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

  def register(self, recordSet, header):
    """
    This function will register the recordSet when it is shared with other components
    """
    strFct, newRecordSet = [], []
    for headerLine in header:
      if isinstance(headerLine, list):
        for headerRow in headerLine:
          if headerRow.get("type") == 'object':
            strFct.append(headerRow.get('key', headerRow['colName']) )
      else:
        if headerLine.get("type") == 'object':
          strFct.append(headerLine.get('key', headerLine['colName']) )
    if id(recordSet) not in self.jsRegistered:
      if strFct:
        newRecordSet = []
        for rec in recordSet:
          fullRec = dict(rec)
          for col in strFct:
            fullRec["__%s" % col] = rec[col]
            fullRec[col] = str(rec[col])
            rec[col] = str(rec[col])
          newRecordSet.append(fullRec)
        self.jsRegistered[id(recordSet)] = recordSet
        self.jsRegistered[id(newRecordSet)] = recordSet
        return newRecordSet

      self.jsRegistered[id(recordSet)] = recordSet
    return recordSet

  # ---------------------------------------------------------------------------------------------------------
  # Section dedicated to map the functions call to the HTML Component
  # This part is done in python 3 in order to ensure users will put the right type of objects
  # del self.content[self.content.index(val.htmlId)]
  # ---------------------------------------------------------------------------------------------------------
  def vignet(self, header, text, recordSet, fnc=None, col=None,  cssCls=None, htmlComp=None): return self.add(AresHtmlContainer.Vignet(self, header, text, self.supp(recordSet), fnc, col, cssCls), sys._getframe().f_code.co_name)
  def text(self, value, cssCls=None, htmlComp=None): return self.add(AresHtmlText.Text(self, self.supp(value), cssCls, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def progressbar(self, value, cssCls=None): return self.add(AresHtmlEvent.Progress(self, self.supp(value), cssCls), sys._getframe().f_code.co_name)
  def tick(self, value, cssCls=None): return self.add(AresHtmlText.Tick(self, value, cssCls), sys._getframe().f_code.co_name)
  def updown(self, value, delta, cssCls=None): return self.add(AresHtmlText.UpDown(self, value, delta, cssCls), sys._getframe().f_code.co_name)
  def code(self, value, cssCls=None, htmlComp=None): return self.add(AresHtmlText.Code(self, self.supp(value), cssCls, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def preformat(self, value, cssCls=None): return self.add(AresHtmlText.Preformat(self, self.supp(value), cssCls), sys._getframe().f_code.co_name)
  def blockquote(self, value, cssCls=None): return self.add(AresHtmlText.BlockQuote(self, self.supp(value), cssCls), sys._getframe().f_code.co_name)
  def paragraph(self, value, cssCls=None, htmlComp=None): return self.add(AresHtmlText.Paragraph(self, self.supp(value), cssCls, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def dropzone(self, value, cssCls=None): return self.add(AresHtmlEvent.DropZone(self, value, cssCls), sys._getframe().f_code.co_name)
  def dropfile(self, value, cssCls=None): return self.add(AresHtmlEvent.DropFile(self, value, cssCls), sys._getframe().f_code.co_name)
  def newline(self, cssCls=None): return self.add(AresHtmlText.Newline(self, '', cssCls), sys._getframe().f_code.co_name)
  def line(self, cssCls=None): return self.add(AresHtmlText.Line(self, '', cssCls), sys._getframe().f_code.co_name)
  def icon(self, value, cssCls=None): return self.add(AresHtmlText.Icon(self, value, cssCls), sys._getframe().f_code.co_name)
  def number(self, value, cssCls=None): return self.add(AresHtmlText.Numeric(self, value, cssCls), sys._getframe().f_code.co_name)
  def wiki(self, dataSourceName, value, cssCls=None): return self.add(AresHtmlText.Wiki(self, dataSourceName, value, cssCls), sys._getframe().f_code.co_name)


  # Title section
  def title(self, value, cssCls=None): return self.add(AresHtmlText.Title(self, value, cssCls), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title2(self, value, cssCls=None): return self.add(AresHtmlText.Title2(self, value, cssCls), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title3(self, value, cssCls=None): return self.add(AresHtmlText.Title3(self, value, cssCls), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title4(self, value, cssCls=None): return self.add(AresHtmlText.Title4(self, value, cssCls), sys._getframe().f_code.co_name) # Need to be linked to the NavBar


  # Button Section
  def refresh(self, value, recordSet, ajaxScript, withDataFiles=False, cssCls=None): return self.add(AresHtmlButton.ButtonRefresh(self, value, recordSet, ajaxScript, withDataFiles, cssCls), sys._getframe().f_code.co_name)
  def remove(self, cssCls=None): return self.add(AresHtmlButton.ButtonRemove(self, '', cssCls), sys._getframe().f_code.co_name)
  def download(self, cssCls=None): return self.add(AresHtmlButton.ButtonDownload(self, '', cssCls), sys._getframe().f_code.co_name)
  def downloadAll(self, value='', cssCls=None): return self.add(AresHtmlButton.ButtonDownloadAll(self, value, cssCls), sys._getframe().f_code.co_name)
  def button(self, value, cssCls=None): return self.add(AresHtmlButton.Button(self, value, cssCls), sys._getframe().f_code.co_name)
  def ok(self, value, cssCls=None): return self.add(AresHtmlButton.ButtonOk(self, value, cssCls), sys._getframe().f_code.co_name)

  # Meter
  def meter(self, value, headerBox=None, cssCls=None): return self.add(AresHtmlMeter.Meter(self, headerBox, value, cssCls), sys._getframe().f_code.co_name)

  # Map
  def map(self, cssCls=None): return self.add(AresHtmlMap.Map(self, cssCls), sys._getframe().f_code.co_name)


  # Generic Action section
  def slider(self, value, cssCls=None): return self.add(AresHtmlEvent.Slider(self, value, cssCls), sys._getframe().f_code.co_name)
  def date(self, label='Date', cssCls=None): return self.add(AresHtmlEvent.DatePicker(self, label, cssCls), sys._getframe().f_code.co_name)
  def textArea(self, value, cssCls=None): return self.add(AresHtmlEvent.TextArea(self, value, cssCls), sys._getframe().f_code.co_name)
  def generatePdf(self, fileName=None, cssCls=None): return self.add(AresHtmlButton.GeneratePdf(self, fileName, cssCls), sys._getframe().f_code.co_name)

  # Containers section
  def div(self, value, cssCls=None): return self.add(AresHtmlContainer.Div(self, value, cssCls), sys._getframe().f_code.co_name)
  def list(self, values, headerBox=None, cssCls=None): return self.add(AresHtmlContainer.List(self, headerBox, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def listbadge(self, values, cssCls=None): return self.add(AresHtmlContainer.ListBadge(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def table(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlTable.Table(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def tabs(self, values, cssCls=None): return self.add(AresHtmlContainer.Tabs(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def dropdown(self, values, cssCls=None): return self.add(AresHtmlEvent.DropDown(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def select(self, values, selected=None, cssCls=None): return self.add(AresHtmlEvent.Select(self, self.supp(values), selected, cssCls), sys._getframe().f_code.co_name)
  def select_group(self, values, cssCls=None): return self.add(AresHtmlEvent.SelectWithGroup(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def container(self, header, values, cssCls=None): return self.add(AresHtmlContainer.Container(self, header, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def row(self, values, cssCls=None): return self.add(AresHtmlContainer.Row(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def col(self, values, cssCls=None): return self.add(AresHtmlContainer.Col(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def img(self, values, cssCls=None): return self.add(AresHtmlContainer.Image(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def iframe(self, values, cssCls=None): return self.add(AresHtmlContainer.IFrame(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)

  # Modal Section
  def modal(self, values, cssCls=None): return self.add(AresHtmlModal.Modal(self, self.supp(values), cssCls), sys._getframe().f_code.co_name)

  # Chart section
  def bar(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.Bar(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def pie(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.Pie(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def donut(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.Donut(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def lineChart(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.Line(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def stackedAreaChart(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.StackedArea(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def multiBarChart(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.MultiBars(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def lineChartFocus(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.LineWithFocus(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def horizBarChart(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.HorizontalBars(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def comboLineBar(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.ComboLineBar(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def scatterChart(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraph.ScatterChart(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def cloud(self, values, header, headerBox=None, cssCls=None): return self.add(AresHtmlGraphWordCloud.WordCloud(self, headerBox, self.register(self.suppRec(values), header), header, cssCls), sys._getframe().f_code.co_name)
  def tree(self, values, header, cssCls=None): return self.add(AresHtmlGraph.IndentedTree(self, header, values, mapCols, selectors, cssCls), sys._getframe().f_code.co_name)

  # File HTML Section
  def upload(self, values='', cssCls=None): return self.add(AresHtmlEvent.UploadFile(self, values, cssCls), sys._getframe().f_code.co_name)


  # Anchor section
  def anchor(self, value, **kwargs): return self.add(AresHtmlHRef.A(self, self.supp(value), **kwargs), sys._getframe().f_code.co_name)
  def external_link(self, value, url, **kwargs): return self.add(AresHtmlHRef.ABespoke(self, self.supp(value), url, **kwargs), sys._getframe().f_code.co_name)

  def anchor_download(self, value, **kwargs): return self.add(AresHtmlHRef.Download(self, self.supp(value), **kwargs), sys._getframe().f_code.co_name)
  def anchor_set_env(self, value, **kwargs): return self.add(AresHtmlHRef.CreateEnv(self, self.supp(value), **kwargs), sys._getframe().f_code.co_name)
  def anchor_add_scripts(self, value, **kwargs): return self.add(AresHtmlHRef.AddScript(self, self.supp(value), **kwargs), sys._getframe().f_code.co_name)
  def main(self, value, **kwargs): return self.add(AresHtmlHRef.ScriptPage(self, self.supp(value), **kwargs), sys._getframe().f_code.co_name)
  def input(self, value='', cssCls=None): return self.add(AresHtmlEvent.Input(self, value, cssCls), sys._getframe().f_code.co_name)

  def handleRequest(self, method, params, js="", cssCls=None): return self.add(AresHtmlAjaxCall.HandleRequest(self, method, params, js, cssCls), sys._getframe().f_code.co_name)

  # Designer objects
  def aresInput(self, cssCls=None): return self.add(AresHtmlText.TextInput(self, 'Put your text here', cssCls), sys._getframe().f_code.co_name)
  def aresDataSource(self, cssCls=None): return self.add(AresHtmlText.DataSource(self, 'Drop here', cssCls), sys._getframe().f_code.co_name)
  def aresDragItems(self, vals, cssCls=None): return self.add(AresHtmlText.DragItems(self, vals, cssCls), sys._getframe().f_code.co_name)

  def components(self):
    """ Get the list of component available in the framework """
    comp = []
    for aresModule in [AresHtmlText]:
      for name, cls in inspect.getmembers(aresModule):
        if inspect.isclass(cls) and cls.alias is not None:
          comp.append(cls.alias)
    return comp


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
  def configFile(self, fileName):
    """ Return the object in the configuration file from the json file """
    confFilg = open(os.path.join(self.http['DIRECTORY'], 'config', fileName))
    data = json.load(confFilg)
    confFilg.close()
    return data

  def getViews(self, fileName):
    """ Return the object in the Statics area with the views parameters """
    confFilg = open(os.path.join(self.http['DIRECTORY'], 'statics', fileName))
    data = confFilg.read()
    confFilg.close()
    return data

  def listDataFrom(self, folder):
    """ List the file available in the folder in the output area """
    folders = []
    for (path, dirs, files) in os.walk(os.path.join(self.http['DIRECTORY'], 'outputs', folder)):
      for file in files:
        fileData =  self.getFileInfo(file, ['outputs', folder])
        fileData.update({'folderPath': folder, 'file': file})
        folders.append(fileData)
    return folders

  def open(self, fileName, typeFile='r', folder=None):
    """ Return a python file object is the selected type """
    if folder is None:
      outPath = os.path.join(self.http['DIRECTORY'], 'outputs')
    else:
      outPath = os.path.join(self.http['DIRECTORY'], 'outputs', folder)
      if not os.path.exists(outPath):
        os.makedirs(outPath)
    # Open the file and register it in the Ares File Manager
    # This will be monitored by the framework to close the files
    fileFullPath = os.path.join(outPath, fileName)
    self.fileManager[fileFullPath] = open(fileFullPath, typeFile)
    return self.fileManager[fileFullPath]

  def logs(self, reportName):
    """ Return the log file """
    fileFullPath = os.path.join(self.http['DIRECTORY'], reportName, 'log_ares.dat')
    if os.path.exists(fileFullPath):
      self.fileManager[fileFullPath] = open(fileFullPath, 'r')
      return self.fileManager[fileFullPath]

    return None

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




  def html(self):
    """

    """
    onloadParts, htmlParts, jsSection, jsGraphs = set(), [], [], []
    for objId in self.content:
      jsOnload, html, js = self.htmlItems[objId].html()
      for ref, data in self.jsRegistered.items():
        onloadParts.add("        var recordSet_%s = %s ;" % (ref, json.dumps(data, default=jsonDefault)))
      for ref in self.jsGlobal.keys():
        onloadParts.add("        var %s ;" % ref)

      for onloadFnc in jsOnload:
        onloadParts.add(onloadFnc)
      htmlParts.append(html)
      for jsType, jsFncs in js.items():
        if jsType == 'addGraph':
          jsGraphs.append("\n".join(jsFncs))
        else:
          jsSection.append("\n".join(jsFncs))

    importMng = AresJsModules.ImportManager()
    jsSection.append("nv.addGraph(function() {\n %s \n});" % "\n".join(jsGraphs))
    return importMng.cssResolve(self.cssImport), importMng.jsResolve(self.jsImports), "\n".join(onloadParts), "\n".join(htmlParts), "\n".join(jsSection)
