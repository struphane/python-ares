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
import hashlib
import logging
import datetime
from app import User, Team, EnvironmentDesc, DataSource, db
from functools import wraps, reduce
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import redirect, url_for, session, current_app, Blueprint, render_template, request, send_from_directory, send_file, make_response, render_template_string
from click import echo
from app import login_manager
import config

import re

regex = re.compile('[^a-zA-Z0-9_]')

# TODO add a check on the variable DIRECTORY to ensure that it cannot be changed
# TODO add the Flask url_for for an even using a text file like the attempt in JsTable
# TODO remove the use of chidren pages. Everything should use run

# Ares Framework
from Libs import AresChartsService
from ares import packages
from ares.Lib import Ares
from ares.Lib import AresImports
from ares.Lib import AresExceptions
from ares.Lib import AresSql
import logging

try:
  from Libs import AresUserAuthorization

  if config.ARES_MODE.upper() != 'LOCAL':
      from system.sqlite.db_config import setup_db_env
      setup_db_env.launch_db()
except:
  pass

AUTHORIZED_SOURCES = []
report = Blueprint('ares', __name__, url_prefix='/reports')

def no_login(function):
  function.no_login = True
  return function

@report.before_request
def ask_login():
  if not current_user.is_anonymous:
    return

  if getattr(current_app.view_functions[request.endpoint], 'no_login', False):
    return

  return redirect(url_for('ares.aresLogin', next=request.endpoint))

def noCache(f):
  @wraps(f)
  def respFunc(*args, **kwargs):
    resp = make_response(f(*args, **kwargs))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    return resp
  return respFunc


# Return the list of all the scripts needed to run this package
# This will group all the module CSS, JS and Python scripts
LIB_PACKAGE = {
  'JS': ['jquery-3.2.1.min.js', 'jquery-ui.min.js', 'bootstrap.min.js', 'bootstrap-select.min.js', 'd3.v3.js',
         'nv.d3.js', 'd3.layout.cloud.js'],
  'CSS': ['jquery-ui.css', 'bootstrap.min.css', 'bootstrap-theme.min.css', 'nv.d3.css',
          'bootstrap-select.min.css', 'w3.css'],
  'JSON': ['horizBars.json', 'linePlusBarData.json', 'lineWithFocus.json', 'multiBar.json', 'stackedAreaData.json']
}

BUILT_IN_PAGES_REQ = {
  'CSS': ['https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css', 'bootstrap.min.css', 'bdi.css',
          'bootstrap-simple-sidebar.css', 'jquery-ui.css'],
  'JS': ['jquery-3.2.1.min.js', 'jquery-ui.min.js', 'tether.min.js', 'bootstrap.min.js', 'ares.js']
}

@login_manager.user_loader
def load_user(email_addr):
  return User.query.filter_by(email=email_addr).first()

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
    httpParams[postValues[0].replace("amp;", "")] = postValues[1]
  for postValues in request.form.items():
    httpParams[postValues[0]] = postValues[1]
  httpParams['DIRECTORY'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  # Special environment configuration
  httpParams['CONFIG'] = {}
  httpParams['CONFIG']['WRK'] = config.WORK_PATH
  httpParams['CONFIG']['COMPANY'] = config.COMPANY
  for source in AUTHORIZED_SOURCES:
    httpParams[source] = session.get(source, None)
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

# @app.route('/')
# def register()

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

def isPrivateEnv(report_name):
  """ """
  db = AresSql.SqliteDB(report_name)
  query = ''' SELECT 1 FROM admin_env 
              INNER JOIN env_def ON env_def.env_id = admin_env.env_id
              WHERE env_def.env_name = '%s' ''' % report_name
  if not list(db.select(query)):
    return False

  return True


def checkAuth(report_name):
  """ Check whether user has authorization to change data within the environment """

  db = AresSql.SqliteDB(report_name)
  query = """SELECT 1 FROM env_auth 
               INNER JOIN env_def ON env_auth.env_id = env_def.env_id and env_def.env_name = '%s'
               INNER JOIN team_def ON env_auth.team_id = team_def.team_id and team_def.team_name = '%s'
               WHERE team_def.role = 'admin'""" % (report_name, session['TEAM'])

  subQuery = """SELECT 1 FROM env_auth
                WHERE temp_owner = '%s'""" % current_user.email
  if not list(db.select(query)):
    if not list(db.select(subQuery)):
      return False

    else:
      return True

  else:
    return True

def getAllowedSavedFiles(report_name, user_name, team, file_name):
  """ """
  query = """ SELECT 1
              FROM file_map fm
              INNER JOIN file_auth fa ON fa.file_id = fm.file_id
              INNER JOIN team_def td ON td.team_id = fa.team_id
              WHERE (td.team_name = '%s' OR fa.temp_owner = '%s')
              AND fm.file_type = 'saved'
              AND fm.alias = '%s'""" % (team, user_name, file_name)

  return list(db.select(query))

def getEnvAdmin(report_name):
  """ """
  db = AresSql.SqliteDB(report_name)
  query = """SELECT team_name 
             FROM team_def
             WHERE role != 'Normal'"""

  return list(db.select(query))

def getTempAdmin(report_name, username):
  """ """
  db = AresSql.SqliteDB(report_name)
  query = """SELECT env_auth.temp_owner FROM env_auth
              INNER JOIN env_def ON env_def.env_id = env_auth.env_id 
              WHERE env_def.env_name = '%s' 
              AND env_auth.temp_owner = '%s'
              """ % (report_name, username)
  if list(db.select(query)):
    return True

  return False

def getUserRole(dbPath, report_name, user_id):
  """ """
  db = AresSql.SqliteDB(report_name)
  query = """SELECT role 
             FROM team_def
             WHERE team_name = '%s' """ % session['TEAM']
  return list(db.select(dbPath, query))

def getFileAuth(report_name, file_name):
  """ """
  db = AresSql.SqliteDB(report_name)
  query = """SELECT file_auth.alias as "alias", file_map.disk_name as "raw_name" 
              FROM file_auth
              INNER JOIN file_map on file_map.file_id = file_auth.file_id
              INNER JOIN team_def on team_def.team_id = file_map.uid
              WHERE team_def.team_name = '%s' and file_map.raw_name = '%s' """ % (session['TEAM'], file_name)
  return list(db.select(query))

def getEnvFiles(report_name, team, username):
  """ """
  db = AresSql.SqliteDB(report_name)
  query = """SELECT file_map.disk_name as file
              FROM file_map
              INNER JOIN file_auth ON file_auth.file_id = file_map.file_id
              INNER JOIN team_def ON team_def.team_id = file_auth.team_id
              WHERE team_def.team_id = '%s' """ % team

  subquery = """SELECT file_map.disk_name as file
              FROM file_map
              INNER JOIN file_auth ON file_auth.file_id = file_map.file_id
              WHERE file_auth.temp_owner = '%s' """ % username

  return list(db.select(query)) + list(db.select(subquery))

def checkFileExist(dbPath, report_name, file_name):
  """ """
  db = AresSql.SqliteDB(report_name)
  query = """SELECT file_id 
                FROM file_map
                WHERE disk_name = '%s' """ % file_name
  return list(db.select(query))

def getAuthorizedFiles(fileConfigs, reportObj, report_name, userDirectory, fnct=None, ajax=False):
  ALIAS, DISK_NAME = 0, 1
  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  sqlFileDict = {'data': 'get_file_auth.sql', 'static': 'static_file_map.sql'}
  fileNameToParser = {}
  for fileConfig in fileConfigs:
    queryFileAuthPrm = {'team': session['TEAM'], 'file_cod': fileConfig['filename'], 'username': current_user.email, 'type': fileConfig.get('folder')}
    files = executeSelectQuery(os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db'),
      open(os.path.join(SQL_CONFIG, sqlFileDict.get(fileConfig.get('folder')))).read(), params=queryFileAuthPrm)
    for file in files:
      if fileConfig.get('parser', None):
        reportObj.files[file[DISK_NAME]] = fileConfig['parser'](open(os.path.join(userDirectory, fileConfig['folder'], file[DISK_NAME])))
      elif fileConfig.get('type') == 'pandas':
        reportObj.files[file[DISK_NAME]] = os.path.join(userDirectory, fileConfig['folder'], file[DISK_NAME])
      else:
        reportObj.files[file[DISK_NAME]] = open(os.path.join(userDirectory, fileConfig['folder'], file[DISK_NAME]))
      if not ajax:
        fileNameToParser[file[DISK_NAME]] = "%s.%s" % (fileConfig['parser'].__module__.split(".")[-1], fileConfig['parser'].__name__)
      if fnct == 'params' and not ajax:
        reportObj.fileMap.setdefault(file[ALIAS], []).append(file[DISK_NAME])
  return fileNameToParser


def syntaxEditor(inFile):
  pyKeywords = ['False', 'class', 'finally', 'is', 'return', 'None', 'continue',
                'for', 'lambda', 'try', 'True', 'def', 'from', 'nonlocal', 'while', 'and',
                'del', 'global', 'not', 'with', 'as', 'elif', 'if', 'or', 'yield', 'assert',
                'else', 'import', 'pass', 'break', 'except', 'in', 'raise', 'self']
  scriptData = []
  finishComment = True
  quoteType = None
  for line in inFile:
    tempData = line
    if tempData.strip().startswith('#'):
      tempData = '<mark class="green">%s</mark>' % tempData
      scriptData.append(tempData)
      continue

    elif (tempData.strip().startswith("'''") or tempData.strip().startswith('"""')) and finishComment:
      quoteType = tempData.strip()[:3]
      finishComment = False
      countQuote = len(tempData.strip().split(quoteType))
      if tempData.endswith("'''") or tempData.strip().endswith('"""') and countQuote > 2:
        finishComment = True
        tempData = '<mark class="green">%s</mark>' % tempData
      else:
        tempData = '<mark class="green">%s' % tempData
      scriptData.append(tempData)
      continue

    elif not finishComment:
      if tempData.strip().startswith("'''") or tempData.strip().startswith('"""'):
        tempData = '%s</mark>' % tempData
        finishComment = True
      scriptData.append(tempData)
      continue

    elif tempData.endswith("'''") or tempData.strip().endswith('"""'):
      tempData = '%s</mark>' % tempData
      finishComment = True
      scriptData.append(tempData)
      continue

    if '#' in tempData:
      code, comment = tempData.split('#')
      comment = '%s</mark>' % comment
    else:
      code, comment = tempData, ''
    for word in pyKeywords:
      code = re.sub(r'\b(%s)\b' % word, '<mark class="blue">%s</mark>' % word, code)

    tempData = '<mark class="green">#'.join([code, comment]) if comment else code
    scriptData.append(tempData)
  scriptData = ''.join(scriptData)
  return scriptData
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

@report.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(current_app.config['ROOT_PATH'], 'static', 'images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@report.route("/deploy", methods=['GET'])
def aresDeploy():
  """ """
  jsImports, cssImports = [], []
  for jsImport in BUILT_IN_PAGES_REQ['JS']:
    jsImports.append(render_template_string("<script language='javascript' type='text/javascript' src='{{ url_for('static', filename='js/%s') }}'></script>" % jsImport))
  for cssImport in BUILT_IN_PAGES_REQ['CSS']:
    if not cssImport.startswith('http'):
      cssImports.append(render_template_string("<link rel='stylesheet' href='{{ url_for('static', filename='css/%s') }}'>" % cssImport))
    else:
      cssImports.append(render_template_string("<link rel='stylesheet' href='%s' }}'>" % cssImport))
  return render_template('ares_deployment.html', cssImport='\n'.join(cssImports), jsImport='\n'.join(jsImports))

@report.route("/", defaults={'report_name': '_AresReports', 'script_name': '_AresReports'})
@report.route("/index", defaults={'report_name': '_AresReports', 'script_name': '_AresReports'})
@report.route("/run/<report_name>", defaults={'script_name': None}, methods = ['GET', 'POST'])
@report.route("/run/<report_name>/<script_name>", methods = ['GET', 'POST'])
def run_report(report_name, script_name):
  """
  Run the report

  """
  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  onload, jsCharts, side_bar, envName, jsGlobal, scriptData = '', '', [], '', '', ''
  fileNameToParser = {}
  viewScript, downloadEnv = False, False
  cssImport, jsImport = '', ''
  isAuth = True
  reportObj = Ares.Report()
  adminEnv, fileRules = False, False
  #TODO Improve this
  # Ensure that all the modules attached to a report have been removed
  # This will be a problem is multiple request at the same time (especially if they take some time
  for reportFolderName in ['utils', 'ajax']:
    if reportFolderName in sys.modules:
      del sys.modules[reportFolderName]


  try:
    if script_name is None:
      script_name = report_name
    # add the folder directory to the python path in order to run the script
    # The underscore folders are internal onces and we do not need to include them to the classpath
    if not report_name.startswith("_"):
      fileRules = True
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
      for rec in getEnvAdmin(report_name):
        if rec['team_name'] == session['TEAM']:
          adminEnv = True
          break

      else:
        if getTempAdmin(report_name, current_user.email):
          adminEnv = True

      if os.path.exists(os.path.join(config.ARES_USERS_LOCATION, report_name, "%s.py" % script_name)):
        inFile = open(os.path.join(config.ARES_USERS_LOCATION, report_name, "%s.py" % script_name))
        scriptData = syntaxEditor(inFile)
        inFile.close()

      if  script_name != report_name and config.ARES_MODE.upper() != 'LOCAL':
        dbPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db')
        queryParams = {'script_name': script_name, 'env_name': report_name, 'username': current_user.email, 'team_name': session['TEAM']}
        executeScriptQuery(dbPath, open(os.path.join(SQL_CONFIG, 'log_request.sql')).read(), params=queryParams)
      side_bar = []
      if not userDirectory in sys.path:
        sys.path.append(userDirectory)
    else:
      side_bar = []
      systemDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'reports', report_name)
      if not systemDirectory in sys.path:
        sys.path.append(systemDirectory)

      # In this context we need the generic user directory as we are in a system report
      # Users should not be allowed to create env starting with _
      #TODO put in place a control
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)

    reportObj.http = getHttpParams(request)
    reportObj.reportName = report_name
    if script_name in sys.modules:
      del sys.modules[script_name]

    # Import dedicated to the script to be displayed
    mod = __import__(script_name) # run the report
    if reportObj.http.get('show_params') == '1' and getattr(mod, 'HTTP_PARAMS', []):
      fnct = 'params'
    else:
      fnct = 'report'
      for param in getattr(mod, 'HTTP_PARAMS', []):
        if not param['code'] in reportObj.http:
          if not 'dflt' in param:
            fnct = 'params'
            break

          else:
            reportObj.http[param['code']] = param['dflt']
    # Set some environments variables which can be used in the report
    reportObj.http.update( {'FILE': script_name, 'REPORT_NAME': report_name, 'DIRECTORY': userDirectory} )
    fileNameToParser = getAuthorizedFiles(getattr(mod, 'FILE_CONFIGS', []), reportObj, report_name, userDirectory, fnct=fnct)
    modal = None
    if fnct == 'params':
      modal = reportObj.modal('Open Report Parameters')
      modal.modal_header = "Report parameters"
      modal.http = reportObj.http
      modal.files = reportObj.files
      getattr(mod, fnct)(modal)
      modal.internalLink('Run', script_name, attrs=modal.httpParams)
      reportObj.jsOnLoadFnc.add("%s.modal('show'); " % modal.jqId)
    else:
      getattr(mod, fnct)(reportObj)
    typeDownload = getattr(mod, 'DOWNLOAD', 'BOTH')
    if typeDownload == 'BOTH':
      downloadEnv = report_name

    # Import the main report name
    # This import is used to retrieve global information
    report = __import__(report_name) # run the report
    envName = getattr(report, 'NAME', '')
    if hasattr(report, 'envParams'):
      # Special function to add some global parameters
      # This should avoid the popup to be redefined in each sub report
      propParams = reportObj.parameters('Parameters')
      for param in getattr(mod, 'HTTP_PARAMS', []):
        if param['code'] in reportObj.http:
          propParams.httpParams[param['code']] = reportObj.http[param['code']]
      getattr(report, 'envParams')(propParams)
      if modal is not None:
        propParams.httpParams = modal.httpParams.update(propParams.httpParams)
      propParams.internalLink('Update Parameters', script_name, attrs=propParams.httpParams)
      side_bar.append(str(propParams))

    side_bar.append('<div style="color:white; margin-top:10px;font-size:16px;height:20px"><b>&nbsp;Dashboard</b></div>')
    for categories, links in getattr(report, 'SHORTCUTS', []):
      side_bar.append('<div style="color:white;font-size:14px;height:20px;margin-top:10px"><b>&nbsp;&nbsp;&nbsp;&nbsp;%s</b></div>' % categories)
      for name, scriptName in links:
        side_bar.append(render_template_string('<li><a style="height:20px;white-space: nowrap;vertical-align: middle;padding-top:1px" href="{{ url_for(\'ares.run_report\', report_name=\'%s\', script_name=\'%s\') }}">%s</a></li>' % (report_name, scriptName.replace(".py", ""), name)))
    cssImport, jsImport, onload, content, jsCharts, jsGlobal = reportObj.html()
    # Database caches will be stored in the reportObj.dbCaches
    # Nothing related to the DB should be done in ares.py in order to allow users to run everything locally
  except AresExceptions.AuthException as e:
    isAuth = False
    content = str(traceback.format_exc()).replace("(most recent call last):", "(most recent call last): <BR /><BR />").replace("File ", "<BR />File ")
    content = content.replace(", line ", "<BR />&nbsp;&nbsp;&nbsp;, line ")
  except Exception as e:
    logging.debug(e)
    #TODO use the import factory to generate the below strings
    cssImport = ''''<link rel="stylesheet" href="/static/css/font-awesome.min.css" type="text/css">
                    <link rel="stylesheet" href="/static/css/bootstrap.min.css" type="text/css">
                    <link rel="stylesheet" href="/static/css/nv.d3.min.css" type="text/css">
                    <link rel="stylesheet" href="/static/css/bdi.css" type="text/css">
                    <link rel="stylesheet" href="/static/css/bootstrap-simple-sidebar.css" type="text/css"> '''
    jsImport = '''
                  <script language="javascript" type="text/javascript" src="/static/js/jquery-3.2.1.min.js"></script>
                  <script language="javascript" type="text/javascript" src="/static/js/jquery-ui.min.js"></script>
                  <script language="javascript" type="text/javascript" src="/static/js/tether.min.js"></script>
                  <script language="javascript" type="text/javascript" src="/static/js/bootstrap.min.js"></script>
                  <script language="javascript" type="text/javascript" src="/static/js/ares.js"></script>
               '''
    content = str(traceback.format_exc()).replace("(most recent call last):", "(most recent call last): <BR /><BR />").replace("File ", "<BR />File ")
    content = content.replace(", line ", "<BR />&nbsp;&nbsp;&nbsp;, line ")
  finally:
    # Try to unload the module
    htmlArchives, htmlConfigs, htmlStatics = [], [], []
    savedHtmlLocation = os.path.join(userDirectory, 'saved')
    if os.path.exists(savedHtmlLocation):
      for htmlPage in os.listdir(savedHtmlLocation):
        htmlArchives.append(render_template_string("<a class='dropdown-item' href='{{ url_for('ares.savedHtmlReport', report_name='%s', html_report='%s') }}' target='_blank'>%s</a>" % (report_name, htmlPage, "".join(htmlPage.split(".")[:-1]))))
    fileStatic = os.path.join(userDirectory, 'static')
    if os.path.exists(fileStatic):
      for staticPage in os.listdir(fileStatic):
        if not staticPage.startswith('filterTable_') and not staticPage.startswith('sortTable_'):
          static_code_rsl = executeSelectQuery(os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db'), "SELECT alias FROM file_map WHERE disk_name = '%s'" % staticPage)
          if not static_code_rsl:
            continue

          static_code = static_code_rsl[0][0]
          htmlStatics.append(render_template_string("<a class='dropdown-item' href='{{ url_for('ares.run_report', report_name='_AresReports', script_name='AresReportStaticView', user_report_name='%s', user_script_name='%s', static_file='%s', static_code='%s', file_parser='%s') }}' target='_blank'>%s</a>" % (report_name, script_name, staticPage, static_code, fileNameToParser.get(staticPage, ''), staticPage)))

    if isAuth:
      if not report_name.startswith("_"):
        if userDirectory in sys.path:
          sys.path.remove(userDirectory)
        # Logic to remove all the modules attaced to a report
        for module, ss in sys.modules.items():
          if userDirectory in str(ss):
            del sys.modules[module]
      else:
        sys.path.remove(systemDirectory)
        for module, ss in dict(sys.modules).items():
          if systemDirectory in str(ss):
            del sys.modules[module]
      for f in reportObj.files.values():
        if hasattr(f, 'close'):
          f.close()
  return render_template('ares_template_basic.html', cssImport=cssImport, jsImport=jsImport,
                         jsOnload=onload, content=content, jsGraphs=jsCharts, side_bar="\n".join(side_bar),
                         name=envName, jsGlobal=jsGlobal, htmlArchives="\n".join(htmlArchives),
                         viewScript=viewScript, downloadEnv=downloadEnv, htmlStatics="\n".join(htmlStatics),
                         htmlConfigs="\n".join(htmlConfigs), report_name=report_name, script_name=script_name,
                         adminEnv=adminEnv, fileRules=fileRules, scriptData=scriptData)


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
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
      sys.path.append(userDirectory)
      if script == 'SrvSaveToFile' and config.ARES_MODE != 'local':
        queryParams = {'report_name': reportObj.http['reportName'], 'file': reportObj.http['fileName'], 'type': 'file', 'team_name': session['TEAM'], 'username': current_user.email}
        logEventDeployment(os.path.join(userDirectory, reportObj.http['reportName']), queryParams)
    else:
      userDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
      sys.path.append(userDirectory)
    reportObj.http['FILE'] = None
    reportObj.http['REPORT_NAME'] = report_name
    reportObj.http['DIRECTORY'] = userDirectory
    reportObj.reportName = report_name
    ajaxScript = script.replace(".py", "")
    mod = __import__("ajax.%s" % ajaxScript)
    ajaxMod = getattr(mod, ajaxScript)
    getAuthorizedFiles(getattr(ajaxMod, 'FILE_CONFIGS', []), reportObj, report_name, userDirectory, ajax=True)
    result = {'status': 'Success', "data": ajaxMod.call(reportObj)}
  except Exception as e:
    logging.debug(e)
    content = traceback.format_exc()
    error = True
  finally:
    sys.path.remove(userDirectory)
    for module, ss in sys.modules.items():
      if userDirectory in str(ss):
        del sys.modules[module]

    for f in reportObj.files.values():
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

@report.route("/account", methods=['GET'])
def userAccount():
  """ """
  script_name = '_AresUserAccount'  # run the report
  onload, jsCharts, error, side_bar, envName, jsGlobal = '', '', False, [], '', ''

  systemDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'reports', '_AresUserAccount')
  if not systemDirectory in sys.path:
    sys.path.append(systemDirectory)

  userData = User.query.filter_by(email=current_user.email).first()
  team_def = Team.query.filter_by(team_id=userData.team_id).first()
  reportObj = Ares.Report()
  reportObj.http = getHttpParams(request)
  reportObj.http['REPORT_NAME'] = script_name
  reportObj.reportName = script_name
  mod = __import__(script_name)  # run the report
  envName = getattr(mod, 'NAME', '')
  sourceRec = []
  for source in userData.datasources:
    sourceRec.append({'src_nam': source.source_name, 'src_username': source.source_username,
                         'src_pwd': AresUserAuthorization.decrypt(source.source_pwd,
                                                      session['PWD'], source.salt)})
  reportObj.http['USERDATA'] = {'envs': userData.environments,
                                'sources': sourceRec,
                                'team': team_def.team_name
                                }
  reportObj.http['USERNAME'] = current_user.email
  mod.report(reportObj)
  cssImport, jsImport, onload, content, jsCharts, jsGlobal = reportObj.html()
  return render_template('ares_template_basic.html', cssImport=cssImport, jsImport=jsImport,
                         jsOnload=onload, content=content, jsGraphs=jsCharts, side_bar="\n".join(side_bar),
                         name=envName, jsGlobal=jsGlobal, htmlArchives="\n".join([]))


@report.route("/<report_name>/fileAuth", methods=['GET'])
def fileAuthorizations(report_name):
  """ File Authorization page for the environment """

  teamLst = Team.query.all()
  teamRec = {}
  for team in teamLst:
    teamStr = "%s#%s" % (team.team_name, team.team_email)
    teamRec[teamStr] = team.team_id

  script_name = '_AresFileManagement'  # run the report
  onload, jsCharts, error, side_bar, envName, jsGlobal = '', '', False, [], '', ''
  systemDirectory = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'reports', script_name)
  if not systemDirectory in sys.path:
    sys.path.append(systemDirectory)
  ajaxPath = os.path.join(systemDirectory, 'ajax')
  if os.path.exists(ajaxPath) and not ajaxPath in sys.path:
    sys.path.append(ajaxPath)


  reportObj = Ares.Report()
  reportObj.http = getHttpParams(request)
  reportObj.reportName = report_name
  mod = __import__(script_name)  # run the report
  envName = getattr(mod, 'NAME', '')
  # Set some environments variables which can be used in the report
  reportObj.http['FILE'] = script_name
  reportObj.http['REPORT_NAME'] = report_name
  reportObj.http['DIRECTORY'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
  reportObj.http['TEAM'] = session['TEAM']
  reportObj.http['REGISTERED_TEAMS'] = teamRec
  reportObj.http['USERNAME'] = current_user.email
  mod.report(reportObj)
  cssImport, jsImport, onload, content, jsCharts, jsGlobal = reportObj.html()
  return render_template('ares_template_basic.html', cssImport=cssImport, jsImport=jsImport,
                         jsOnload=onload, content=content, jsGraphs=jsCharts, side_bar="\n".join(side_bar),
                         name=envName, jsGlobal=jsGlobal, htmlArchives="\n".join([]))

@report.route("/<report_name>/admin", methods=['GET'])
def adminEnv(report_name):
  """ Admin session for the environment """
  isAdmin = False

  for rec in getEnvAdmin(report_name):
    if rec['team_name'] == session['TEAM']:
      isAdmin = True
  else:
    if getTempAdmin(report_name, current_user.email):
      isAdmin = True

  if not isAdmin:
    return "You are not an administrator of this environment", 500

  teamLst = Team.query.all()
  teamRec = {}
  for team in teamLst:
    teamStr = "%s#%s" % (team.team_name, team.team_email)
    teamRec[teamStr] = team.team_id

  script_name = '_AresAdmin' # run the report
  onload, jsCharts, error, side_bar, envName, jsGlobal = '', '', False, [], '', ''
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
  reportObj.http['TEAM_DSC'] = teamRec
  mod.report(reportObj)
  cssImport, jsImport, onload, content, jsCharts, jsGlobal = reportObj.html()
  return render_template('ares_template_basic.html', cssImport=cssImport, jsImport=jsImport,
                         jsOnload=onload, content=content, jsGraphs=jsCharts, side_bar="\n".join(side_bar),
                         name=envName, jsGlobal=jsGlobal, htmlArchives="\n".join([]))

@report.route("/saved/<report_name>/<html_report>", methods = ['GET'])
def savedHtmlReport(report_name, html_report):
  """  """
  if config.ARES_MODE.upper() != 'LOCAL':
    if not getAllowedSavedFiles(report_name, session['TEAM'], current_user.email, html_report):
      raise AresExceptions.AuthException("""Sorry, you are not authorised to view this report - please contact this environment administrator to request access.
                                         Administrator: %s """ ", ".join([rec['email_addr'] for rec in getEnvAdmin()]))


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

def logEventDeployment(scriptPath, queryParams):
  """ """

  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  dbPath = os.path.join(scriptPath, 'db', 'admin.db')
  executeScriptQuery(dbPath, open(os.path.join(SQL_CONFIG, 'log_deploy.sql')).read(), params=queryParams)

@report.route("/create/env", methods = ['POST'])
def ajaxCreate():
  """ Special Ajax call to set up the environment

  This service will create the environment and also add an emtpy report.
  The log file will be produce and the zip archive with the history will be defined
  """
  email_address = current_user.email
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
    os.makedirs(dbPath)
    executeScriptQuery(os.path.join(dbPath, 'admin.db'), open(os.path.join(SQL_CONFIG, 'create_sqlite_schema.sql')).read())
    #fisrt user insert to appoint an admin on the environment

    queryParams = {'team_name': session['TEAM'].replace('#TEMP', ''), 'env_name': reportObj.http['REPORT_NAME']}
    firtsUsrRights = open(os.path.join(SQL_CONFIG, 'create_env.sql')).read()
    executeScriptQuery(os.path.join(dbPath, 'admin.db'), firtsUsrRights, params=queryParams)
    env_dsc = EnvironmentDesc(reportObj.http['REPORT_NAME'], session['TEAM_ID'])
    db.add(env_dsc)
    db.commit()
    queryParams = {'report_name': reportObj.http['REPORT_NAME'], 'file': 'environment', 'type': 'environment', 'team_name': session['TEAM'], 'username': email_address}
    logEventDeployment(scriptPath, queryParams)

    shutil.copyfile(os.path.join(reportObj.http['ARES_TMPL'], 'tmpl_report.py'), os.path.join(scriptPath, scriptName))

    os.makedirs(os.path.join(scriptPath, 'data'))
    return json.dumps("New environment created: %s" % scriptName), 200

  return json.dumps("Existing Environment"), 200

@report.route("/deployment/", methods = ['POST'])
def deployment():
  """
  """
  hasFiles = False
  if request.files.getlist('file')[0]:
    hasFiles = True
  DATA = {'files': list(zip(request.files.getlist('file'), request.form.getlist('File Type'), request.form.getlist('file_code')))}
  for file, fileType, fileCod in DATA['files']:
    if fileType in ['static', 'data'] and not fileCod:
      return json.dumps('Error - You should specify a file code for statics and outputs'), 500

  env = request.values['env']
  isNew = True if request.values['isNew'] == 'true' else False
  if isNew:
    createEnv(env)
  if hasFiles:
    return deployFiles(env, DATA)

  return json.dumps("Environment created"), 200

def createEnv(environment):
  """ Special Ajax call to set up the environment

  This service will create the environment and also add an emtpy report.
  The log file will be produce and the zip archive with the history will be defined
  """
  DIR_LIST = ['data', 'ajax', 'static', 'styles', 'saved', 'utils', 'snapshot']
  email_addr = session['user_id']
  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  reportObj = Ares.Report()
  reportObj.http['DIRECTORY'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  reportObj.http['ARES_TMPL'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'tmpl')
  scriptName = "%s.py" % environment
  scriptPath = os.path.join(reportObj.http['DIRECTORY'],environment)
  if scriptName.startswith("_"):
    return json.dumps("Environment Name cannot start with _"), 500

  if not os.path.exists(scriptPath):
    os.makedirs(scriptPath)
    # envKey = os.urandom(24).encode('hex')
    # Create a dedicated database in the user environment
    # This will be there in order to ensure the data access but also it will allow us to check the admin and log tables
    dbPath = os.path.join(scriptPath, 'db')
    os.makedirs(dbPath)
    executeScriptQuery(os.path.join(dbPath, 'admin.db'), open(os.path.join(SQL_CONFIG, 'create_sqlite_schema.sql')).read())
    #fisrt user insert to appoint an admin on the environment

    queryParams = {'team_name': session['TEAM'].replace('#TEMP', ''), 'env_name': environment, 'username': email_addr, 'team_id': session['TEAM_ID']}
    # queryParams = {'team_name': session['TEAM'], 'env_name': environment,  'username': email_addr,}
    firtsUsrRights = open(os.path.join(SQL_CONFIG, 'create_env.sql')).read()
    executeScriptQuery(os.path.join(dbPath, 'admin.db'), firtsUsrRights, params=queryParams)
    queryParams = {'report_name': environment, 'file': 'environment', 'type': 'environment', 'username': email_addr, 'team_name': session['TEAM'], 'team_id': session['TEAM_ID']}
    executeScriptQuery(os.path.join(dbPath, 'admin.db'), open(os.path.join(SQL_CONFIG, 'log_deploy.sql')).read(), params=queryParams)

    shutil.copyfile(os.path.join(reportObj.http['ARES_TMPL'], 'tmpl_report.py'), os.path.join(scriptPath, scriptName))

    for dir in DIR_LIST:
      os.makedirs(os.path.join(scriptPath, dir))
      if dir in ['utils', 'ajax']:
        initFile = open(os.path.join(scriptPath, dir, '__init__.py'), 'w')
        initFile.close()
    return "New environment created: %s" % scriptName

  return "Existing Environment"

def deployFiles(env, DATA):
  """ """
  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  result = []
  user_name = current_user.email
  report_name = env
  reportTypes = {'report': (['.PY'], None), 'static': (['.DAT', '.TXT', '.CSV', '.JSON'], 'static'),
                 'data': (None, 'data'), 'styles': (['.CSS', '.JS'], 'styles'),
                 'saved': (['.HTML'], 'saved'), 'utils': (['.PY'], 'utils'), 'ajax': (['.PY'], 'ajax') }
  dbPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db')

  if not checkAuth(report_name):
    return json.dumps('Not authorized to deploy on environment: %s' % report_name), 500

  if report_name.startswith("_"):
    return json.dumps("Environment Name cannot start with _"), 500

  for fileObj, fileType, fileCod in DATA['files']:
    if fileType not in reportTypes:
      return json.dumps('Error %s category not recognized !' % fileType), 500

    ext, path = reportTypes[fileType]
    filename = fileObj.filename
    if filename == '':
      continue

    if fileType != 'data':
      # No checks for the data folder
      # User can deploy whatever they want in this folder
      fileWithoutExt = getFileName(filename, ext)
      if fileWithoutExt is None:
        return json.dumps('File extension %s not recognized for this category %s  !' % (ext, fileType)), 500

    if path is None:
      fileFullPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name,
                                  filename)
    else:
      filePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, path)
      if not os.path.exists(filePath):
        os.makedirs(filePath)
      fileFullPath = os.path.join(filePath, filename)
    fileObj.save(fileFullPath)
    if fileType in ['data', 'static', 'saved']:
      if not fileCod and fileType == 'data':
        return json.dumps('You have to provide a file code for the data type'), 500

      fileCod = filename if not fileCod else fileCod
      fileParams = {'filename': filename, 'fileCode': fileCod, 'file_type': fileType, 'username': user_name, 'team_name': session['TEAM'].replace('#TEMP', '')}
      executeScriptQuery(dbPath, open(os.path.join(SQL_CONFIG, 'create_file.sql')).read(), params=fileParams)
    queryParams = {'report_name': report_name, 'file': filename, 'type': fileType, 'username': user_name, 'team_name': session['TEAM']}
    executeScriptQuery(dbPath, open(os.path.join(SQL_CONFIG, 'log_deploy.sql')).read(), params=queryParams)
    result.append(filename)
  return json.dumps(result), 200

@report.route("/upload/<report_type>/<report_name>", methods = ['POST'])
def uploadFiles(report_type, report_name, user_name):
  """ Add all the files that a users will drag and drop in the section """
  SQL_CONFIG = os.path.join(current_app.config['ROOT_PATH'], config.ARES_SQLITE_FILES_LOCATION)
  result = []
  reportTypes = {'report': (['.PY'], None), 'configuration': (['.DAT', '.TXT', '.CSV', '.JSON'], 'config'),
                 'ajax': (['.PY'], 'ajax'), 'javascript': (['.JS'], 'js'),
                 'views': (['.TXT', '.CSV'], 'statics'), 'data': (None, 'data'),
                 'styles': (['.CSS', '.JS'], 'styles'), 'saved': (['.HTML'], 'saved')
                 }
  dbPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db')

  if not checkAuth(report_name):
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
      if report_type != 'data':
        # No checks for the data folder
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
      queryParams = {'report_name': report_name, 'file': file.filename, 'type': report_type, 'username': user_name, 'team_name': session['TEAM']}
      executeScriptQuery(dbPath, open(os.path.join(SQL_CONFIG, 'log_deploy.sql')).read(), params=queryParams)

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

@report.route("/download/dsc/json/<jsonFile>", methods = ['GET', 'POST'])
def downloadJsonFiles(jsonFile):
  if not jsonFile.endswith(".json"):
    jsonFile = "%s.json" % jsonFile

  mokfilePath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, 'json')
  return send_from_directory(mokfilePath, jsonFile, as_attachment=True)

@report.route("/download/<report_name>/package", methods = ['GET', 'POST'])
def downloadReport(report_name):
  """ Return in a Zip archive the full python package """
  dbPath = os.path.join(config.ARES_USERS_LOCATION, report_name, 'db', 'admin.db')
  memory_file = io.BytesIO()
  with zipfile.ZipFile(memory_file, 'w') as zf:
    reportPath = os.path.join(config.ARES_USERS_LOCATION, report_name)
    for (path, dirs, files) in os.walk(reportPath):
      for pyFile in  files:
        if Ares.isExcluded(current_app.config['SERVER_PATH'], file=pyFile):
          continue

        folder = path.replace("%s" % reportPath, "")
        if folder == '\data':
          listAuthFiles = [rec['file'] for rec in getEnvFiles(report_name, session['TEAM'], current_user.email)]
          if pyFile in listAuthFiles:
            zf.write(os.path.join(reportPath, path, pyFile), r"%s\%s\%s" % (report_name, folder, pyFile))
        else:
          zf.write(os.path.join(reportPath, path, pyFile), r"%s\%s\%s" % (report_name, folder, pyFile))

    # Add all the external libraries
    libPath = os.path.join(current_app.config['SERVER_PATH'], 'Libs')
    for (path, dirs, files) in os.walk(libPath):
      if '.svn' in path:
        continue

      for pyFile in  files:
        if Ares.isExcluded(current_app.config['SERVER_PATH'], file=pyFile):
          continue

        folder = path.replace("%s" % libPath, "")
        if pyFile in ['__init__.py', 'AresFileParser.py', 'AresChartsService.py']:
          zf.write(os.path.join(folder, libPath, pyFile), r"Libs\%s\%s" % (folder, pyFile))
        elif not path.endswith('Ares\Libs'):
          zf.write(os.path.join(folder, libPath, pyFile), r"Libs\%s\%s" % (folder, pyFile))

  logDownloadParam = {'email': current_user.email, 'team': session['TEAM'], 'report_name': report_name}
  executeScriptQuery(dbPath, open(os.path.join(current_app.config['SERVER_PATH'], config.ARES_SQLITE_FILES_LOCATION, 'log_download.sql')).read(), params=logDownloadParam)
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


@report.route("/download/package/<name>")
@noCache
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


@report.route("/editScript", methods = ['POST'])
def editScript():
  """ """
  scriptDtls = request.environ['HTTP_REFERER'].split('?')[0].split('/')
  if scriptDtls[-2] == 'run':
    script = open(os.path.join(config.ARES_USERS_LOCATION, scriptDtls[-1], "%s.py" % scriptDtls[-1]), 'w')
  else:
    script = open(os.path.join(config.ARES_USERS_LOCATION, scriptDtls[-2], "%s.py" % scriptDtls[-1]), 'w')
  try:
    for line in request.data.decode('utf-8').split('\n'):
      script.write('%s\n' % line)
  except Exception as e:
    logging.debug(e)
  finally:
    script.close()
  return 'OK'

@report.route("/download/<report_name>/data/<file_name>/<file_location>", methods = ['GET'])
@report.route("/download/<report_name>/data/<file_name>", defaults={'file_location': 'data'}, methods = ['GET'])
@noCache
def downloadOutputs(report_name, file_name, file_location):
  """ Download the up to date Ares package """
  aresoutputFile = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, file_location, file_name)
  #no need to check for error the normal raise should be fine
  return send_file(aresoutputFile, as_attachment=True)

@report.route("/download/in-memory", methods = ['POST'])
@noCache
def downloadMemory():
  """ Download the up to date Ares package """
  archive = ''
  return send_file(archive, as_attachment=True)

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

@report.route('/ares/source/create', methods=['GET', 'POST'])
def createDataSource():
  app_id = request.args['app_id']
  source = request.args['source']
  username = request.args['username']
  password = request.args['password']
  user = User.query.filter_by(email=app_id).first()
  encryptPwd, salt= AresUserAuthorization.encrypt(password, session['PWD'])
  dataSource = DataSource.query.filter_by(uid=user.uid, source_name=source).first()
  if dataSource:
    db.session.delete(dataSource)
    db.session.commit()
    session[source] = (username, password)
  dataSource = DataSource(source, user.uid, username, encryptPwd, salt)
  db.session.add(dataSource)
  db.session.commit()
  return json.dumps('Success'), 200

@report.route('/ares/addFileAuth', methods=['GET', 'POST'])
def addFileAuth():
  report_name = request.args['report_name']
  db = AresSql.SqliteDB(report_name)
  recSet = db.select("SELECT file_id FROM file_auth WHERE team_id = %s" % session['TEAM_ID'])
  fileLst = [rec['file_id'] for rec in recSet]
  file = request.args['file_id']
  if int(file) not in fileLst:
    return "Permission Denied", 401

  team_email = request.args.get('team', '')
  tempOwner = request.args.get('temp_owner', '')
  stt_dt = datetime.datetime.now().strftime('%Y-%m-%d') if request.args.get('stt_dt', '') == '' else  request.args['stt_dt']
  end_dt = '3001-01-01' if request.args.get('end_dt', '') == '' else request.args['end_dt']


  if not tempOwner and not team_email:
    print("Bad Data")
    return "Bad Data", 400

  if team_email:
    team_def = Team.query.filter_by(team_email=team_email).first()
    if not team_def:
      print("Team does not exist")
      return "Team does not exist - create it first", 400

    if team_def.team_id:
      db.modify("""INSERT INTO file_auth (file_id, team_id, stt_dt, end_dt) VALUES (%s, %s, '%s', '%s')""" % (file, team_def.team_id, stt_dt, end_dt))
      return "Success", 200

  if tempOwner:
    db.modify("""INSERT INTO file_auth (file_id, temp_owner, stt_dt, end_dt) VALUES (%s, '%s', '%s', '%s')""" % (file, tempOwner, stt_dt, end_dt))
    return "Success", 200


@report.route('/ares/create_team', methods=['GET', 'POST'])
def createTeam():
  """ """
  if request.environ.get('HTTP_ORIGIN') == request.host_url[:-1]:
    newTeam = Team.query.filter_by(team_name=request.args['team']).first()
    dbEnv = AresSql.SqliteDB(request.args['report_name'])
    if not newTeam:
      team = Team(request.args['team'], request.args['team_email'])
      db.session.add(team)
      db.session.commit()
      newTeam = Team.query.filter_by(team_name=request.args['team']).first()
    team_id = newTeam.team_id
    role = request.args.get('role', 'user')
    dbEnv.modify("""INSERT INTO team_def (team_id, team_name, role) VALUES (%s, '%s', '%s');
                 INSERT INTO env_auth (env_id, team_id)
                 SELECT env_def.env_id, %s
                 FROM env_def
                 WHERE env_def.env_name = '%s' ;""" % (team_id, request.args['team'], role, team_id, request.args['report_name']))
    return json.dumps('Success'), 200

  return json.dumps('Forbidden', 403)


@report.route("/ares/registration", methods = ['GET', 'POST'])
@no_login
def aresRegistration():
  """ """
  if request.method == 'GET':
    jsImport = render_template_string('<script language="javascript" type="text/javascript" src="{{ url_for(\'static\', filename=\'js/jquery-3.2.1.min.js\') }}"></script>')
    special_css = render_template_string('<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/aresLogin.css\')  }}" >')
    return render_template('ares_login_page.html', cssImport=special_css, jsImport=jsImport)

  if request.method == 'POST':
    data = request.form
    if User.query.filter_by(email=data['email_addr']).first():
      return redirect(url_for('ares.aresLogin', next=url_for('ares.run_report')))

    if not Team.query.filter_by(team_name=data['team']).first():
      team = Team(data['team'], data['team_email'])
      db.session.add(team)
    team_def = Team.query.filter_by(team_name=data['team']).first()
    user = User(data['email_addr'], team_def.team_id, data['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('ares.aresLogin', next=url_for('ares.run_report')))

@report.route("/ares/login", methods= ['GET', 'POST'])
@no_login
def aresLogin():
  """ """

  if request.method == 'GET':
    jsImport = render_template_string('<script language="javascript" type="text/javascript" src="{{ url_for(\'static\', filename=\'js/jquery-3.2.1.min.js\') }}"></script>')
    special_css = render_template_string('<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/aresLogin.css\')  }}" >')
    return render_template('ares_login_page.html', cssImport=special_css, jsImport=jsImport)

  if request.method == 'POST':
    data = request.form
    user = User.query.filter_by(email=data['email_addr']).first()
    next = request.args.get('next')
    if user:
      team_def = Team.query.filter_by(team_id=user.team_id).first()
      if user.password == hashlib.sha256(bytes(data['password'].encode('utf-8'))).hexdigest():
        suffix = '' if user.team_confirm == 'Y' else '#TEMP'
        session['TEAM'] = team_def.team_name + suffix
        session['TEAM_ID'] = user.team_id
        session['PWD'] = data['password']
        for source in user.datasources:
          session[source.source_name.upper()] = (source.source_username, AresUserAuthorization.decrypt(source.source_pwd, session['PWD'], source.salt))
        login_user(user)
        return redirect(next or url_for('ares.run_report'))

      return redirect(url_for('ares.aresLogin'))

    return redirect(url_for('ares.aresLogin'))


@report.route('/ares/logout')
def aresLogout():
  """ """
  session.clear()
  logout_user()
  return redirect(url_for('ares.aresLogin'))
