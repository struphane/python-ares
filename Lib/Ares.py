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
import inspect
import Lib.AresHtml as AresHtml
import Lib.AresGraph as AresGraph

htmlFactory = None # This is the factory with all the alias and HTML classes
# the below global variables are only used locally to generate the secondary pages and Ajax calls
LOCAL_DIRECTORY, LOCAL_STATIC_PATH, LOCAL_CSSFILES, LOCALJSFILES = None, None, None, None
RESULT_FOLDER = 'html' # This is the folder with all the HTML files, it is only used locally

def mapHtmlItems():
  """ Map the aliases to the HTML objects """
  htmlObjs = {}
  for name, obj in inspect.getmembers(AresHtml):
    if inspect.isclass(obj) and obj.alias is not None:
      htmlObjs[obj.alias] = obj
  return htmlObjs

def htmlLocalHeader(directory, report, statisPath, cssFiles, javascriptFiles):
  """ Add the header to the report when we are producing a text file - namely local run """
  global LOCAL_DIRECTORY, LOCAL_STATIC_PATH, LOCAL_CSSFILES, LOCALJSFILES

  if RESULT_FOLDER and LOCAL_DIRECTORY is None:
    # This will move all the results in a html folder
    # It only work locally
    directory = os.path.join(directory, RESULT_FOLDER, report)
    if not os.path.exists(directory):
      os.makedirs(directory)

    if not statisPath:
      localPathSize = len(os.path.split(directory))
      if os.path.split(directory)[0] == '':
        localPathSize -= 1

      statisPath = os.path.join(*[".." for i in range(localPathSize)])

  LOCAL_DIRECTORY, LOCAL_STATIC_PATH, LOCAL_CSSFILES, LOCALJSFILES = directory, statisPath, cssFiles, javascriptFiles
  htmlFile = open(r"%s\%s.html" % (directory, report), "w")
  htmlFile.write('<!DOCTYPE html>\n')
  htmlFile.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr"> \n')
  htmlFile.write('<head>\n')
  htmlFile.write('%s<meta charset="utf-8">\n' % AresHtml.INDENT)
  htmlFile.write('%s<meta http-equiv="X-UA-Compatible" content="IE=edge">\n' % AresHtml.INDENT)
  htmlFile.write('%s<meta name="viewport" content="width=device-width, initial-scale=1">\n' % AresHtml.INDENT)
  htmlFile.write('%s<title>Local HTML Report</title>\n' % AresHtml.INDENT)
  for style in cssFiles:
    htmlFile.write('%s<link rel="stylesheet" href="%s" type="text/css">\n' % (AresHtml.INDENT, os.path.join(statisPath, 'css', style)))
  for javascript in javascriptFiles:
    htmlFile.write('%s<script src="%s"></script>\n' % (AresHtml.INDENT, os.path.join(statisPath, 'js', javascript)))
  htmlFile.write('</head>\n')
  htmlFile.write('<body><div class="container">\n\n')

  return htmlFile

def htmlLocalFooter(htmlFile):
  """ Close all the HTML report and close the input text File - namely locally """
  htmlFile.write('\n</div>\n</body>\n')
  htmlFile.write('</html>\n')
  htmlFile.close()


def addGraphObject(chartName, width=960, height=500, withSvg=True, cssCls=None):
  def addChart(func):
    def wrapper(self, *args, **kwargs):
      paramArgs = {'width': width, 'height': height, 'cssCls': cssCls}
      paramArgs.update(kwargs)
      # for now this call to func is useless but I leave it for the day someone wants to do a special treatment in a new graph
      func(self, *args, **kwargs)

      if hasattr(AresGraph, chartName):
        graphContainer = AresHtml.Graph(self.countItems, paramArgs['width'], paramArgs['height'], withSvg=withSvg, cssCls=paramArgs['cssCls'])
        self.htmlItems[graphContainer.htmlId] = graphContainer
        self.content.append(graphContainer.htmlId)
        self.countItems += 1

        graphObject = getattr(AresGraph, chartName)(graphContainer.htmlId, *args)
        self.jsGraph.append(graphObject)
        return graphContainer.htmlId
    return wrapper
  return addChart

def addHtmlObject(addNavBar=False):
  """ Simple decorator to add basic html objects """
  functionMapping = {'grid': 'split', 'anchor': 'a'}
  def addHtml(func):
    def wrapper(self, *args, **kwargs):
      func(self, *args, **kwargs)
      for member in dir(AresHtml):
        funcName = func.__name__
        if member.upper() == funcName.upper() or functionMapping.get(funcName, 'UNK#FUNC').upper() == member.upper():
          htmlObj = getattr(AresHtml, member)(self.countItems, *args)
          self.htmlItems[htmlObj.htmlId] = htmlObj
          self.content.append(htmlObj.htmlId)
          if addNavBar:
            self.navTitle.append(htmlObj)
          self.countItems += 1
          return htmlObj.htmlId
      else:
        raise Exception("No object is configured yet for %s" % func.__name__)
    return wrapper
  return addHtml

class Report(object):
  """
  Ares Interface

  Main module to link the user reports and the HTML and Graph modules.

  """

  def __init__(self, prefix=''):
    """
    """
    global htmlFactory

    # Internal variable that should not be used directly
    # Those variable will drive the report generation
    self.countItems = 0
    self.prefix = prefix
    self.content, self.jsGraph, self.navTitle = [], [], []
    self.htmlItems, self.jsOnLoad, self.http = {}, {}, {'GET': {}, 'POST': {}}

    if htmlFactory is None:
      htmlFactory = mapHtmlItems()
    #for name, htmlCls in htmlFactory.items():
    #  print(name)

  def structure(self):
    return self.content

  def item(self, itemId):
    """ Return the HTML object """
    return self.htmlItems[itemId]

  @addHtmlObject()
  def div(self, value):
    """

    Return the object ID to help on getting the object back. In any time during the
    report generation. THis ID is not supposed to change and it will be the
    """
    pass

  @addHtmlObject()
  def list(self, values):
    """ """
    pass

  @addHtmlObject()
  def table(self, cols, values):
    """ """
    pass

  @addHtmlObject()
  def dropDown(self, title, values):
    """ """
    pass

  @addHtmlObject()
  def dropZone(self):
    """ """
    pass

  @addHtmlObject()
  def textArea(self):
    """ """
    pass

  @addHtmlObject()
  def select(self, values):
    """ """
    pass

  @addHtmlObject()
  def container(self, htmlObj):
    """ """
    del self.content[self.content.index(htmlObj.htmlId)] # Is not defined in the root structure

  @addHtmlObject()
  def grid(self, htmlObjLeft, htmlObjRight):
    """ """
    del self.content[self.content.index(htmlObjLeft.htmlId)] # Is not defined in the root structure
    del self.content[self.content.index(htmlObjRight.htmlId)] # Is not defined in the root structure

  @addHtmlObject()
  def button(self, value, cssCls=None):
    """ """
    pass

  @addHtmlObject()
  def input(self, name, value):
    """ """
    pass

  @addHtmlObject
  def comment(self, name, value):
    """ """
    pass

  @addHtmlObject()
  def text(self, value, cssCls=None):
    """ """
    pass

  @addHtmlObject()
  def code(self, value, cssCls=None):
    """ """
    pass

  @addHtmlObject()
  def paragraph(self, value, textObjsList=None, cssCls=None):
    """ """
    if textObjsList is not None:
      for textObj in textObjsList:
        del self.content[self.content.index(textObj.htmlId)] # Is not defined in the root structure

  def modal(self, value, cssCls=None):
    """ """
    htmlObject = AresHtml.Modal(self.countItems, value, Report("modal_%s_" % self.countItems), cssCls=cssCls)
    self.htmlItems[htmlObject.htmlId] = htmlObject
    self.content.append(htmlObject.htmlId)
    self.countItems += 1
    return htmlObject.htmlId

  @addHtmlObject(addNavBar=True)
  def title(self, dim, value, cssCls=None):
    """ """
    pass

  @addGraphObject('Donut')
  def pieChart(self, values, width=960, height=500, cssCls=None):
    """ Construct a Pie Chart in the HTML page """
    pass

  @addGraphObject('WordCloud')
  def cloudChart(self, values, width=960, height=500, cssCls=None):
    """ Construct a Pie Chart in the HTML page """
    pass

  @addGraphObject('IndentedTree', withSvg=False)
  def tree(self, cols, values, width=960, height=500, cssCls=None):
    """ """
    pass

  @addGraphObject('ComboLineBar')
  def comboLineBar(self, values, width=960, height=500, cssCls=None):
    """ Construct a Pie Chart in the HTML page """
    pass

  #don't use the decorator as this function needs to change the value of some parameters before doing the generic processing
  def anchor(self, value, link, structure, localPath, cssCls=None):
    """ Add an anchor HTML tag to the report """
    if localPath is not None:
      # There is a child and we need to produce the sub Report attached to it
      # The below part allow also to test locally the get and post method that we put in the URL
      # Basically the Wrapper will create all tehe secondary pages using all the different parameters
      splitUrl  = link.split("?")
      childReport = structure[splitUrl[0]].replace(".py", "")
      htmlPage = htmlLocalHeader(LOCAL_DIRECTORY, childReport, LOCAL_STATIC_PATH, LOCAL_CSSFILES, LOCALJSFILES)
      aresObj = Report()
      if len(splitUrl) > 1:
        aresObj.http['GET'] = {}
        for urlVar in splitUrl[1].split('&'):
          varName, varVal = urlVar.split("=")
          aresObj.http['GET'][varName] = varVal
      htmlPage.write(__import__(childReport).report(aresObj, localPath=LOCAL_DIRECTORY))
      htmlLocalFooter(htmlPage)
      link = "%s.html" % childReport
    else:
      splitUrl  = link.split("?")
      if len(splitUrl) > 1:
        link = "../reports_child/%s?%s" % (structure[splitUrl[0]].replace(".py", ""), splitUrl[1])
      else:
        link = "../reports_child/%s" % (structure[splitUrl[0]].replace(".py", ""))

    htmlObject = AresHtml.A(self.countItems, value, link, cssCls=cssCls)
    self.htmlItems[htmlObject.htmlId] = htmlObject
    self.content.append(htmlObject.htmlId)
    self.countItems += 1
    return htmlObject.htmlId


  def html(self, localPath, title=None, menu=True):
    """ Main function used to generate the report

    """
    # TODO: add the menu
    results, jsResults = [], []

    results.append('<script>')
    for jsOnLoad in self.jsOnLoad.keys():
      results.append(jsOnLoad)
    results.append('</script>')

    if menu:
      results.append('<div class="page-wrapper">')
      results.append('%s<div class="doc-wrapper">' % AresHtml.INDENT)
      results.append('%s%s<div class="container">' % (AresHtml.INDENT, AresHtml.INDENT))
      results.append('%s%s<div class="doc-body">' % (AresHtml.INDENT, AresHtml.INDENT))
      results.append('%s%s%s<div class="doc-sidebar hidden-xs">' % (AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT))
      results.append('%s%s%s%s<nav id="doc-nav">' % (AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT))
      results.append('%s%s%s%s%s<ul id="doc-menu" class="nav doc-menu" data-apy="affix">' % (AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT, AresHtml.INDENT))
      for section in self.navTitle:
        #subItems = self.navBar[section]
        results.append('<li><a href="%s">%s</a></li>' % (section.htmlId, section.val))
        #if subItems:
        #  jsResults.append('<ul class="nav doc-sub-menu">')
        #  for subItems in subItems:
        #    jsResults.append('<li><a href="%s">%s</a></li>')
        #  jsResults.append('</ul>')
      results.append("</ul></nav></div>")
    if title is not None:
      titleObj = AresHtml.Title(self.countItems, 1, title)
      results.append(titleObj.html(localPath))
    results.append('</div></div></div></div>')

    for htmlId in self.content:
      print (self.htmlItems[htmlId])
      results.append(self.htmlItems[htmlId].html(localPath))
      if self.htmlItems[htmlId].jsEvent is not None:
        for fnc, fncDef in self.htmlItems[htmlId].jsEvent:
          if fnc in ['drop', 'dragover']:
            jsResults.append('%s.bind("%s", function (event){' % (self.htmlItems[htmlId].jsRef(), fnc))
            jsResults.append(fncDef)
            jsResults.append('});\n')
          elif fnc in ['autocomplete']:
            jsResults.append(fncDef)
          else:
            jsResults.append('%s.%s(function(){' % (self.htmlItems[htmlId].jsRef(), fnc))
            jsResults.append(fncDef)
            jsResults.append('});\n')

    if self.jsGraph:
      jsResults.append("nv.addGraph(function() {\n")
      for jsgraphs in self.jsGraph:
        jsResults.append(jsgraphs.js(localPath))
        jsResults.append("\n\n")
      jsResults.append("});\n")

    # Section dedicated to write all the extra Javascript callback functions
    # This will allow the page to be interactive
    results.append("<script>")
    results.extend(jsResults)
    results.append("</script>\n")
    return "\n".join(results)
