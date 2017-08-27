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
import collections

from ares.Lib import AresHtmlContainer
from ares.Lib import AresHtmlEvent
from ares.Lib import AresHtmlText
from ares.Lib import AresHtmlTable
from ares.Lib import AresHtmlGraph
from ares.Lib import AresHtmlAlert
from ares.Lib import AresHtmlModal
from ares.Lib import AresItem


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
    if file == '__pycache__' or file.endswith('pyc') or file.endswith('.zip') or file == 'log_ares.dat'  or file == '__init__.py':
      return True

  if folders is not None:
    folder = os.path.join(*folders)
    if '__pycache__' in folder or folder == rootPath or '.svn' in folder:
      return True

  return False

class Report(object):
  """

  """

  # This list should not be changed
  definedNotif = {'SUCCESS': 'SuccessAlert', 'INFO': 'InfoAlert', 'WARNING': 'WarningAlert', 'DANGER': 'DangerAlert'}
  showNavMenu = False

  def __init__(self, prefix=''):
    """
    """
    # Internal variable that should not be used directly
    # Those variable will drive the report generation
    self.countItems, self.countNotif = 0, 0
    self.prefix, self.directory = prefix, None
    self.content, self.jsGraph = [], []
    self.currentTitleObj, self.navBarContent = {}, {'content': []}
    self.htmlItems, self.jsOnLoad, self.http = {}, [], {}
    self.notifications = collections.defaultdict(list)
    self.interruptReport = (False, None)

  def structure(self):
    return self.content

  def addNavigationBar(self, width=25, cssCls=None):
    self.showNavMenu = True
    self.navBarContent.update({'width': width, 'cssCls': cssCls})

  def addNotification(self, notifType, title, value, cssCls=None, backgroundColor=None, closeButton=True):
    """ Add a user notfication to the report """
    notif = notifType.upper()
    if not notif in self.definedNotif:
      print("Notification %s not recognized !" % notif)
      print("Allowed notification %s" % self.definedNotif.keys())
      raise Exception("Notification Type should belong to one of the above category")

    alertCls = getattr(AresHtmlAlert, self.definedNotif[notif])
    alertObject = alertCls(self.countItems, title, value, self.countNotif, cssCls=cssCls, backgroundColor=backgroundColor, closeButton=closeButton)
    self.htmlItems[alertObject.htmlId] = alertObject
    self.content.append(alertObject.htmlId)
    if notif == 'DANGER':
      self.interruptReport = (True, alertObject.htmlId)  # we keep track of the object since this is the only thing we will display
    self.countItems += 1
    self.countNotif += 1
    return alertObject

  def item(self, itemId):
    """ Return the HTML object """
    return self.htmlItems[itemId]

  def getNext(self):
    """ Return the next ID available for a HTML component """
    self.countItems += 1
    return self.countItems

  def add(self, htmlObj, fncName):
    """ Register the HTML component to the Ares object """
    if fncName != htmlObj.alias:
      raise Exception("%s not register for the Ares function %s" % (htmlObj.alias, fncName))

    self.htmlItems[htmlObj.htmlId] = htmlObj
    self.content.append(htmlObj.htmlId)
    return htmlObj

  def supp(self, htmlObjs):
    """ Unregister the HTML component to the Ares object """
    if htmlObjs is None:
      return htmlObjs

    if isinstance(htmlObjs, list):
      for htmlObj in htmlObjs:
        if isinstance(htmlObj, list):
          for val in htmlObj:
            if hasattr(val, 'htmlId'):
              try:
                del self.content[self.content.index(val.htmlId)]
              except:
                print("PROBLEME")
                pass
        else:
          if hasattr(htmlObj, 'htmlId'):
            try:
              del self.content[self.content.index(htmlObj.htmlId)]
            except:
              print("PROBLEME")
              pass
    else:
      if hasattr(htmlObjs, 'htmlId'):
        del self.content[self.content.index(htmlObjs.htmlId)]
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
  def text(self, value, cssCls=None, htmlComp=None): return self.add(AresHtmlText.Text(self.getNext(), self.supp(value), cssCls, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def code(self, value, cssCls=None, htmlComp=None): return self.add(AresHtmlText.Code(self.getNext(), self.supp(value), cssCls, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def paragraph(self, value, cssCls=None, htmlComp=None): return self.add(AresHtmlText.Paragraph(self.getNext(), self.supp(value), cssCls, self.supp(htmlComp)), sys._getframe().f_code.co_name)
  def dropzone(self, value, cssCls=None): return self.add(AresHtmlEvent.DropZone(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def dropfile(self, value, cssCls=None): return self.add(AresHtmlEvent.DropFile(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def newline(self, cssCls=None): return self.add(AresHtmlText.Newline(self.getNext(), '', cssCls), sys._getframe().f_code.co_name)
  def line(self, cssCls=None): return self.add(AresHtmlText.Line(self.getNext(), '', cssCls), sys._getframe().f_code.co_name)
  def icon(self, value, cssCls=None): return self.add(AresHtmlText.Icon(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def number(self, value, cssCls=None): return self.add(AresHtmlText.Numeric(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)

  # Title section
  def title(self, value, cssCls=None): return self.add(AresHtmlText.Title(self.getNext(), value, cssCls), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title2(self, value, cssCls=None): return self.add(AresHtmlText.Title2(self.getNext(), value, cssCls), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title3(self, value, cssCls=None): return self.add(AresHtmlText.Title3(self.getNext(), value, cssCls), sys._getframe().f_code.co_name) # Need to be linked to the NavBar
  def title4(self, value, cssCls=None): return self.add(AresHtmlText.Title4(self.getNext(), value, cssCls), sys._getframe().f_code.co_name) # Need to be linked to the NavBar

  # Action section
  def slider(self, value, cssCls=None): return self.add(AresHtmlEvent.Slider(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def date(self, label='Date', cssCls=None): return self.add(AresHtmlEvent.DatePicker(self.getNext(), label, cssCls), sys._getframe().f_code.co_name)
  def textArea(self, value, cssCls=None): return self.add(AresHtmlEvent.TextArea(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def button(self, value, cssCls=None): return self.add(AresHtmlEvent.Button(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def remove(self, cssCls=None): return self.add(AresHtmlEvent.ButtonRemove(self.getNext(), '', cssCls), sys._getframe().f_code.co_name)
  def download(self, cssCls=None): return self.add(AresHtmlEvent.ButtonDownload(self.getNext(), '', cssCls), sys._getframe().f_code.co_name)
  def downloadAll(self, value='', cssCls=None): return self.add(AresHtmlEvent.ButtonDownloadAll(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def ok(self, value, cssCls=None): return self.add(AresHtmlEvent.ButtonOk(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def generatePdf(self, fileName=None, cssCls=None): return self.add(AresHtmlEvent.GeneratePdf(self, fileName, cssCls), sys._getframe().f_code.co_name) # hack: I need the full aresObj to generate the pdf, hence I pass self and not self.getNext() as param

  # Containers section
  def div(self, value, cssCls=None): return self.add(AresHtmlContainer.Div(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)
  def listbadge(self, values, cssCls=None): return self.add(AresHtmlContainer.ListBadge(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def table(self, header, values, cssCls=None): return self.add(AresHtmlTable.Table(self.getNext(), header, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def tableRec(self, headerBox, values, header, cssCls=None): return self.add(AresHtmlTable.TableRec(self.getNext(), headerBox, self.supp(values), header, cssCls), sys._getframe().f_code.co_name)
  def tabs(self, values, cssCls=None): return self.add(AresHtmlContainer.Tabs(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def dropdown(self, values, cssCls=None): return self.add(AresHtmlEvent.DropDown(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def select(self, values, cssCls=None): return self.add(AresHtmlEvent.Select(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def container(self, header, values, cssCls=None): return self.add(AresHtmlContainer.Container(self.getNext(), header, self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def grid(self, values, cssCls=None): return self.add(AresHtmlContainer.Split(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def row(self, values, cssCls=None): return self.add(AresHtmlContainer.Row(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def img(self, values, cssCls=None): return self.add(AresHtmlContainer.Image(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)
  def iframe(self, values, cssCls=None): return self.add(AresHtmlContainer.IFrame(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)

  # Modal Section
  def modal(self, values, cssCls=None): return self.add(AresHtmlModal.Modal(self.getNext(), self.supp(values), cssCls), sys._getframe().f_code.co_name)

  # Chart section
  def bar(self, header, values, mapCols, selectors, cssCls=None): return self.add(AresHtmlGraph.Bar(self.getNext(), header, values, mapCols, selectors, cssCls), sys._getframe().f_code.co_name)
  def pieChart(self, header, values, mapCols, selectors, cssCls=None): return self.add(AresHtmlGraph.Pie(self.getNext(), header, values, mapCols, selectors, cssCls), sys._getframe().f_code.co_name)
  def donutChart(self, header, values, mapCols, selectors, cssCls=None): return self.add(AresHtmlGraph.Donut(self.getNext(), header, values, mapCols, selectors, cssCls), sys._getframe().f_code.co_name)
  def lineChart(self, header, values, cssCls=None): return self.add(AresHtmlGraph.Line(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)
  def cloudChart(self, header, values, cssCls=None): return self.add(AresHtmlGraph.WordCloud(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)
  def tree(self, values, header, cssCls=None): return self.add(AresHtmlGraph.IndentedTree(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)
  def comboLineBar(self, header, values, cssCls=None): return self.add(AresHtmlGraph.ComboLineBar(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)
  def scatterChart(self, header, values, cssCls=None): return self.add(AresHtmlGraph.ScatterChart(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)
  def stackedAreaChart(self, header, values, cssCls=None): return self.add(AresHtmlGraph.StackedArea(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)
  def multiBarChart(self, header, values, cssCls=None): return self.add(AresHtmlGraph.MultiBars(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)
  def lineChartFocus(self, header, values, cssCls=None): return self.add(AresHtmlGraph.LineWithFocus(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)
  def horizBarChart(self, header, values, cssCls=None): return self.add(AresHtmlGraph.HorizontalBars(self.getNext(), header, values, cssCls), sys._getframe().f_code.co_name)

  # File HTML Section
  def upload(self, values='', cssCls=None): return self.add(AresHtmlEvent.UploadFile(self.getNext(), values, cssCls), sys._getframe().f_code.co_name)

  # Anchor section
  def anchor(self, value='', cssCls=None): return self.add(AresHtmlEvent.A(self.getNext(), self.supp(value), self.reportName, self.childPages, self.directory, cssCls), sys._getframe().f_code.co_name)
  def input(self, value='', cssCls=None): return self.add(AresHtmlEvent.Input(self.getNext(), value, cssCls), sys._getframe().f_code.co_name)


  # ---------------------------------------------------
  #    Action on files and folders reaad and write
  #
  # ---------------------------------------------------

  # TODO add the closure in ares when the report is running
  # It should not be the user responsible to close the files

  def readFile(self, file, subfolders=None):
    """
    This function will read a file in the list of sub folder
    that the user will select in the report directory
    """
    if subfolders is not None:
      filePath = os.path.join(self.http['DIRECTORY'], *subfolders)
      filePath = os.path.join(filePath, file)
    else:
      filePath = os.path.join(self.http['DIRECTORY'], file)

    if os.path.exists(filePath):
      return open(filePath)

    return None

  def createFile(self, file, subfolders=None, checkFileExist=True):
    """
    This function will create a file in the folder that the user will select
    This function will return an error is the file already exist and we try to override it
    You can change the flag to False if you do not want to fail
    """
    if checkFileExist:
      if subfolders is not None:
        subFolderDirectory = os.path.join(self.http['DIRECTORY'], *subfolders)
        subFolderDirectory = os.path.join(subFolderDirectory, file)
        if os.path.exists(subFolderDirectory):
          print("%s file already created on the server" % file)
          return None

      else:
        if os.path.exists(os.path.join(self.http['DIRECTORY'], file)):
          print("%s file already created on the server" % file)
          return None

    if subfolders is None:
      return open(os.path.join(self.http['DIRECTORY'], file), 'w')

    subFolderDirectory = os.path.join(self.http['DIRECTORY'], *subfolders)
    if not os.path.exists(subFolderDirectory):
      os.makedirs(subFolderDirectory)
    return open('%s\%s' % (subFolderDirectory, file), 'w')

  def getFolders(self):
    """ Return the list of sub folders in tne environment """
    folders = set()
    for folder in os.walk(os.path.join(self.http['DIRECTORY'])):
      if isExcluded(self.http['DIRECTORY'], folders=[folder[0]]):
        continue

      fPath = list(os.path.split(folder[0].lstrip("\\").replace(self.http['DIRECTORY'], '').lstrip("\\")))
      folders.add(tuple(fPath[1:])) if fPath[0] == '' else folders.add(tuple(fPath))
    return folders

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
    for htmlId in self.content:
      jsOnload, html, js = self.htmlItems[htmlId].html()
      for onloadFnc in jsOnload:
        onloadParts.add(onloadFnc)
      htmlParts.append(html)
      for jsType, jsFncs in js.items():
        if jsType == 'addGraph':
          jsGraphs.append("\n".join(jsFncs))
        else:
          jsSection.append("\n".join(jsFncs))

    jsSection.append("nv.addGraph(function() {\n %s });" % "\n".join(jsGraphs))
    return "\n".join(onloadParts), "\n".join(htmlParts), "\n".join(jsSection)
