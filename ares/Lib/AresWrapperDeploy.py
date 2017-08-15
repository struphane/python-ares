__author__ = 'HOME'

# For Python 2.7
# you need to have request installed on your computer
# pip install requests

import os
import requests


reportName = 'ircCalculator'
projectLocalPath = r'E:\GitHub\Ares\saturn'
filename = 'saturn.py'

# The Url to be used in order to create the environments in Ares
# This will allow the use of scripts instead of the web interface
serverPath = 'http://127.0.0.1:5000'
postUrlDeploy = r'%s/reports/upload/%s' % (serverPath, reportName)
postUrlCreate = r'%s/reports/create/env' % serverPath
postUrlFolderCreate = r'%s/reports/folder/create' % serverPath
withEnvCreation = True

def uploadFile(filename):
  """ Upload a file on the server """
  files = {'file': open(r"%s\%s" % (projectLocalPath, filename))}
  response = requests.post(postUrlDeploy, files=files)
  if response.status_code == 500:
    print "########################################"
    print "The environment is potentially missing"
    print "########################################"
    if withEnvCreation:
      response = requests.post(postUrlCreate, {'REPORT': reportName})
      print response

def createFolders(folders):
  """ Create a folder on the server """
  response = requests.post(postUrlFolderCreate, {'REPORT_NAME': reportName, 'FOLDERS': "/".join(folders)})


createFolders(['aa', 'bb'])