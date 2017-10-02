from __future__ import print_function

# For Python 2.7
# you need to have request installed on your computer
# pip install requests

#Ares documentation is available here:
#  http://127.0.0.1:5000/reports/doc
#[This documentation is autogenerated from the script comments]

from __future__ import print_function
import requests
import json
import os
import AresInstall # This import will work locally (because the structure is a bit different)

# The Url to be used in order to create the environments in Ares
# This will allow the use of scripts instead of the web interface
postUrlDeploy = AresInstall.SERVER_PATH + r'/reports/upload/%s/%s'
postUrlCreate = r'%s/reports/create/env' % AresInstall.SERVER_PATH
postUrlScriptVersion = r"%s/reports/ares/version" % AresInstall.SERVER_PATH

def uploadFiles(files, reportName, withEnvCreation=False):
  """ Upload a file on the server """
  if withEnvCreation:
    response = requests.post(postUrlCreate, {'REPORT_NAME': reportName})
    if response.status_code == 500:
      print("########################################")
      print("Problem in the environment creation")
      print("########################################")
      print(response.text)

  for filename, fileType in files:
    folder = {'report': None, 'configuration': 'config', 'ajax': 'ajax', 'javascript': 'js', 'views': 'statics', 'outputs': 'outputs'}[fileType]
    if folder is not None:
      files = {'file': open(os.path.join(os.getcwd(), reportName, folder, filename))}
    else:
      files = {'file': open(os.path.join(os.getcwd(), reportName, filename))}
    response = requests.post(postUrlDeploy % (fileType, reportName), files=files)
    if response.status_code == 500:
      print("########################################")
      print("The environment is potentially missing")
      print("########################################")
      print(response.text)

def getPackageVersion():
  """  Check the version of the files on the server to ensure that the framework runs with the last version
  this service will return the last modification time and the size from [stat.st_mtime, stat.st_size]

    stat = os.stat(os.path.join(aresModulePath, pyFile))
  """
  # TODO add the comparison in the RIskLab shared folder
  response = requests.post(postUrlScriptVersion)
  print(json.loads(response.text))

if __name__ == '__main__':
  #createFolders(['aa', 'bb'])
  # Possible category of reports
  # report - For a bespoke python report which will have a defined display
  # ajax - For a python service. This will not display anything but return dictionaries
  # configuration - For static configuration files. Extension .json
  # javascript - In the folder js For javascript templates (like text files with a js extension)
  # views - in the folder statics For view configuration (like text files extension .txt)
  # outputs - in the folder outputs For any bespoke data - No extension checks)
  files = [('NewReport.py', 'report'),
           #('test.json', 'configuration'),
           #('params.txt', 'views'),
           #('params.zz', 'outputs'),
          ]
  REPORT = 'NewReport'

  # Function used to send files to the server
  uploadFiles(files, REPORT, withEnvCreation=True)


  # Function used to check your version of your local package
  # This will warn you if you have some important module not in line with the ones on the server
  # If your modules are not in line this might not work when you will deploy
  # getPackageVersion)_