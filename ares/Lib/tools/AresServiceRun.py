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
  sys.path.append(os.path.join(aresObject.http['DIRECTORY'], 'utils'))

  mod = __import__(scriptName)

  extFiles = dict([(extFile['filename'], extFile) for extFile in getattr(mod, 'FILE_CONFIGS', {})])
  for f in ['static', 'data']:
    fileDirectory = os.path.join(directory, reportName, f)
    if os.path.isdir(fileDirectory):
      for file in os.listdir(fileDirectory):
        if file in extFiles:
          if extFiles[file].get('type') == 'pandas':
            aresObject.files[file] = r"%s\%s" % (fileDirectory, file)
          else:
            inFile = open(os.path.join(fileDirectory, file))
            aresObject.files[file] = extFiles[file]['parser'](inFile)
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
    sys.path.append(aresObj.http['DIRECTORY'])
    aresObj.http['REPORT_NAME'] = reportName
    localRuns(ajaxService.replace(".py", ""), aresObj)
  else:
    httpParameters['REPORT_NAME'] = reportName
    serverRun(ajaxService.replace(".py", ""), httpParameters)

