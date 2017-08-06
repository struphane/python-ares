""" Special app for the report section

"""

import json
import os
import sys
import zipfile
import io
import config

from flask import current_app, Blueprint, Flask, render_template, request, send_from_directory, send_file

# Ares Framework
from ares.Lib import Ares
from ares import report_index, report_index_page, report_index_set
report = Blueprint('ares', __name__, url_prefix='/reports')

# Return the list of all the scripts needed to run this package
# This will group all the module CSS, JS and Python scripts
LIB_PACKAGE = {
  'JS': ['jquery-3.2.1.min.js', 'jquery-ui.min.js', 'bootstrap.min.js', 'bootstrap-select.min.js', 'd3.v3.js',
         'nv.d3.js', 'd3.layout.cloud.js'],
  'CSS': ['jquery-ui.css', 'bootstrap.css', 'bootstrap.min.css', 'bootstrap-theme.min.css', 'nv.d3.css',
          'bootstrap-select.min.css', 'w3.css'],
  'PY': ['Ares.py', 'AresGraph.py', 'AresHtml.py', 'AresJs.py', '__init__.py'],
  'JSON': ['horizBars.json', 'linePlusBarData.json', 'lineWithFocus.json', 'multiBar.json', 'stackedAreaData.json']
}

@report.route("/report/dsc")
def report_description():
  """ Function to return the HTML object description and a user guide """

@report.route("/html/<objectName>")
def report_html_description(objectName):
  """ Function to return teh html defition of an object """


@report.route("/page/<report_name>")
def page_report(report_name):
  """
  """
  reportObj = Ares.Report()
  reportEnv = report_name.replace(".py", "")
  scriptEnv = os.path.join('user_reports', reportEnv)
  reportObj.http['SCRIPTS'] = os.listdir(scriptEnv)
  reportObj.http['SCRIPTS_NAME'] = report_name
  if os.path.isfile(r"%s\%s.py" % (scriptEnv, reportEnv)):
    sys.path.append(scriptEnv)
    mod = __import__(reportObj.http['SCRIPTS_NAME'])
    reportObj.http['SCRIPTS_DSC'] = mod.__doc__.strip()
    reportObj.http['SCRIPTS_CHILD'] = getattr(mod, 'CHILD_PAGES', {})
    reportObj.http['SCRIPTS_AJAX'] = getattr(mod, 'AJAX_CALL', {})
  else:
    reportObj.http.update({'SCRIPTS_DSC': '', 'SCRIPTS_CHILD': {}, 'SCRIPTS_AJAX': {}})
  reportObj.http['SCRIPTS_PATH'] = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
  return render_template('ares_template.html', content=report_index_page.report(reportObj).html(None))

@report.route("/index")
def index():
  """ Return the main page with the reports selection """
  aresObj = Ares.Report()
  aresObj.http['ROOT_PATH'] = current_app.config['ROOT_PATH']
  return render_template('ares_template.html', content=report_index.report(aresObj).html(None))

@report.route("/run/<report_name>")
def run_report(report_name):
	return render_template('ares_template.html', content=report_name.report(Ares.Report()).html(None))

@report.route("/child/<report_name>", methods = ['GET'])
def child(report_name):
	reportObj = Ares.Report()
	for getValues in request.args.items():
	  reportObj.http['GET'][getValues[0]] = getValues[1]

	return render_template('ares_template.html', content=report_name.report(reportObj).html(None))

@report.route("/create/<report_name>", methods = ['GET', 'POST'])
def ajaxCreate(report_name):
  """ Special Ajax call to set up the environment """
  reportObj = Ares.Report()
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
      file.save(r'user_reports/%s/%s' % (report_name, file.filename))
  return json.dumps({})

@report.route("/delete/<report_name>", methods = ['POST'])
def deleteFiles(report_name):
  import shutil
  if request.form.get('SCRIPT') is not None:
    deletedReportPath = 'deleted_report'
    if not os.path.exists(deletedReportPath):
      os.makedirs(deletedReportPath)

    shutil.move("user_reports/%s/%s" % (report_name, request.form.get('SCRIPT')),
                "%s/%s_%s" % (deletedReportPath, report_name, request.form.get('SCRIPT')))
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
  return send_file(os.path.join('user_reports',  report_name), mimetype='text/csv', attachment_filename=script, as_attachment=True)

@report.route("/download/<report_name>/package", methods = ['GET', 'POST'])
def downloadReport(report_name):
  """ Return in a Zip archive the full python package """
  memory_file = io.BytesIO()
  with zipfile.ZipFile(memory_file, 'w') as zf:
    reportPath = os.path.join(current_app.config['ROOT_PATH'], config.ARES_USERS_LOCATION, report_name)
    for reportFile in os.listdir(reportPath):
      if reportFile == '__pycache__':
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
