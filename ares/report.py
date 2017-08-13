""" Special app for the report section

"""

import json
import os
import sys
import zipfile
import io
import collections

from flask import current_app, Blueprint, render_template, request, send_from_directory, send_file

import config


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
  'PY': ['Ares.py', 'AresGraph.py', 'AresHtml.py', 'AresJs.py', '__init__.py'],
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

@report.route("/dsc")
@report.route("/dsc/index")
def report_dsc_index():
  """ Main page for the Ares Documentation """
  aresObj = Ares.Report()
  aresObj.reportName = 'dsc'
  aresObj.childPages = {'html': 'html', 'graph': 'graph'}
  aresObj.title("Report Documentation")
  aresObj.title2("How to create a report")
  aresObj.title2("Report Components")
  aresComp = aresObj.anchor('HTML Component documentation')
  aresComp.addLink('html')
  aresObj.newline()
  aresComp = aresObj.anchor('Graph Component documentation')
  aresComp.addLink('graph')
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
    htmlObject = [['Class Name', 'Description']]
    for name, obj in inspect.getmembers(aresModule):
      if inspect.isclass(obj) and obj.alias is not None:
        aresObj.childPages[name] = '../../../child:dsc/html/%s' % obj.alias
        comp = aresObj.anchor(name)
        comp.addLink(name)
        htmlObject.append([comp, aresObj.code(obj.__doc__)])
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

@report.route("/child:dsc/graph")
def report_dsc_graph():
  """ Function to return the Graph object description and a user guide """
  import inspect
  from ares.Lib import AresHtmlGraph

  aresObj = Ares.Report()
  aresObj.reportName = 'dsc/graph'
  aresObj.childPages = {}
  graphObject = []
  aresObj.title("Graph Components")
  aresObj.title4(AresHtmlGraph.__doc__)
  for name, obj in inspect.getmembers(AresHtmlGraph):
    if inspect.isclass(obj) and name not in ['JsGraph', 'IndentedTree']:
      aresObj.childPages[name] = '../../../child:dsc/graph/%s' % name
      comp = aresObj.anchor(name)
      comp.addLink(name)
      graphObject.append([comp, aresObj.code(obj.__doc__)])
  aresObj.table(['Class Name', 'Description'], graphObject)
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
    data = json.load(data_file)
  getattr(aresObj, object.alias)(data)

  # Add the mock data as example
  aresObj.title3('Source Code')
  aresObj.childPages['graph'] = '../../../download/dsc/%s' % object.mockData
  comp = aresObj.anchor('Data Source') #, object.mockData, 'html', {'html': '../../../download/dsc/%s' % object.mockData}, None)
  comp.addLink('graph')
  aresObj.paragraph(['You can download the input data here: ', comp])
  compObj = aresComponents[chartName](0, data)
  aresObj.code(compObj.jsEvents()['addGraph'])
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
  reportObj.reportName = report_name
  reportEnv = report_name.replace(".py", "")
  scriptEnv = os.path.join(config.ARES_USERS_LOCATION, reportEnv)
  reportObj.http['SCRIPTS'] = os.listdir(scriptEnv)
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
  finally:
    # Internal callback functions, Users are not expected to use them
    reportObj.http['SCRIPTS_CHILD'] = children
    reportObj.http['SCRIPTS_AJAX'] = ajaxCalls
    reportObj.http['AJAX_CALLBACK'] = {}
    reportObj.http['SCRIPTS_PATH'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
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
  aresObj.http['ROOT_PATH'] = current_app.config['ROOT_PATH']
  aresObj.http['USER_PATH'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  onload, content, js = report_index.report(aresObj).html()
  return render_template('ares_template.html', onload=onload, content=content, js=js)

@report.route("/run/<report_name>")
def run_report(report_name):
  """ Run the report """
  try:
    sys.path.append(os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name))
    reportObj = Ares.Report()
    reportObj.http['FILE'] = report_name
    aresObj = __import__(report_name).report(reportObj)
    dId = aresObj.download(cssCls='bdiBar-download')
    aresObj.item(dId).js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': report_name, 'script': "%s.py" % report_name})
    spId = aresObj.downloadAll('', cssCls='bdiBar-download-all')
    aresObj.item(spId).js('click', "window.location.href='../download/%s/package'" % report_name)
    result = aresObj.html(None)
  except Exception as e:
    result = e
  finally:
    # Try to unload the module
    if report_name in sys.modules:
      del sys.modules[report_name]
  return render_template('ares_template.html', content=result)

@report.route("/child:<report_name>/<script>", methods = ['GET'])
def child(report_name, script):
  """ Return the content of the attached pages """
  reportObj = Ares.Report()
  reportObj.http['FILE'] = report_name
  for getValues in request.args.items():
    reportObj.http['GET'][getValues[0]] = getValues[1]

  try:
    sys.path.append(os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name))
    aresObj = __import__(script).report(reportObj)
    dId = aresObj.download(cssCls='bdiBar-download')
    aresObj.item(dId).js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': report_name, 'script': "%s.py" % script})
    spId = aresObj.downloadAll('', cssCls='bdiBar-download-all')
    aresObj.item(spId).js('click', "window.location.href='../download/%s/package'" % report_name)
    result = aresObj.html(None)
    del sys.modules[script]
  except Exception as e:
    result = e
  finally:
    if report_name in sys.modules:
      del sys.modules[report_name]

  return render_template('ares_template.html', content=result)

@report.route("/create/<report_name>", methods = ['GET', 'POST'])
def ajaxCreate(report_name):
  """ Special Ajax call to set up the environment """
  reportObj = Ares.Report()
  reportObj.http['USER_PATH'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION)
  for postValues in request.form.items():
	  reportObj.http['POST'][postValues[0]] = postValues[1]
  return json.dumps(report_index_set.call(reportObj))

@report.route("/ajax/<report_name>", methods = ['GET', 'POST'])
def ajaxCall(report_name):
  """ Generic Ajax call """
  reportObj = Ares.Report()
  for getValues in request.args.items():
    reportObj.http['GET'][getValues[0]] = getValues[1]
  for postValues in request.form.items():
    reportObj.http['POST'][postValues[0]] = postValues[1]
  return json.dumps(report_name.call(reportObj))

@report.route("/upload/<report_name>", methods = ['POST'])
def uploadFiles(report_name):
  """ Add all the files that a users will drag and drop in the section """
  if request.method == 'POST':
    for filename, fileType in request.files.items():
      file = request.files[filename]
      file.save(os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name, file.filename))
  return json.dumps({})

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
    for reportFile in os.listdir(reportPath):
      if reportFile == '__pycache__' or reportFile.endswith('pyc') :
        continue

      zf.write(os.path.join(reportPath, reportFile), reportFile)
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
    for pyFile in LIB_PACKAGE['PY']:
      zf.write(os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, "Lib", pyFile), os.path.join("Lib", pyFile), zipfile.ZIP_DEFLATED )
    for jsonFile in LIB_PACKAGE['JSON']:
      zf.write(os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, "json", jsonFile), os.path.join("json", jsonFile), zipfile.ZIP_DEFLATED )
    zf.write(os.path.join(current_app.config['ROOT_PATH'], config.ARES_FOLDER, "Lib", 'AresWrapper.py'), os.path.join('AresWrapper.py'), zipfile.ZIP_DEFLATED )
    zf.writestr('html/', '')
  memory_file.seek(0)
  return send_file(memory_file, attachment_filename='ares.zip', as_attachment=True)
