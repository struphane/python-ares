"""

"""

import os
import json
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def getRecordSet():
  """ """
  CCYS = ['EUR', 'GBP', 'USD']
  recordSet = []
  for i in range(10):
    recordSet.append({'ID': id_generator(), 'PTF': random.randint(1000, 1010), 'PTF2': random.randint(900, 1005),
                      'VAL2': random.uniform(0, 100),
                      'VAL3': random.uniform(0, 320),
                      'VAL': random.uniform(0, 100), 'CCY': CCYS[random.randint(0, 2)]})
  return recordSet

def call(aresObj):
  """
  [ PLEASE DETAIL YOU SCRIPT HERE ]
  """
  recordSet = getRecordSet()
  recordSetJson = open(os.path.join(aresObj.http['DIRECTORY'], 'data', aresObj.http['FILE_NAME']), "w")
  json.dump(recordSet, recordSetJson)
  recordSetJson.close()

  # And return the recordSet
  return {"status": "Updated", "data": recordSet, "content": ""}