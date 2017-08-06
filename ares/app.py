""" Special app for the report section

"""

import json
import os
import sys

from flask import Blueprint, Flask, render_template, request, send_from_directory, send_file
app = Flask(__name__)

report = Blueprint('ares', __name__)
#app.register_blueprint(report) #, url_prefix='/pages')

app.config['ARES_FOLDER'] = 'ares'
app.config['ARES_USERS_LOCATION'] = 'user_reports'

print(app.config['APPLICATION_ROOT'])

@report.route("/report_description")
def report_description():
  """ Function to return the HTML object description and a user guide """

@report.route("/report_html/<objectName>")
def report_html_description(objectName):
  """ Function to return teh html defition of an object """


@report.route("/page/<report_name>")
def page_report(report_name):
  """
  """
  import os
  import sys
  sys.path.append(r'E:\GitHub\Ares')
  sys.path.append(r'E:\GitHub\Ares\Lib')

  import Ares
  reportObj = Ares.Report()
  reportEnv = report_name.replace(".py", "")
  scriptEnv = os.path.join('user_reports', reportEnv)
  reportObj.http['SCRIPTS'] = os.listdir(scriptEnv)
  reportObj.http['SCRIPTS_NAME'] = report_name
  if os.path.isfile(r"%s\%s.py" % (scriptEnv, reportEnv)):
    sys.path.append(scriptEnv)
    mod = __import__(reportObj.http['SCRIPTS_NAME'])
    reportObj.http['SCRIPTS_DSC'] = mod.__doc__
    reportObj.http['SCRIPTS_CHILD'] = getattr(mod, 'CHILD_PAGES', {})
    reportObj.http['SCRIPTS_AJAX'] = getattr(mod, 'AJAX_CALL', {})
  else:
    reportObj.http.update({'SCRIPTS_DSC': '', 'SCRIPTS_CHILD': {}, 'SCRIPTS_AJAX': {}})
  return render_template('ares_template.html', content=__import__('report_index_page').report(reportObj).html(None))

@report.route("/reports_index")
def report_index():
  """
  """
  import os
  import sys
  sys.path.append(r'E:\GitHub\Ares')
  sys.path.append(r'E:\GitHub\Ares\Lib')

  import Ares
  return render_template('ares_template.html', content=__import__('report_index').report(Ares.Report()).html(None))

@report.route("/reports/<report_name>")
def report(report_name):
	import sys
	sys.path.append(r'E:\GitHub\Ares')
	sys.path.append(r'E:\GitHub\Ares\Lib')
	import Ares
	return render_template('ares_template.html', content=__import__(report_name).report(Ares.Report()).html(None))

@report.route("/reports_child/<report_name>", methods = ['GET'])
def child(report_name):
	import sys
	sys.path.append(r'E:\GitHub\Ares')
	sys.path.append(r'E:\GitHub\Ares\Lib')

	import Ares
	reportObj = Ares.Report()
	for getValues in request.args.items():
	  reportObj.http['GET'][getValues[0]] = getValues[1]

	return render_template('ares_template.html', content=__import__(report_name).report(reportObj).html(None))

@report.route("/reports_ajax/<report_name>", methods = ['GET', 'POST'])
def ajaxCall(report_name):
	import sys
	sys.path.append(r'E:\GitHub\Ares')
	sys.path.append(r'E:\GitHub\Ares\Lib')
	
	import Ares
	reportObj = Ares.Report()
	for getValues in request.args.items():
	  reportObj.http['GET'][getValues[0]] = getValues[1]
	for postValues in request.form.items():
	  reportObj.http['POST'][postValues[0]] = postValues[1]
	  
	return json.dumps(__import__(report_name).call(reportObj))

@report.route("/script_upload/<report_name>", methods = ['POST'])
def uploadFiles(report_name):
	import sys
	sys.path.append(r'E:\GitHub\Ares')
	sys.path.append(r'E:\GitHub\Ares\Lib')
	if request.method == 'POST':
	  file = request.files['files']
	  file.save(r'user_reports/%s/%s' % (report_name, file.filename))
	return json.dumps({})

@report.route("/file_delete/<report_name>", methods = ['POST'])
def deleteFiles(report_name):
  import sys
  import shutil

  sys.path.append(r'E:\GitHub\Ares')
  sys.path.append(r'E:\GitHub\Ares\Lib')

  if request.form.get('SCRIPT') is not None:
    deletedReportPath = 'deleted_report'
    if not os.path.exists(deletedReportPath):
      os.makedirs(deletedReportPath)

    shutil.move("user_reports/%s/%s" % (report_name, request.form.get('SCRIPT')),
                "%s/%s_%s" % (deletedReportPath, report_name, request.form.get('SCRIPT')))
  return json.dumps({'SCRIPT': request.form.get('SCRIPT'), 'ENV': report_name})

@report.route("/script_download/<report_name>/<script>", methods = ['GET', 'POST'])
def downloadFiles(report_name, script):
  """
  """
  if not script.endswith(".py"):
    script = "%s.py" % script
  uploads = os.path.join('user_reports',  report_name)
  return send_file(uploads, mimetype='text/csv', attachment_filename=script, as_attachment=True)
  #return send_from_directory(directory=uploads, filename=script, as_attachment=True)
  
if __name__ == "__main__":
    app.debug = True
    app.run()