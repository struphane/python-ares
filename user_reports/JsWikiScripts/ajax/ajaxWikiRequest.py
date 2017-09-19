""" Ajax call for the request management

"""

import os
import json

def getRequests(path):
  """ Return the list of requests """
  requests = []
  if not os.path.exists(path):
    return requests

  for file in os.listdir(path):
    requests.append(file.replace(".json", ""))
  return requests

def call(aresObj):
  """ Process the new request and return the content of the requests folder """
  requestPath = os.path.join(aresObj.http['DIRECTORY'], 'requests')
  if not os.path.exists(requestPath):
    os.makedirs(requestPath)
  requestFile = open(os.path.join(requestPath, 'request_%s.json' % aresObj.http['SCRIPT_NAME']), "w")
  json.dump(aresObj.http, requestFile)
  return {'status': 'Request Sent', 'data': getRequests(requestPath)}
