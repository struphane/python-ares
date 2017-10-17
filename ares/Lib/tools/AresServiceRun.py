""" Local wrapper to test an ajax service locally

"""

from __future__ import print_function

import os
import sys
import json
import requests
import AresInstall # This import will work locally (because the structure is a bit different)

from ares.Lib import Ares

def serverRun(scriptName, httpParameters):
  """ To run the service from the server directly and then to get the result back """
  response = requests.post('%s/reports/ajax/%s/%s' % (AresInstall.SERVER_PATH, httpParameters['REPORT_NAME'], scriptName), httpParameters)
  data = json.loads(response.text)
  if data["status"] == 'Success':
    print("Service working correctly")
    print("result: ")
    print(data['data'])
  else:
    print("-------------------------------------------")
    print("Error in the service")
    print("Error message: ")
    print(data['message'])
    print("-------------------------------------------")

def localRuns(scriptName, aresObject):
  """ To run the test on the server by running locally """
  sys.path.append(os.path.join(aresObject.http['DIRECTORY'], 'ajax'))
  mod = __import__(scriptName)
  # Those two lines are just there to test the json conversion on the server side
  stringConversion = json.dumps(mod.call(aresObject))
  data = json.loads(stringConversion)
  print(data)

if __name__ == '__main__':
  """ Run the script """
  reportName = 'NewReport'
  ajaxService = 'ajaxNewReport.py' # This script should be defined in the ajax folder
  httpParameters = {'SCRIPT_NAME': 'test'}
  localTest = True

  if localTest:
    directory = os.getcwd() # The path of this script by default
    aresObj = Ares.Report()
    for key, val in httpParameters.items():
      aresObj.http[key.upper()] = val
    aresObj.http['DIRECTORY'] = os.path.join(directory, reportName)
    aresObj.http['REPORT_NAME'] = reportName
    localRuns(ajaxService.replace(".py", ""), aresObj)
  else:
    httpParameters['REPORT_NAME'] = reportName
    serverRun(ajaxService.replace(".py", ""), httpParameters)

