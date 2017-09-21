"""

"""

import os
import json
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def getRecordSet(directory):
  """
  """
  recordSet = []
  pathMultiBar = os.path.join(directory, 'data', 'multiBar.json')
  multibarRecSet = open(pathMultiBar)
  data = json.load(multibarRecSet)
  multibarRecSet.close()
  for series in data:
    for val in series.get('values'):
      recordSet.append({'category': series.get('key'), 'Date': val[0], 'Value': val[1]})
  return recordSet


def call(aresObj):
  """
  [ PLEASE DETAIL YOU SCRIPT HERE ]
  """
  recordSet = getRecordSet(aresObj.http['DIRECTORY'])
  recordSetJson = open(os.path.join(aresObj.http['DIRECTORY'], 'data', aresObj.http['file_name']), "w")
  json.dump(recordSet, recordSetJson)
  recordSetJson.close()

  # And return the recordSet
  return json.dumps(recordSet)

