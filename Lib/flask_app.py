
import json
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/reports/<report_name>")
def report(report_name):
	import sys
	sys.path.append(r'E:\GitHub\Ares')
	sys.path.append(r'E:\GitHub\Ares\Lib')
	import Ares
	return render_template('ares_template.html', content=__import__(report_name).report(Ares.Report()))

@app.route("/reports_child/<report_name>", methods = ['GET'])
def child(report_name):
	import sys
	sys.path.append(r'E:\GitHub\Ares')
	sys.path.append(r'E:\GitHub\Ares\Lib')
	print(report_name)
	import Ares
	reportObj = Ares.Report()
	for getValues in request.args.items():
	  reportObj.http['GET'][getValues[0]] = getValues[1]

	return render_template('ares_template.html', content=__import__(report_name).report(reportObj))

@app.route("/reports_ajax/<report_name>", methods = ['GET', 'POST'])
def ajaxCall(report_name):
	import sys
	sys.path.append(r'E:\GitHub\Ares')
	sys.path.append(r'E:\GitHub\Ares\Lib')
	
	import Ares
	reportObj = Ares.Report()
	for getValues in request.args.items():
	  reportObj.http['GET'][getValues[0]] = getValues[1]
	return json.dumps(__import__(report_name).call(reportObj))


if __name__ == "__main__":
    app.debug = True
    app.run()