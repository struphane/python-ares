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
import shutil

from flask import current_app, Blueprint, render_template, request, send_from_directory, send_file, make_response, render_template_string
from click import echo

import config

# TODO add a check on the variable DIRECTORY to ensure that it cannot be changed
# TODO add the Flask url_for for an even using a text file like the attempt in JsTable
# TODO remove the use of chidren pages. Everything should use run

# Ares Framework
from ares.Lib import Ares
from ares.Lib import AresLog

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


def appendToLog(reportName, event, comment):
  """ Append an event to the dedicated log file """
  logFile = open(os.path.join(config.ARES_USERS_LOCATION, reportName, 'log_ares.dat'), 'a')
  showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")
  logFile.write("%s#%s#%s#%s\n" % (event, showtime[0], showtime[1], comment))
  logFile.close()

def getHttpParams(request):
  """
  Get the HTTP parameters of a request

  All the results will be done in upper case, just to make sure that users will be used to define
  those variable in uppercases
  """
  httpParams = {}
  for postValues in request.args.items():
    #TODO Find a way to not have this stupid hack
    httpParams[postValues[0].replace("amp;", "").upper()] = postValues[1]
  for postValues in request.form.items():
    httpParams[postValues[0].upper()] = postValues[1]
  httpParams['DIRECTORY'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  # Special environment configuration
  httpParams['CONFIG'] = {}
  httpParams['CONFIG']['WRK'] = config.WORK_PATH
  return httpParams

def getFileName(script, exts):
  """ Return the filename with the expected extension

  This is just to ensure that users will not make eny mistake in the filenames
  This function will check for an extension and it will add the expected one otherwise.

  If the extension is not expected, it will return None
  """
  scriptName, file_extension = os.path.splitext(script)
  if file_extension.upper() in exts:
    return script

  if file_extension == '':
    return "%s%s" % (scriptName, exts[0])

  return None

def noCache(f):
  def respFunc(*args, **kwargs):
    resp = make_response(f(*args, **kwargs))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    return resp
  return respFunc

#TO BE REMOVED
@report.route("/doc/html")
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
    aresObj.table('Available HTML Components',  htmlObject)
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

#TO BE REMOVED
@report.route("/doc/graph")
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
    if inspect.isclass(obj) and name not in ['JsGraph', 'IndentedTree', 'NVD3Chart']:
      aresObj.childPages[name] = '../../../child:dsc/graph/%s' % name
      comp = aresObj.anchor(name)
      comp.addLink(name, dots='.')
      graphObject.append([comp, aresObj.code(obj.__doc__)])
  aresObj.table('Available Graph', graphObject)
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

#TO BE REMOVED
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
  graphCom = getattr(aresObj, object.alias)('Graph Example', data)
  graphCom.addClick('alert(e.toSource()) ;')

  # Add the mock data as example
  aresObj.title3('Source Code')
  aresObj.childPages['graph'] = '../../../download/dsc/%s' % object.mockData
  comp = aresObj.anchor('Data Source') #, object.mockData, 'html', {'html': '../../../download/dsc/%s' % object.mockData}, None)
  comp.addLink('graph')
  aresObj.paragraph(['You can download the input data here: ', comp])
  compObj = aresComponents[chartName](0, 'Graph Example', data)
  aresObj.code("%s\n" % "".join(compObj.jsEvents()['addGraph'])[:-3])
  onload, content, js = aresObj.html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

# ------------------------------------------------------------------------------------------------------------
# Section dedicated to run the reports on the servers
#
# All the reports will use one of the two common entry points as below
#     - run_report, for the main reports. The ones which can be run directly
#     - ajaxCall, for the services used by reports to refresh data
#
# No other entries is posslble and the structure of the local environment should be as defined in the wiki
# Please make sure that this script is never shared and also that no user env start with a _
# _ is dedicated to internal environments (for BDI only)
# ------------------------------------------------------------------------------------------------------------
@report.route("/", defaults={'report_name': '_AresReports', 'script_name': '_AresReports'})
@report.route("/index", defaults={'report_name': '_AresReports', 'script_name': '_AresReports'})
@report.route("/run/<report_name>", defaults={'script_name': None}, methods = ['GET', 'POST'])
@report.route("/run/<report_name>/<script_name>", methods = ['GET', 'POST'])
def run_report(report_name, script_name):
  """
  Run the report

  """
  onload, js, error, side_bar, envName = '', '', False, [], ''
  cssImport, jsImport = '', ''
  try:
    if script_name is None:
      script_name = report_name
    # add the folder directory to the python path in order to run the script
    # The underscore folders are internal onces and we do not need to include them to the classpath
    if not report_name.startswith("_"):
      side_bar = [render_template_string('<li><a href="{{ url_for(\'ares.run_report\', report_name=\'_AresReports\', script_name=\'AresIndexPage\', user_script=\'%s\') }}" target="_blank" style="color:white;text-decoration: none">Env <span class="badge-pill badge-danger">New</span></a></li>' % report_name)]
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
      if not userDirectory in sys.path:
        sys.path.append(userDirectory)
      ajaxPath = os.path.join(userDirectory, 'ajax')
      if os.path.exists(ajaxPath) and not ajaxPath in sys.path:
        sys.path.append(ajaxPath)
    else:
      side_bar = []
      systemDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'reports', report_name)
      if not systemDirectory in sys.path:
        sys.path.append(systemDirectory)
      ajaxPath = os.path.join(systemDirectory, 'ajax')
      if os.path.exists(ajaxPath) and not ajaxPath in sys.path:
        sys.path.append(ajaxPath)

      # In this context we need the generic user directory as we are in a system report
      # Users should not be allowed to create env starting with _
      #TODO put in place a control
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)

    reportObj = Ares.Report()
    reportObj.http = getHttpParams(request)
    reportObj.reportName = report_name
    if script_name in sys.modules:
      del sys.modules[script_name]
    mod = __import__(script_name) # run the report
    # Set some environments variables which can be used in the report
    reportObj.http['FILE'] = script_name
    reportObj.http['REPORT_NAME'] = report_name
    reportObj.http['DIRECTORY'] = userDirectory
    mod.report(reportObj)
    typeDownload = getattr(mod, 'DOWNLOAD', 'BOTH')
    if typeDownload in ['BOTH', 'SCRIPT']:
      side_bar.append(render_template_string('<li><a href="{{ url_for(\'ares.downloadFiles\', report_name=\'%s\', script=\'%s.py\') }}" >Python script</a></li>' % (report_name, script_name)))
    if typeDownload == 'BOTH':
      side_bar.append(render_template_string('<li><a href="{{ url_for(\'ares.downloadReport\', report_name=\'%s\') }}" >environment</a></li>' % report_name))
    report = __import__(report_name) # run the report
    envName = getattr(report, 'NAME', '')
    side_bar.append('<h5 style="color:white"><b>&nbsp;<i class="fa fa-area-chart" aria-hidden="true"></i>&nbsp;Dashboard</b></h5>')
    for categories, links in getattr(report, 'SHORTCUTS', []):
      side_bar.append('<h6 style="color:white"><b>&nbsp;&nbsp;&nbsp;<i class="fa fa-check-square-o" aria-hidden="true"></i>&nbsp;%s</b></h6>' % categories)
      for name, scriptName in links:
        side_bar.append(render_template_string('<li><a href="{{ url_for(\'ares.run_report\', report_name=\'%s\', script_name=\'%s\') }}">%s</a></li>' % (report_name, scriptName.replace(".py", ""), name)))
    cssImport, jsImport, onload, content, js = reportObj.html()
  except Exception as e:
    error = True
    content = str(traceback.format_exc()).replace("(most recent call last):", "(most recent call last): <BR /><BR />").replace("File ", "<BR />File ")
    content = content.replace(", line ", "<BR />&nbsp;&nbsp;&nbsp;, line ")
  finally:
    # Try to unload the module
    if not report_name.startswith("_"):
      sys.path.remove(userDirectory)
      if os.path.exists(os.path.join(userDirectory, 'ajax')):
        sys.path.remove(os.path.join(userDirectory, 'ajax'))

      for module, ss in sys.modules.items():
        if userDirectory in str(ss):
          del sys.modules[module]
    for f in reportObj.fileManager.values():
      if not f.closed:
        f.close()

  if error:
    return render_template('ares_error.html', cssImport=cssImport, jsImport=jsImport, onload=onload, content=content, js=js, side_bar=side_bar)

  return render_template('ares_template_basic.html', cssImport=cssImport, jsImport=jsImport, onload=onload, content=content, js=js, side_bar="\n".join(side_bar), name=envName)

@report.route("/ajax/<report_name>/<script>", methods = ['GET', 'POST'])
def ajaxCall(report_name, script):
  """ Generic Ajax call """
  onload, js, error = '', '', False
  try:
    reportObj = Ares.Report()
    reportObj.http = getHttpParams(request)
    if report_name.startswith("_"):
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'reports', report_name)
      sys.path.append(userDirectory)
      # TODO Improve the __import__ to not have to append the ajax path to the sys.path
      sys.path.append(os.path.join(userDirectory, 'ajax'))
      # , reportObj.http['USER_SCRIPT']
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
    else:
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
      sys.path.append(userDirectory)
      sys.path.append(os.path.join(userDirectory, 'ajax'))
    reportObj.http['FILE'] = None
    reportObj.http['REPORT_NAME'] = report_name
    reportObj.http['DIRECTORY'] = userDirectory
    reportObj.reportName = report_name
    mod = __import__(script.replace(".py", ""))
    result = {'status': 'Success', "data": mod.call(reportObj)}
  except Exception as e:
    content = traceback.format_exc()
    error = True
  finally:
    if script in sys.modules:
      del sys.modules[script]
    for f in reportObj.fileManager.values():
      if not f.closed:
        f.close()

  if error:
    return json.dumps({'status': 'Error', "data": [], 'message': str(content)})

  return json.dumps(result)

@report.route("/handlerequest/<module_name>/<function>", methods = ['GET', 'POST'])
def handleRequest(module_name, function):
  onload, js, error = '', '', False
  try:
    mod = __import__(module_name)
    results = {"status": "success", "data": getattr(mod, function)(getHttpParams(request))}
  except Exception as e:
    results = {"status": "Error", "message": str(e), "data": []}
  return json.dumps(results)

# ------------------------------------------------------------------------------------------------------------
# Section dedicated to upload files to a shared environment on the server
#
# Users will not have a write access on the server so it will have to use the scripts dedicated to deploy
# their environment to the correct location. Users will have to get the same structure of folders locally
# This constraint will ensure that there will be no surprise when they will try to push the scripts to production
# Basically the structure of a report should be as below
# /ReportName/
#    ReportName.py
#    /ajax/
#       xxx.py
#    /output/
#    /json/
#    /js/
#    /statics/
# For more information please look at the documentation of the local runs
# ------------------------------------------------------------------------------------------------------------
@report.route("/create/env", methods = ['POST', 'GET'])
def ajaxCreate():
  """ Special Ajax call to set up the environment

  This service will create the environment and also add an emtpy report.
  The log file will be produce and the zip archive with the history will be defined
  """

  reportObj = Ares.Report()
  reportObj.http = getHttpParams(request)
  reportObj.http['DIRECTORY'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  reportObj.http['ARES_TMPL'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'tmpl')
  scriptName = "%s.py" % reportObj.http['REPORT_NAME']
  scriptPath = os.path.join(reportObj.http['DIRECTORY'], reportObj.http['REPORT_NAME'])
  if scriptName.startswith("_"):
    return json.dumps("Environment Name cannot start with _"), 500

  log = AresLog.AresLog(current_app.config['ROOT_PATH'], reportObj.http['REPORT_NAME'], config)
  if not os.path.exists(scriptPath):
    os.makedirs(scriptPath)
    log.createFolder()
    shutil.copyfile(os.path.join(reportObj.http['ARES_TMPL'], 'tmpl_report.py'), os.path.join(scriptPath, scriptName))
    log.addScript('Report', scriptName)
    fileFullPath = os.path.join(scriptPath, scriptName)
    with zipfile.ZipFile("%s.zip" % fileFullPath, 'w') as zf:
      zf.write(fileFullPath, "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), scriptName))

    os.makedirs(os.path.join(scriptPath, 'outputs'))
    return json.dumps("New environment created: %s" % scriptName), 200

  return json.dumps("Existing Environment"), 200

@report.route("/upload/<report_type>/<report_name>", methods = ['POST'])
def uploadFiles(report_type, report_name):
  """ Add all the files that a users will drag and drop in the section """
  result = []
  reportTypes = {'report': (['.PY'], None), 'configuration': (['.JSON'], 'config'),
                 'ajax': (['.PY'], 'ajax'), 'javascript': (['.JS'], 'js'),
                 'views': (['.TXT', '.CSV'], 'statics'), 'outputs': (None, 'outputs'),
                 }
  if not report_type in reportTypes:
    return json.dumps('Error %s category not recognized !' % report_type), 500

  if report_name.startswith("_"):
    return json.dumps("Environment Name cannot start with _"), 500

  if request.method == 'POST':
    ext, path = reportTypes[report_type]
    postParams = getHttpParams(request)
    for filename, fileType in request.files.items():
      file = request.files[filename]
      if report_type != 'outputs':
        # No checks for the outputs folder
        # User can deploy whatever they want in this folder
        fileWithoutExt = getFileName(file.filename, ext)
        if fileWithoutExt is None:
          return json.dumps('File extension %s not recognized for this category %s  !' % (ext, report_type)), 500

      if 'DESTINATION' in postParams:
        fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, postParams['DESTINATION'], file.filename)
      else:
        if path is None:
          fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, file.filename)
        else:
          filePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, path)
          if not os.path.exists(filePath):
            os.makedirs(filePath)
          fileFullPath = os.path.join(filePath, file.filename)
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
    requestParams = getHttpParams(request)
    if 'SOURCE_PATH' in requestParams:
      fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, requestParams['SOURCE_PATH'], requestParams['FILE_NAME'])
    else:
      fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, requestParams['FILE_NAME'])
    os.remove(fileFullPath)
  return json.dumps({'FILE_NAME': request.form.get('SOURCE_PATH'), 'ENV': report_name})

@report.route("/delete_folder/<report_name>", methods = ['POST'])
def deleteFolder(report_name):
  """ Delete a file in the report environment """
  import shutil
  if request.method == 'POST':
    requestParams = getHttpParams(request)
    if 'SOURCE_PATH' in requestParams:
      shutil.rmtree(os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, requestParams['SOURCE_PATH']))
    else:
      shutil.rmtree(os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name))
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

#TO BE REMOVED
@report.route("/json/<report_name>", methods=['POST'])
def configFile(report_name):
  """
  Write a Json configuration file
  """
  if request.method == 'POST':
    requestParams = getHttpParams(request)
    userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, "config", requestParams['source'])
    if not os.path.exists(userDirectory):
      os.makedirs(userDirectory)
    # 
    commentFile = open(os.path.join(userDirectory, "%s.cfg" % requestParams['key']), "w")
    commentFile.write(requestParams['val'])
    commentFile.close()
  return json.dumps('')

@report.route("/components/<component>:<compId>")
def designerComponent(component, compId):
  """

  """
  echo(compId)
  echo(component)
  echo(Ares.moduleFromAlias(component))
  echo(Ares.moduleFromAlias(component).aresDesigner(compId))
  return json.dumps('')

# ---------------------------------------------------------------------------------------------------------
#                                          DOWNLOAD SECTION
#
# The below section will allow
#   - To get the full Ares updated package
#   - To get the full report updated package
#   - To get the last version of a specific script
# ---------------------------------------------------------------------------------------------------------
@noCache
@report.route("/download/<report_name>/<script>", methods = ['GET', 'POST'])
def downloadFiles(report_name, script):
  """ Download a specific file in a report project """
  #TODO add a check on the class variable DOWNLOAD to check if the module is downloadable (by default it is the case)
  requestParams = getHttpParams(request)
  if '.' not in script:
    # We assume it is a python script
    script = "%s.py" % script
  if report_name.startswith("_"):
    pathDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'reports')
  else:
    pathDirectory = config.ARES_USERS_LOCATION
  if '&' in script:
    splitScriptPath = script.strip("\\").split("&")
    userDirectory = os.path.join(pathDirectory, report_name, *splitScriptPath[:-1])
  else:
    splitScriptPath = [script]
    userDirectory = os.path.join(pathDirectory, report_name)
  return send_from_directory(userDirectory, splitScriptPath[-1], as_attachment=True)

#TO BE REMOVED
@noCache
@report.route("/download/dsc/json/<jsonFile>", methods = ['GET', 'POST'])
def downloadJsonFiles(jsonFile):
  if not jsonFile.endswith(".json"):
    jsonFile = "%s.json" % jsonFile

  mokfilePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'json')
  return send_from_directory(mokfilePath, jsonFile, as_attachment=True)

@noCache
@report.route("/download/<report_name>/package", methods = ['GET', 'POST'])
def downloadReport(report_name):
  """ Return in a Zip archive the full python package """
  memory_file = io.BytesIO()
  with zipfile.ZipFile(memory_file, 'w') as zf:
    reportPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
    for (path, dirs, files) in os.walk(reportPath):
      for pyFile in  files:
        if Ares.isExcluded(current_app.config['ROOT_PATH'], file=pyFile):
          continue

        folder = path.replace("%s" % reportPath, "")
        zf.write(os.path.join(reportPath, path, pyFile), r"%s\%s" % (folder, pyFile))
    # Add all the external libraries
    libPath = os.path.join(current_app.config['ROOT_PATH'], 'Lib')
    for (path, dirs, files) in os.walk(libPath):
      for pyFile in  files:
        if Ares.isExcluded(current_app.config['ROOT_PATH'], file=pyFile):
          continue

        folder = path.replace("%s" % libPath, "")
        zf.write(os.path.join(libPath, path, pyFile), r"Lib\%s" % pyFile)

  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='%s.zip' % report_name, as_attachment=True)

@noCache
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
      if Ares.isExcluded(current_app.config['ROOT_PATH'], file=pyFile):
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
        if Ares.isExcluded(current_app.config['ROOT_PATH'], file=pyFile):
          continue

        zipArchPath = path.replace(libPath, "").lstrip("\\")
        if zipArchPath == "":
          zf.write(os.path.join(libPath, path, pyFile), os.path.join("Lib", pyFile))
        else:
          zf.write(os.path.join(libPath, path, pyFile), os.path.join("Lib", zipArchPath, pyFile))
  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='ares.zip', as_attachment=True)

@noCache
@report.route("/download/ares", methods = ['GET', 'POST'])
def downloadAres():
  """ Download the up to date Ares package """
  memory_file = io.BytesIO()
  aresModulePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'Lib')
  with zipfile.ZipFile(memory_file, 'w') as zf:
    for paths in ['Lib', 'tmpl', os.path.join('Lib', 'graph'), os.path.join('Lib', 'html'), os.path.join('Lib', 'tools')]:
      aresModulePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, paths)
      for pyFile in os.listdir(aresModulePath):
        if Ares.isExcluded(current_app.config['ROOT_PATH'], file=pyFile):
          continue

        if pyFile == 'AresInstall.py':
          # Install cannot be copied and it is available in the SVN repository directly
          continue

        if pyFile not in ['AresDeploy.py', 'AresLocalRuns.py']:
          zf.write(os.path.join(aresModulePath, pyFile), os.path.join('ares', paths, pyFile))
        else:
          zf.write(os.path.join(aresModulePath, pyFile), os.path.join(pyFile))

    # Add all the external libraries
    libPath = os.path.join(current_app.config['ROOT_PATH'], 'Lib')
    for (path, dirs, files) in os.walk(libPath):
      for pyFile in  files:
        if pyFile == 'flask_dummy.py':
          zf.write(os.path.join(libPath, path, pyFile), os.path.join('flask.py'))
          continue

        if Ares.isExcluded(path, file=pyFile):
          continue

        zipArchPath = path.replace(libPath, "").lstrip("\\")
        if zipArchPath == "":
          zf.write(os.path.join(libPath, path, pyFile), os.path.join("Lib", pyFile))
        else:
          zf.write(os.path.join(libPath, path, pyFile), os.path.join("Lib", zipArchPath, pyFile))
  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='ares.zip', as_attachment=True)

@report.route("/ares/version", methods = ['GET', 'POST'])
def getAresFilesVersions():
  """ Return the files, the version and the size """
  aresModulePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'Lib')
  files = {}
  for pyFile in os.listdir(aresModulePath):
    if Ares.isExcluded(current_app.config['ROOT_PATH'], file=pyFile):
      continue

    stat = os.stat(os.path.join(aresModulePath, pyFile))
    files[pyFile] = [stat.st_mtime, stat.st_size]
  # Add all the external libraries
  libPath = os.path.join(current_app.config['ROOT_PATH'], 'Lib')
  for (path, dirs, f) in os.walk(libPath):
    for pyFile in  f:
      if Ares.isExcluded(current_app.config['ROOT_PATH'], file=pyFile):
        continue

      stat = os.stat(os.path.join(libPath, pyFile))
      files[pyFile] = [stat.st_mtime, stat.st_size]
  return json.dumps(files)
