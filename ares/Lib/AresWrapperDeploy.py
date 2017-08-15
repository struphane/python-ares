__author__ = 'HOME'

# For Python 2.7
# you need to have request installed on your computer
# pip install requests

import requests


reportName = 'RRR'
projectLocalPath = r'E:\GitHub\Ares\saturn'
filename = 'saturn.py'

# The Url to be used in order to create the environments in Ares
# This will allow the use of scripts instead of the web interface
postUrlDeploy = 'http://127.0.0.1:5000/reports/upload/%s' % reportName
postUrlCreate = 'http://127.0.0.1:5000/reports/create/env'
withEnvCreation = True

files = {'file': open(r"%s\%s" % (projectLocalPath, filename))}
response = requests.post(postUrlDeploy, files=files)
if response.status_code == 500:
  print "########################################"
  print "The environment is potentially missing"
  print "########################################"
  if withEnvCreation:
    response = requests.post(postUrlCreate, {'REPORT': reportName})
    print response