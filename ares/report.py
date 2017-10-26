""" Special app for the report section

"""

import json
import os
import sys
import zipfile
import io
import traceback
import time
import shutil
import sqlite3
import datetime
import hashlib

from flask import current_app, Blueprint, render_template, request, send_from_directory, send_file, make_response, render_template_string
from click import echo

import config

# TODO add a check on the variable DIRECTORY to ensure that it cannot be changed
# TODO add the Flask url_for for an even using a text file like the attempt in JsTable
# TODO remove the use of chidren pages. Everything should use run

# Ares Framework
from Libs import AresChartsService
from ares import packages
from ares.Lib import Ares
from ares.Lib import AresImports
from ares.Lib import AresExceptions

try:
  from Libs import AresUserAuthorization
except:
  pass

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
  httpParams['CONFIG']['COMPANY'] = config.COMPANY
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


def executeScriptQuery(dbPath, query, params=None):
  """ simple function to execute queries"""

  conn = sqlite3.connect(dbPath)
  c = conn.cursor()
  if params:
    query = query % params
  c.executescript(query)
  conn.commit()
  conn.close()

def executeSelectQuery(dbPath, query, params=None):
  """ simple select wrapper """

  conn = sqlite3.connect(dbPath)
  c = conn.cursor()
  if params:
    query = query % params
  c.execute(query)
  res = c.fetchall()
  conn.close()
  return res

def checkAuth(dbpath, report_name, user_id):
  """ Check whether user has authorization to see data within the environment """
  #TODO add login information to have proper security with Salt
  # cipherId = AresSecurity.encrypt()
  if not os.path.exists(dbpath):
    raise IOError("Path to DB does not exist - the SQLite Database may have been deleted")

  query = """SELECT 1 FROM env_auth 
               INNER JOIN env_def ON env_auth.env_id = env_def.env_id and env_def.env_name = '%(report_name)s'
               INNER JOIN user_accnt ON env_auth.uid = user_accnt.uid and user_accnt.email_addr = '%(user_id)s'"""
  res = executeSelectQuery(dbpath, query, params={'report_name': report_name, 'user_id': user_id})
  if not res:
    return False

  else:
    return True


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

@report.route("/", defaults={'report_name': '_AresReports', 'script_name': '_AresReports', 'user_id': None})
@report.route("/index", defaults={'report_name': '_AresReports', 'script_name': '_AresReports', 'user_id': None})
@report.route("/run/<report_name>", defaults={'script_name': None, 'user_id': None}, methods = ['GET', 'POST'])
@report.route("/run/<report_name>/<script_name>", defaults={'user_id': None}, methods = ['GET', 'POST'])
@report.route("/run/<report_name>/<script_name>/<user_id>", methods = ['GET', 'POST'])
def run_report(report_name, script_name, user_id):
  """
  Run the report

  """
  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  onload, jsCharts, error, side_bar, envName, jsGlobal = '', '', False, [], '', ''
  viewScript, downloadEnv = False, False
  cssImport, jsImport = '', ''
  isAuth = True
  try:
    if script_name is None:
      script_name = report_name
    # add the folder directory to the python path in order to run the script
    # The underscore folders are internal onces and we do not need to include them to the classpath
    if not report_name.startswith("_"):
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
      if  script_name != report_name and config.upper() != 'LOCAL':
        dbPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db')
        if not checkAuth(dbPath, report_name, user_id):
          raise AresExceptions.AuthException('Not authorized to visualize this data')

        queryParams = {'script_name': script_name, 'env_name': report_name, 'usr_id': user_id}
        executeScriptQuery(dbPath, open(os.path.join(SQL_CONFIG, 'log_request.sql')).read(), params=queryParams)
      side_bar = [render_template_string('<li><a href="{{ url_for(\'ares.run_report\', report_name=\'_AresReports\', script_name=\'AresIndexPage\', user_script=\'%s\') }}" target="_blank" style="color:white;text-decoration: none">Env <span class="badge-pill badge-danger">New</span></a></li>' % report_name)]
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
    #if typeDownload in ['BOTH', 'SCRIPT']:
    #  side_bar.append('<h5 style="color:white">&nbsp;<b><i class="fa fa-download" aria-hidden="true">&nbsp;</i>Download</b></h5>')
    #  side_bar.append(render_template_string('<li><a href="{{ url_for(\'ares.downloadFiles\', report_name=\'%s\', script=\'%s.py\') }}" >Python script</a></li>' % (report_name, script_name)))
    if typeDownload == 'BOTH':
      downloadEnv = report_name
    report = __import__(report_name) # run the report
    envName = getattr(report, 'NAME', '')
    side_bar.append('<h5 style="color:white"><b>&nbsp;<i class="fa fa-area-chart" aria-hidden="true"></i>&nbsp;Dashboard</b></h5>')
    for categories, links in getattr(report, 'SHORTCUTS', []):
      side_bar.append('<h6 style="color:white"><b>&nbsp;&nbsp;&nbsp;&nbsp;%s</b></h6>' % categories)
      for name, scriptName in links:
        side_bar.append(render_template_string('<li><a href="{{ url_for(\'ares.run_report\', report_name=\'%s\', script_name=\'%s\') }}">%s</a></li>' % (report_name, scriptName.replace(".py", ""), name)))
    cssImport, jsImport, onload, content, jsCharts, jsGlobal = reportObj.html()
    # Database caches will be stored in the reportObj.dbCaches
    # Nothing related to the DB should be done in ares.py in order to allow users to run everything locally
  except AresExceptions.AuthException as e:
    isAuth = False
    content = str(traceback.format_exc()).replace("(most recent call last):", "(most recent call last): <BR /><BR />").replace("File ", "<BR />File ")
    content = content.replace(", line ", "<BR />&nbsp;&nbsp;&nbsp;, line ")

  except Exception as e:
    error = True
    content = str(traceback.format_exc()).replace("(most recent call last):", "(most recent call last): <BR /><BR />").replace("File ", "<BR />File ")
    content = content.replace(", line ", "<BR />&nbsp;&nbsp;&nbsp;, line ")
  finally:
    # Try to unload the module
    htmlArchives = []
    savedHtmlLocation = os.path.join(userDirectory, 'saved')
    if os.path.exists(savedHtmlLocation):
      for htmlPage in os.listdir(savedHtmlLocation):
        htmlArchives.append(render_template_string("<a class='dropdown-item' href='{{ url_for('ares.savedHtmlReport', report_name='%s', html_report='%s') }}'>%s</a>" % (report_name, htmlPage, "".join(htmlPage.split(".")[:-1]))))
    if isAuth:
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

  if not isAuth:
    return render_template('ares_error.html', content=content)

  if error:
    return render_template('ares_error.html', cssImport=cssImport, jsImport=jsImport, jsOnload=onload, content=content, jsGraphs=jsCharts, side_bar=side_bar, jsGlobal=jsGlobal)

  return render_template('ares_template_basic.html', cssImport=cssImport, jsImport=jsImport,
                         jsOnload=onload, content=content, jsGraphs=jsCharts, side_bar="\n".join(side_bar),
                         name=envName, jsGlobal=jsGlobal, htmlArchives="\n".join(htmlArchives),
                         viewScript=viewScript, downloadEnv=downloadEnv)

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

@report.route("/pivotData/<format>", methods = ['POST'])
def pivotData(format):
  """ Dedicated service to translate the data """
  httpParams = request.get_json()
  if format.upper() in ['PIE', 'DONUT', 'LINE']:
    return json.dumps(AresChartsService.toPie(httpParams['RECORDSET'], httpParams['KEY'], httpParams['VAL']))

  if format.upper() in ['BAR']:
    return json.dumps(AresChartsService.toPie(httpParams['RECORDSET'], httpParams['SERIESNAME'], httpParams['KEY'], httpParams['VAL']))

  if format.upper() in ['HORIZBAR', 'MULTIBAR', 'SCATTER', 'STACKEDAREA']:
    return json.dumps(AresChartsService.toMultiSeries(httpParams['RECORDSET'],
                                                      httpParams['KEY'],
                                                      httpParams['X'],
                                                      httpParams['VAL'],
                                                      #httpParams['SERIESNAME'],
                                                      ))

  return json.dumps('Format %s not recognised' % format)

@report.route("/admin/<report_name>/<token>", defaults={'token': None}, methods=['GET'])
def adminEnv(report_name, token):
  """ Admin session for the environment """
  #
  #
  #if not checkAuth(dbPath, report_name, user_id):
  #  raise AresExceptions.AuthException('Not authorized to visualize this data')
  script_name = '_AresAdmin' # run the report
  dbPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db')
  onload, jsCharts, error, side_bar, envName, jsGlobal = '', '', False, [], '', ''
  cssImport, jsImport = '', ''
  systemDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'reports', script_name)
  if not systemDirectory in sys.path:
    sys.path.append(systemDirectory)
  ajaxPath = os.path.join(systemDirectory, 'ajax')
  if os.path.exists(ajaxPath) and not ajaxPath in sys.path:
    sys.path.append(ajaxPath)

  reportObj = Ares.Report()
  reportObj.http = getHttpParams(request)
  reportObj.reportName = report_name
  mod = __import__(script_name) # run the report
  envName = getattr(mod, 'NAME', '')
  # Set some environments variables which can be used in the report
  reportObj.http['FILE'] = script_name
  reportObj.http['REPORT_NAME'] = report_name
  reportObj.http['DIRECTORY'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
  mod.report(reportObj)
  cssImport, jsImport, onload, content, jsCharts, jsGlobal = reportObj.html()
  return render_template('ares_template_basic.html', cssImport=cssImport, jsImport=jsImport,
                         jsOnload=onload, content=content, jsGraphs=jsCharts, side_bar="\n".join(side_bar),
                         name=envName, jsGlobal=jsGlobal, htmlArchives="\n".join([]))

@report.route("/saved/<report_name>/<html_report>", methods = ['GET'])
def savedHtmlReport(report_name, html_report):
  """  """
  reportPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'saved', html_report)
  html_report = []
  if os.path.exists(reportPath):
    htmlReport = open(reportPath)
    contentReport = False
    for line in htmlReport:
      if contentReport:
        html_report.append(line)
        continue

      if line.upper().startswith('<BODY'):
        contentReport = True
        html_report.append(line)
  importManager = AresImports.ImportManager()
  cssPath = os.path.join(current_app.config['ROOT_PATH'], 'static', 'user', report_name, 'css')
  cssImports = [importManager.cssGetAll()]
  if os.path.exists(cssPath):
    for cssFile in os.listdir(cssPath):
      cssImports.append(render_template_string('<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'user/%s/css/%s\') }}">' % (report_name, cssFile)))

  jsPath = os.path.join(current_app.config['ROOT_PATH'], 'static', 'user', report_name, 'js')
  jsImports = [importManager.jsGetAll()]
  if os.path.exists(jsPath):
    for jsFile in os.listdir(jsPath):
      if jsFile.endswith('.js'):
        jsImports.append(render_template_string('<script language="javascript" type="text/javascript" src="{{ url_for(\'static\', filename=\'user/%s/css/%s\') }}"></script>' % (report_name, jsFile)))

  return render_template('ares_empty.html', cssImports="\n".join(cssImports), jsImports="\n".join(jsImports), html_report="".join(html_report))




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

@report.route("/create/env/<email_address>", methods = ['POST'])
def ajaxCreate(email_address):
  """ Special Ajax call to set up the environment

  This service will create the environment and also add an emtpy report.
  The log file will be produce and the zip archive with the history will be defined
  """
  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  reportObj = Ares.Report()
  reportObj.http = getHttpParams(request)
  reportObj.http['DIRECTORY'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  reportObj.http['ARES_TMPL'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'tmpl')
  scriptName = "%s.py" % reportObj.http['REPORT_NAME']
  scriptPath = os.path.join(reportObj.http['DIRECTORY'], reportObj.http['REPORT_NAME'])
  if scriptName.startswith("_"):
    return json.dumps("Environment Name cannot start with _"), 500

  if not os.path.exists(scriptPath):
    os.makedirs(scriptPath)
    # envKey = os.urandom(24).encode('hex')
    # Create a dedicated database in the user environment
    # This will be there in order to ensure the data access but also it will allow us to check the admin and log tables
    dbPath = os.path.join(scriptPath, 'db')
    h = hashlib.new('md5')
    h.update(bytes(email_address.encode('utf-8')))
    hash_id = h.hexdigest()
    os.makedirs(dbPath)
    executeScriptQuery(os.path.join(dbPath, 'admin.db'), open(os.path.join(SQL_CONFIG, 'create_sqlite_schema.sql')).read())
    #fisrt user insert to appoint an admin on the environment

    queryParams = {'usr_id': email_address, 'hash_id': hash_id, 'env_name': reportObj.http['REPORT_NAME']}
    firtsUsrRights = open(os.path.join(SQL_CONFIG, 'create_env.sql')).read()
    executeScriptQuery(os.path.join(dbPath, 'admin.db'), firtsUsrRights, params=queryParams)
    queryParams = {'report_name': reportObj.http['REPORT_NAME'], 'file': 'environment', 'type': 'environment', 'usr_id': email_address}
    executeScriptQuery(os.path.join(dbPath, 'admin.db'), open(os.path.join(SQL_CONFIG, 'log_deploy.sql')).read(), params=queryParams)

    shutil.copyfile(os.path.join(reportObj.http['ARES_TMPL'], 'tmpl_report.py'), os.path.join(scriptPath, scriptName))
    fileFullPath = os.path.join(scriptPath, scriptName)
    with zipfile.ZipFile("%s.zip" % fileFullPath, 'w') as zf:
      zf.write(fileFullPath, "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), scriptName))

    os.makedirs(os.path.join(scriptPath, 'outputs'))
    return json.dumps("New environment created: %s" % scriptName), 200

  return json.dumps("Existing Environment"), 200

@report.route("/upload/<report_type>/<report_name>/<user_name>", methods = ['POST'])
def uploadFiles(report_type, report_name, user_name):
  """ Add all the files that a users will drag and drop in the section """
  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  result = []
  reportTypes = {'report': (['.PY'], None), 'configuration': (['.JSON'], 'config'),
                 'ajax': (['.PY'], 'ajax'), 'javascript': (['.JS'], 'js'),
                 'views': (['.TXT', '.CSV'], 'statics'), 'outputs': (None, 'outputs'),
                 'styles': (['.CSS', '.JS'], 'styles'), 'saved': (['.HTML'], 'saved')
                 }
  dbPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db')

  if not checkAuth(dbPath, report_name, user_name):
    return json.dumps('Not authorized to deploy on environment: %s' % report_name), 500

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
        elif path is 'styles':
          userFullPath = os.path.join(current_app.config['ROOT_PATH'], 'static', 'users', report_name)
          if not os.path.exists(userFullPath):
            os.makedirs(userFullPath)
          fullPath = os.path.join(userFullPath, file.filename.lower().split('.')[-1])
          if not os.path.exists(fullPath):
            os.makedirs(fullPath)
          fileFullPath = os.path.join(fullPath, file.filename)
        else:
          filePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, path)
          if not os.path.exists(filePath):
            os.makedirs(filePath)
          fileFullPath = os.path.join(filePath, file.filename)
      file.save(fileFullPath)
      queryParams = {'report_name': report_name, 'file': file.filename, 'type': report_type, 'usr_id': user_name}
      executeScriptQuery(dbPath, open(os.path.join(SQL_CONFIG, 'log_deploy.sql')).read(), params=queryParams)

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
  #echo(Ares.moduleFromAlias(component))
  #echo(Ares.moduleFromAlias(component).aresDesigner(compId))
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
@report.route("/download/package/<name>")
def downloadPackage(name):
  modules = getattr(packages, name, None)
  memory_file = io.BytesIO()
  files, remap = [], {}
  # Add the files to the package
  for folder in modules.get('INCLUDED', {'FOLDERS': []}).get('FOLDERS', []):
    path = os.path.join(*folder)
    for file in os.listdir(path):
      filePath = os.path.join(path, file)
      if not Ares.isExcluded(current_app.config['ROOT_PATH'], file) and os.path.isfile(filePath):
        files.append(filePath)

  for folder in modules.get('INCLUDED', {'FILES': []}).get('FILES', []):
    filePath = os.path.join(*folder)
    if os.path.isfile(filePath):
      files.append(filePath)

  # Remove the files from the package
  for folder in modules.get('EXCLUDED', {'FOLDERS': []}).get('FOLDERS', []):
    path = os.path.join(*folder)
    for file in os.listdir(path):
      filePath = os.path.join(path, file)
      if not Ares.isExcluded(current_app.config['ROOT_PATH'], file) and os.path.isfile(filePath) and filePath in files:
        files.remove(filePath)
  for folder in modules.get('EXCLUDED', {'FILES': []}).get('FILES', []):
    filePath = os.path.join(*folder)
    if os.path.isfile(filePath) and filePath in files:
      files.remove(filePath)

  # Store the file and folder remappings to structure the zip archive
  for remapSrc, remapDst in modules.get('REMAP', {'FOLDERS': {}}).get('FOLDERS', {}).items():
    if not remapDst:
      remap[os.path.join(*remapSrc)] = ''
    else:
      remap[os.path.join(*remapSrc)] = os.path.join(*remapDst)
  for remapSrc, remapDst in modules.get('REMAP', {'FILES': {}}).get('FILES', {}).items():
    remap[os.path.join(*remapSrc)] = os.path.join(*remapDst)

  # write the zip archive
  with zipfile.ZipFile(memory_file, 'w') as zf:
    for file in files:
      for src, dst in remap.items():
        if file.startswith(src):
          remapFile = file.replace(src, dst)
          zf.write(file, remapFile)
          break

      else:
        zf.write(file, file)

  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='%s.zip' % name, as_attachment=True)

@noCache
@report.route("/download/<report_name>/outputs/<file_name>", methods = ['GET'])
def downloadOutputs(report_name, file_name):
  """ Download the up to date Ares package """
  aresoutputFile = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'outputs', file_name)
  #no need to check for error the normal raise should be fine
  return send_file(aresoutputFile)

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
