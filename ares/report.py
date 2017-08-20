""" Special app for the report section

"""

import json
import os
import sys
import zipfile
import io
import collections
import traceback
import time

from flask import current_app, Blueprint, render_template, request, send_from_directory, send_file, make_response

import config

# TODO add a check on the variable DIRECTORY to ensure that it cannot be changed

# Ares Framework
from ares.Lib import Ares

from ares import report_index, report_index_page, report_index_set

report = Blueprint('ares', __name__, url_prefix='/reports')

# Return the list of all the scripts needed to run this package
# This will group all the module CSS, JS and Python scripts
LIB_PACKAGE = {
  'JS': ['jquery-3.2.1.min.js', 'jquery-ui.min.js', 'bootstrap.min.js', 'bootstrap-select.min.js', 'd3.v3.js',
         'nv.d3.js', 'd3.layout.cloud.js'],
  'CSS': ['jquery-ui.css', 'bootstrap.min.css', 'bootstrap-theme.min.css', 'nv.d3.css',
          'bootstrap-select.min.css', 'w3.css'],
  'JSON': ['horizBars.json', 'linePlusBarData.json', 'lineWithFocus.json', 'multiBar.json', 'stackedAreaData.json']
}

def getScriptChildren(env, scriptName, scriptTree, ajaxCalls):
  """ Return the list of script attached to a script """
  if os.path.isfile(os.path.join(env, scriptName)):
    mod = __import__(scriptName.replace(".py", ""))
    children = getattr(mod, 'CHILD_PAGES', {}).values()
    ajax = getattr(mod, 'AJAX_CALLS', [])
    for js in ajax:
      ajaxCalls[scriptName].append(js)
    if not children:
      scriptTree[scriptName] = {}
    else:
      scriptTree[scriptName] = {}
      for child in children:
        scriptTree[scriptName][child] = {}
        if child not in scriptTree:
          getScriptChildren(env, child, scriptTree[scriptName], ajaxCalls)

def getChildrenFlatStruct(scriptTree, listChildren):
  """ Returns a flat list of children for a given report """
  for mainScript, children in scriptTree.items():
    for child in children.keys():
      listChildren.append((mainScript, child))
      if children[child]:
        getChildrenFlatStruct(children, listChildren)

def appendToLog(reportName, event, comment):
  """ Append an event to the dedicated log file """
  logFile = open(os.path.join(config.ARES_USERS_LOCATION, reportName, 'log_ares.dat'), 'a')
  showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")
  logFile.write("%s#%s#%s#%s\n" % (event, showtime[0], showtime[1], comment))
  logFile.close()


@report.route("/doc")
@report.route("/dsc")
@report.route("/dsc/index")
def report_dsc_index():
  """ Main page for the Ares Documentation """
  aresObj = Ares.Report()
  aresObj.reportName = 'dsc'
  aresObj.childPages = {'html': 'html', 'graph': 'graph', 'local': 'local'}
  aresObj.title("Report Documentation")
  aresObj.title2("How to create a report")
  aresObj.img('local_runs.JPG')
  aresObj.title2("Report Components")
  aresComp = aresObj.anchor('Local Environment')
  aresComp.addLink('local', dots='.')
  aresObj.newline()
  aresComp = aresObj.anchor('HTML Component documentation')
  aresComp.addLink('html', dots='.')
  aresObj.newline()
  aresComp = aresObj.anchor('Graph Component documentation')
  aresObj.img('graph.JPG')
  aresComp.addLink('graph', dots='.')
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/child:dsc/html")
def report_dsc_html():
  """ Function to return the HTML object description and a user guide """
  import inspect
  from ares.Lib import AresHtmlText
  from ares.Lib import AresHtmlEvent
  from ares.Lib import AresHtmlModal
  from ares.Lib import AresHtmlTable
  from ares.Lib import AresHtmlContainer

  aresObj = Ares.Report()
  aresObj.reportName = 'dsc/html'
  aresObj.childPages = {}
  aresObj.title("Html Components")
  for aresModule in [AresHtmlText, AresHtmlContainer, AresHtmlEvent, AresHtmlModal, AresHtmlTable]:
    aresObj.title4(aresModule.__doc__)
    htmlObject = [["Class Name", "Description", "Example", "Render"]]
    for name, cls in inspect.getmembers(aresModule):
      if inspect.isclass(cls) and cls.alias is not None:
        aresObj.childPages[name] = '../../../child:dsc/html/%s' % cls.alias
        comp = aresObj.anchor(name)
        comp.addLink(name, dots='.')

        src = inspect.getsource(cls.aresExample).split("\n", 2)[-1].replace("return ", "")
        htmlObject.append([comp, aresObj.code(cls.__doc__), aresObj.code(src), cls.aresExample(aresObj)])
    aresObj.table(htmlObject)
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/child:dsc/html/<chartName>")
def report_dsc_html_details(chartName):
  """ """
  aresObj = Ares.Report()
  aresObj.reportName = 'dsc/html'
  aresObj.childPages = {}
  aresObj.title(chartName)
  getattr(aresObj, chartName)('Youpi')
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/child:dsc/local")
def report_dsc_local_details():
  aresObj = Ares.Report()
  aresObj.reportName = None
  aresObj.childPages = {'html': 'html', 'graph': 'graph', 'download': '../download/ares'}
  aresObj.title("How to use ArES locally")
  aresObj.newline()
  aresObj.title3("What is ArES")
  aresObj.paragraph('''
                      ArES is a Python reporting suit which will allow you easily to get data from differents sources based on the different
                      available modules in the
                    ''')
  aresObj.title3("Set up your environment")
  aresObj.paragraph('''
                      The framework is very easy to set up and it will allow to perform all the tests fully locally based on your environment
                      but also to deploy your scripts easily on the server. <BR />
                      The only thing to do is to click on the Download ArES link below, unzip the archive in a folder and start writing Python codes. <BR />
                    ''')
  download = aresObj.anchor('Download ArES')
  download.addLink('download')
  localEnv = aresObj.img('local_env.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('ares_download.JPG')
  downloadPicture.doubleDots = 2
  aresObj.table([['', ''], [downloadPicture, localEnv]])
  aresObj.newline()
  aresObj.paragraph('''
                      The framework is very easy to set up and it will allow to perform all the tests fully locally based on your environment
                      but also to deploy your scripts easily on the server. <BR />
                      The only thing to do is to click on the Download ArES link, unzip the archive in a folder and start writing Python codes. <BR />
                      The structure of the reports is very intuitive and linear. Each items is fully documented in the framework and extra links are
                      available for advance users. <BR />
                      ArES is only a wrapper layer between HTML5 and Javascript, so you can directly include some part of those language to enrich your
                      components. The ArES layer will only put together your object to then build your HTML page.
                    ''')
  aresObj.title3("Run your first script")
  aresObj.paragraph('''
                        First of all create a folder with the name of your report. This name should be the name of the main script of your environment.
                        Indeed it will be the entry point to go thought your pages interactively. <BR />
                        Then copy the AresEmtpyReport.py from the Lib folder to your folder and rename it. This will give you the standard format
                        expected by the framework.

                    ''')
  localEnv = aresObj.img('first_report_1.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('first_report_2.JPG')
  downloadPicture.doubleDots = 2
  aresObj.table([['', ''], [localEnv, downloadPicture]])

  aresObj.paragraph('''
                        Then add the different HTML components to your reports !!! <BR />
                        Once your report created you can run it locally and get the result in a HTML file
                    ''')
  localEnv = aresObj.img('first_report_3.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('first_report_4.JPG')
  downloadPicture.doubleDots = 2
  aresObj.table([['Create your report', 'Run the Wrapper in your IDE'], [localEnv, downloadPicture]])

  localEnv = aresObj.img('first_report_5.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('first_report_6.JPG')
  downloadPicture.doubleDots = 2
  aresObj.table([['Get the file', 'Open it in your web browser'], [localEnv, downloadPicture]])

  aresObj.paragraph('''
                        Then once your report is finalised your can upload it to our server and share it with other user. <BR />
                        The module AresWrapperDeploy.py will allow the connection with the server. The creation of files, folder and
                        also the check of the version of your locally framework are done from script. <BR />
                        All new features and modules developed on the server will be available either from pip or directly in the zip
                        archive for simple tools.
                    ''')
  localEnv = aresObj.img('first_report_7.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('first_report_8.JPG')
  downloadPicture.doubleDots = 2
  aresObj.table([['Push to the server', 'Environment Available'], [localEnv, downloadPicture]])

  aresObj.title4("Your script will be avaiable !!!")
  localEnv = aresObj.img('first_report_9.JPG')
  localEnv.doubleDots = 2
  aresObj.newline()
  aresObj.newline()


  aresObj.title4("Example of Python to HTML transform")
  localEnv = aresObj.img('html_python.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('html_example.JPG')
  downloadPicture.doubleDots = 2
  aresObj.table([['Python Code', 'HTML result'], [localEnv, downloadPicture]])

  aresObj.newline()
  aresObj.title4("Example of Python to Javascript / Ajax transform")
  localEnv = aresObj.img('javascript_python.JPG')
  localEnv.doubleDots = 2
  downloadPicture = aresObj.img('javascript_example.JPG')
  downloadPicture.doubleDots = 2
  aresObj.table([['Python Code', 'Javascript Result'], [localEnv, downloadPicture]])

  aresObj.paragraph('''
                        More details on the components are available on the below links
                    ''')
  aresComp = aresObj.anchor('HTML Component documentation')
  aresComp.addLink('html', dots='..')
  aresObj.newline()
  aresComp = aresObj.anchor('Graph Component documentation')
  aresComp.addLink('graph', dots='..')

  aresObj.title3("Available Modules")
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/child:dsc/graph")
def report_dsc_graph():
  """ Function to return the Graph object description and a user guide """
  import inspect
  from ares.Lib import AresHtmlGraph

  aresObj = Ares.Report()
  aresObj.reportName = 'dsc/graph'
  aresObj.childPages = {}
  graphObject = [['Class Name', 'Description']]
  aresObj.title("Graph Components")
  aresObj.iframe('http://nvd3.org/livecode/index.html')
  aresObj.title4(AresHtmlGraph.__doc__)
  for name, obj in inspect.getmembers(AresHtmlGraph):
    if inspect.isclass(obj) and name not in ['JsGraph', 'IndentedTree']:
      aresObj.childPages[name] = '../../../child:dsc/graph/%s' % name
      comp = aresObj.anchor(name)
      comp.addLink(name, dots='.')
      graphObject.append([comp, aresObj.code(obj.__doc__)])
  aresObj.table(graphObject)
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/child:dsc/graph/<chartName>")
def report_dsc_graph_details(chartName):
  """ """
  import inspect
  import json
  from ares.Lib import AresHtmlGraph
  from ares.Lib import AresHtml

  aresObj = Ares.Report()
  aresObj.reportName = 'download'
  aresObj.childPages = {}
  aresComponents = {}
  for name, obj in inspect.getmembers(AresHtmlGraph):
    if inspect.isclass(obj):
      aresComponents[name] = obj
  object = aresComponents[chartName]
  aresObj.title(chartName)
  aresObj.title3("%s Components Details" % chartName)
  aresObj.text(object.__doc__)
  mokfilePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, object.mockData)
  with open(mokfilePath) as data_file:
    data = data_file.read()
  graphCom = getattr(aresObj, object.alias)(data)
  graphCom.addClick('alert(e.toSource()) ;')

  # Add the mock data as example
  aresObj.title3('Source Code')
  aresObj.childPages['graph'] = '../../../download/dsc/%s' % object.mockData
  comp = aresObj.anchor('Data Source') #, object.mockData, 'html', {'html': '../../../download/dsc/%s' % object.mockData}, None)
  comp.addLink('graph')
  aresObj.paragraph(['You can download the input data here: ', comp])
  compObj = aresComponents[chartName](0, data)
  aresObj.code("%s\n" % "".join(compObj.jsEvents()['addGraph'])[:-3])
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/html/<objectName>")
def report_html_description(objectName):
  """ Function to return teh html defition of an object """

@report.route("/page/<report_name>")
def page_report(report_name):
  """ Return the html content of the main report """
  reportObj = Ares.Report()
  reportObj.http['FILE'] = report_name
  userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
  reportObj.http['DIRECTORY'] = userDirectory
  reportObj.reportName = report_name
  reportEnv = report_name.replace(".py", "")
  scriptEnv = os.path.join(config.ARES_USERS_LOCATION, reportEnv)

  scripts = {}
  for (path, dirs, files) in os.walk(scriptEnv):
    if path != scriptEnv and not '__init__.py' in files:
      continue

    for pyFile in  files:
      if pyFile == '__pycache__' or pyFile.endswith('pyc') or pyFile.endswith('.zip') or pyFile == 'log_ares.dat':
        continue

      scripts[pyFile] = path.replace(config.ARES_USERS_LOCATION, '')[1:]
  reportObj.http['SCRIPTS'] = scripts
  reportObj.http['SCRIPTS_NAME'] = report_name
  scriptTree, children, ajaxCalls = {}, [], collections.defaultdict(list)
  try:
    sys.path.append(scriptEnv)
    getScriptChildren(scriptEnv, "%s.py" % report_name, scriptTree, ajaxCalls)
    getChildrenFlatStruct(scriptTree, children)
    mod = __import__(reportObj.http['SCRIPTS_NAME'])
    reportObj.http['SCRIPTS_DSC'] = mod.__doc__.strip()
  except Exception as e:
    reportObj.http['SCRIPTS_DSC'] = e

  # Internal callback functions, Users are not expected to use them
  reportObj.http['SCRIPTS_CHILD'] = children
  reportObj.http['SCRIPTS_AJAX'] = ajaxCalls
  reportObj.http['AJAX_CALLBACK'] = {}
  reportObj.http['SCRIPTS_PATH'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  reportObj.childPages = report_index_page.CHILD_PAGES
  onload, content, js = report_index_page.report(reportObj).html()
  if scriptEnv in sys.modules:
    del sys.modules[scriptEnv]
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/")
@report.route("/index")
def index():
  """ Return the main page with the reports selection """
  aresObj = Ares.Report()
  userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  aresObj.http['DIRECTORY'] = userDirectory
  aresObj.http['ROOT_PATH'] = current_app.config['ROOT_PATH']
  aresObj.http['USER_PATH'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  onload, content, js = report_index.report(aresObj).html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/run/<report_name>", methods = ['GET'])
def run_report(report_name):
  """ Run the report """
  onload, js, error = '', '', False
  try:
    userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
    sys.path.append(userDirectory)
    reportObj = Ares.Report()
    for getValues in request.args.items():
      reportObj.http['GET'][getValues[0]] = getValues[1]
    reportObj.reportName = report_name
    mod = __import__(report_name)
    reportObj.childPages = getattr(mod, 'CHILD_PAGES', {})
    reportObj.http['FILE'] = report_name
    reportObj.http['REPORT_NAME'] = report_name
    reportObj.http['DIRECTORY'] = userDirectory
    aresObj = mod.report(reportObj)
    downAll = aresObj.download(cssCls='btn btn-success bdiBar-download')
    downAll.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': report_name, 'script': "%s.py" % report_name})
    downScript = aresObj.downloadAll(cssCls='btn btn-success bdiBar-download-all')
    downScript.js('click', "window.location.href='../download/%s/package'" % report_name)
    onload, content, js = aresObj.html()
  except Exception as e:
    error = True
    content = str(traceback.format_exc()).replace("(most recent call last):", "(most recent call last): <BR /><BR />").replace("File ", "<BR />File ")
    content = content.replace(", line ", "<BR />&nbsp;&nbsp;&nbsp;, line ")
  finally:
    # Try to unload the module
    if report_name in sys.modules:
      del sys.modules[report_name]

  if error:
    return render_template('ares_error.html', onload=onload, content=content, js=js)
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/child:<report_name>/<script>", methods = ['GET'])
def child(report_name, script):
  """ Return the content of the attached pages """
  reportObj = Ares.Report()
  for getValues in request.args.items():
    reportObj.http['GET'][getValues[0]] = getValues[1]

  onload, js, error = '', '', False
  try:
    userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
    sys.path.append(userDirectory)
    mod = __import__(script)
    reportObj.childPages = getattr(mod, 'CHILD_PAGES', {})
    reportObj.http['FILE'] = script
    reportObj.http['REPORT_NAME'] = report_name
    reportObj.http['DIRECTORY'] = userDirectory
    reportObj.reportName = report_name
    aresObj = mod.report(reportObj)
    downAll = aresObj.download(cssCls='btn btn-success bdiBar-download')
    downAll.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': report_name, 'script': "%s.py" % script})
    downScript = aresObj.downloadAll(cssCls='btn btn-success bdiBar-download-all')
    downScript.js('click', "window.location.href='../download/%s/package'" % report_name)
    onload, content, js = aresObj.html()
  except Exception as e:
    content = traceback.format_exc()
    error = True
  finally:
    if script in sys.modules:
      del sys.modules[script]
  if error:
    return render_template('ares_error.html', onload=onload, content=content, js=js)

  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/create/env", methods = ['GET', 'POST'])
def ajaxCreate():
  """ Special Ajax call to set up the environment """
  reportObj = Ares.Report()
  reportObj.http['USER_PATH'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  for postValues in request.form.items():
    reportObj.http['POST'][postValues[0]] = postValues[1]
  return json.dumps(report_index_set.call(reportObj))

@report.route("/ajax/<report_name>/<script>", methods = ['GET', 'POST'])
def ajaxCall(report_name, script):
  """ Generic Ajax call """
  onload, js, error = '', '', False
  userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
  reportObj = Ares.Report()
  reportObj.http['FILE'] = None
  reportObj.http['REPORT_NAME'] = report_name
  reportObj.http['DIRECTORY'] = userDirectory
  reportObj.reportName = report_name
  for getValues in request.args.items():
    reportObj.http['GET'][getValues[0]] = getValues[1]
  for postValues in request.form.items():
    reportObj.http['POST'][postValues[0]] = postValues[1]
  try:
    mod = __import__(report_name)
    result = mod.call(reportObj)
  except Exception as e:
    content = traceback.format_exc()
    error = True
  finally:
    if report_name in sys.modules:
      del sys.modules[report_name]
  if error:
    return render_template('ares_error.html', onload=onload, content=content, js=js)

  return json.dumps(result)

@report.route("/upload/<report_name>", methods = ['POST'])
def uploadFiles(report_name):
  """ Add all the files that a users will drag and drop in the section """
  result = []
  if request.method == 'POST':
    postParams = {}
    for postValues in request.form.items():
      postParams[postValues[0]] = postValues[1]

    for filename, fileType in request.files.items():
      file = request.files[filename]
      if 'DESTINATION' in postParams:
        fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, postParams['DESTINATION'], file.filename)
      else:
        fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, file.filename)
      file.save(fileFullPath)
      appendToLog(report_name, 'UPLOAD', file.filename)

      if not os.path.exists("%s.zip" % fileFullPath):
        with zipfile.ZipFile("%s.zip" % fileFullPath, 'w') as zf:
          zf.write(fileFullPath, "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), file.filename))
      else:
        zf = zipfile.ZipFile("%s.zip" % fileFullPath, 'a')
        zf.write(fileFullPath, "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), file.filename))
        zf.close()
      result.append(filename)
  return json.dumps(result)

@report.route("/delete_file/<report_name>", methods = ['POST'])
def deleteData(report_name):
  """ Delete a file in the report environment """
  if request.method == 'POST':
    postParams = {}
    for postValues in request.form.items():
      postParams[postValues[0]] = postValues[1]
    if 'SOURCE_PATH' in postParams:
      fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, postParams['SOURCE_PATH'], postParams['FILE_NAME'])
    else:
      fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, postParams['FILE_NAME'])
    os.remove(fileFullPath)

  return json.dumps({'FILE_NAME': request.form.get('SOURCE_PATH'), 'ENV': report_name})

@report.route("/delete_folder/<report_name>", methods = ['POST'])
def deleteFolder(report_name):
  """ Delete a file in the report environment """
  import shutil
  if request.method == 'POST':
    postParams = {}
    for postValues in request.form.items():
      postParams[postValues[0]] = postValues[1]
    if 'SOURCE_PATH' in postParams:
      fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, postParams['SOURCE_PATH'], postParams['FILE_NAME'])
    else:
      if 'FILE_NAME' in postParams:
        fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, postParams['FILE_NAME'])
      else:
        fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
    shutil.rmtree(fileFullPath)

  return json.dumps({'FILE_NAME': request.form.get('SOURCE_PATH'), 'ENV': report_name})

@report.route("/delete/<report_name>", methods = ['POST'])
def deleteFiles(report_name):
  """ Delete a file in the report environment """
  import shutil

  if request.form.get('SCRIPT') is not None:
    deletedLocation = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_DELETED_FOLDERS)
    if not os.path.exists(deletedLocation):
      os.makedirs(deletedLocation)
    # Move the file to the deleted Location
    # This folder should be purged every month
    shutil.move(os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, request.form.get('SCRIPT')),
                os.path.join(deletedLocation, "%s_%s" % (report_name, request.form.get('SCRIPT'))))
    appendToLog(report_name, 'DELETE', request.form.get('SCRIPT'))
  return json.dumps({'SCRIPT': request.form.get('SCRIPT'), 'ENV': report_name})

# ---------------------------------------------------------------------------------------------------------
#                                          DOWNLOAD SECTION
#
# The below section will allow
#   - To get the full Ares updated package
#   - To get the full report updated package
#   - To get the last version of a specific script
# ---------------------------------------------------------------------------------------------------------
@report.route("/download/<report_name>/<script>", methods = ['GET', 'POST'])
def downloadFiles(report_name, script):
  """ Download a specific file in a report project """

  if not script.endswith(".py"):
    script = "%s.py" % script

  return send_from_directory(os.path.join(config.ARES_USERS_LOCATION, report_name), script, as_attachment=True)

@report.route("/download/dsc/json/<jsonFile>", methods = ['GET', 'POST'])
def downloadJsonFiles(jsonFile):
  if not jsonFile.endswith(".json"):
    jsonFile = "%s.json" % jsonFile

  mokfilePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'json')
  return send_from_directory(mokfilePath, jsonFile, as_attachment=True)

@report.route("/download/<report_name>/package", methods = ['GET', 'POST'])
def downloadReport(report_name):
  """ Return in a Zip archive the full python package """
  memory_file = io.BytesIO()
  with zipfile.ZipFile(memory_file, 'w') as zf:
    reportPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
    for (path, dirs, files) in os.walk(reportPath):
      for pyFile in  files:
        if pyFile == '__pycache__' or pyFile.endswith('pyc') or pyFile.endswith('.zip') or pyFile == 'log_ares.dat':
          continue

        folder = path.replace("%s" % reportPath, "")
        zf.write(os.path.join(reportPath, path, pyFile), r"%s\%s" % (folder, pyFile))
    # Add all the external libraries
    libPath = os.path.join(current_app.config['ROOT_PATH'], 'Lib')
    for (path, dirs, files) in os.walk(libPath):
      for pyFile in  files:
        if pyFile == '__pycache__' or pyFile.endswith('pyc') or pyFile.endswith('.zip'):
          continue

        folder = path.replace("%s" % libPath, "")
        zf.write(os.path.join(libPath, path, pyFile), r"Lib\%s" % pyFile)

  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='%s.zip' % report_name, as_attachment=True)

@report.route("/download/package")
def download():
  """ Return the package in order to test the scripts """
  memory_file = io.BytesIO()
  with zipfile.ZipFile(memory_file, 'w') as zf:
    for css in LIB_PACKAGE['CSS']:
      zf.write(os.path.join(current_app.config['ROOT_PATH'], "static", "css", css), os.path.join("css", css), zipfile.ZIP_DEFLATED )
    for jsFile in LIB_PACKAGE['JS']:
      zf.write(os.path.join(current_app.config['ROOT_PATH'], "static", "js", jsFile), os.path.join("js", jsFile), zipfile.ZIP_DEFLATED )
    aresModulePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'Lib')
    for pyFile in os.listdir(aresModulePath):
      if '__pycache__' in pyFile or pyFile.endswith('pyc'):
        continue

      if pyFile not in ['AresWrapper.py', 'AresWrapperDeploy.py']:
        zf.write(os.path.join(aresModulePath, pyFile), os.path.join('ares' ,'Lib', pyFile))
      else:
        zf.write(os.path.join(aresModulePath, pyFile), os.path.join(pyFile))
    for jsonFile in LIB_PACKAGE['JSON']:
      zf.write(os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, "json", jsonFile), os.path.join("json", jsonFile), zipfile.ZIP_DEFLATED )
    zf.writestr('html/', '')
    # Add all the external libraries
    libPath = os.path.join(current_app.config['ROOT_PATH'], 'Lib')
    for (path, dirs, files) in os.walk(libPath):
      for pyFile in  files:
        if pyFile == '__pycache__' or pyFile.endswith('pyc') or pyFile.endswith('.zip'):
          continue

        folder = path.replace("%s" % libPath, "")
        zf.write(os.path.join(libPath, path, pyFile), os.path.join("Lib", pyFile))

  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='ares.zip', as_attachment=True)


@report.route("/download/ares", methods = ['GET', 'POST'])
def downloadAres():
  """ Download the up to date Ares package """
  memory_file = io.BytesIO()
  aresModulePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'Lib')
  with zipfile.ZipFile(memory_file, 'w') as zf:
    for pyFile in os.listdir(aresModulePath):
      if '__pycache__' in pyFile or pyFile.endswith('pyc'):
        continue

      if pyFile not in ['AresWrapper.py', 'AresWrapperDeploy.py']:
        zf.write(os.path.join(aresModulePath, pyFile), os.path.join('ares', 'Lib', pyFile))
      else:
        zf.write(os.path.join(aresModulePath, pyFile), os.path.join(pyFile))

    # Add all the external libraries
    libPath = os.path.join(current_app.config['ROOT_PATH'], 'Lib')
    for (path, dirs, files) in os.walk(libPath):
      for pyFile in  files:
        if pyFile == '__pycache__' or pyFile.endswith('pyc') or pyFile.endswith('.zip'):
          continue

        folder = path.replace("%s" % libPath, "")
        zf.write(os.path.join(libPath, path, pyFile), os.path.join("Lib", pyFile))
  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='ares.zip', as_attachment=True)

@report.route("/ares/version", methods = ['GET', 'POST'])
def getAresFilesVersions():
  """ Return the files, the version and the size """
  aresModulePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'Lib')
  files = {}
  for pyFile in os.listdir(aresModulePath):
    if '__pycache__' in pyFile or pyFile.endswith('pyc'):
      continue

    stat = os.stat(os.path.join(aresModulePath, pyFile))
    files[pyFile] = [stat.st_mtime, stat.st_size]
  # Add all the external libraries
  libPath = os.path.join(current_app.config['ROOT_PATH'], 'Lib')
  for (path, dirs, f) in os.walk(libPath):
    for pyFile in  f:
      if pyFile == '__pycache__' or pyFile.endswith('pyc') or pyFile.endswith('.zip'):
        continue

      stat = os.stat(os.path.join(libPath, pyFile))
      files[pyFile] = [stat.st_mtime, stat.st_size]
  return json.dumps(files)

# ---------------------------------------------------------------------------------------------------------
#                             CREATE FILES AND FOLDERS IN AN ARES ENV
#
# The below section will allow
#   - To get the full Ares updated package
#   - To get the full report updated package
#   - To get the last version of a specific script
# ---------------------------------------------------------------------------------------------------------

@report.route("/folder/create", methods = ['POST'])
def create_folder():
  """ This REST service will create a file in a given env """
  reportObj = Ares.Report()
  for postValues in request.form.items():
    reportObj.http['POST'][postValues[0]] = postValues[1]
  reportObj.http['DIRECTORY'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, reportObj.http['POST']['REPORT_NAME'])
  subfolders = reportObj.http['POST']['FOLDERS'].split("/")
  subDirectories = os.path.join(reportObj.http['DIRECTORY'], *subfolders)
  if not os.path.exists(subDirectories):
    os.makedirs(subDirectories)
    appendToLog(reportObj.http['POST']['REPORT_NAME'], 'FOLDER_CREATION', reportObj.http['POST']['FOLDERS'])
  return json.dumps('Folders created in the env %s' % reportObj.http['POST']['REPORT_NAME'])

