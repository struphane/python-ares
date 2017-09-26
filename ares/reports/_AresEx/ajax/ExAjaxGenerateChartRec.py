"""

"""

import os
import json
import string
import random

# def getMultiRecordSet(aresObj):
#   """
#   """
#   recordSet = []
#   pathMultiBar = os.path.join(aresObj.http['DIRECTORY'], 'data', 'multiBar.json')
#   multibarRecSet = open(pathMultiBar)
#   data = json.load(multibarRecSet)
#   multibarRecSet.close()
#   for series in data:
#     for val in series.get('values'):
#       recordSet.append({'category': series.get('key'), 'Date': val[0], 'Value': val[1]})
#   return recordSet


JSON_DATA_MULTI = [
    {
      "key" : "North America" ,
      "values" : [ [ 1025409600000 , 23.041422681023] , [ 1028088000000 , 19.854291255832] , [ 1030766400000 , 21.02286281168] , [ 1033358400000 , 22.093608385173] , [ 1036040400000 , 25.108079299458] ]
    },

    {
      "key" : "Africa" ,
      "values" : [ [ 1025409600000 , 7.9356392949025] , [ 1028088000000 , 7.4514668527298] , [ 1030766400000 , 7.9085410566608] , [ 1033358400000 , 5.8996782364764] , [ 1036040400000 , 6.0591869346923] ]
    },

    {
      "key" : "South America" ,
      "values" : [ [ 1025409600000 , 7.9149900245423] , [ 1028088000000 , 7.0899888751059] , [ 1030766400000 , 7.5996132380614] , [ 1033358400000 , 8.2741174301034] , [ 1036040400000 , 9.3564460833513] ]
    },

    {
      "key" : "Asia" ,
      "values" : [ [ 1025409600000 , 13.153938631352] , [ 1028088000000 , 12.456410521864] , [ 1030766400000 , 12.537048663919] , [ 1033358400000 , 13.947386398309] , [ 1036040400000 , 14.421680682568] ]
    } ,

    {
      "key" : "Europe" ,
      "values" : [ [ 1025409600000 , 9.3433263069351] , [ 1028088000000 , 8.4583069475546] , [ 1030766400000 , 8.0342398154196] , [ 1033358400000 , 8.1538966876572] , [ 1036040400000 , 10.743604786849] ]
    } ,

    {
      "key" : "Australia" ,
      "values" : [ [ 1025409600000 , 5.1162447683392] , [ 1028088000000 , 4.2022848306513] , [ 1030766400000 , 4.3543715758736] , [ 1033358400000 , 5.4641223667245] , [ 1036040400000 , 6.0041275884577] ]
    } ,

    {
      "key" : "Antarctica" ,
      "values" : [ [ 1025409600000 , 1.3503144674343] , [ 1028088000000 , 1.2232741112434] , [ 1030766400000 , 1.3930470790784] , [ 1033358400000 , 1.2631275030593] , [ 1036040400000 , 1.5842699103708] ]
    }

]


BAR_DATA = [
    {
      "key": "Cumulative Return",
      "values": [
		 ["A Label", -29.76595777110],
		 ["C Label",  17.76595777110],
		 ["B Label", -196.76595777110]
      ]
    }
]


def getRecordSet():
  recordSet = []
  for series in JSON_DATA_MULTI:
    for val in series.get('values'):
      recordSet.append({'serie': series.get('key'), 'Date': val[0], 'Value': val[1]})
  return recordSet

def getBarRecordset():
  recordSet = []
  for series in BAR_DATA:
    for val in series.get('values'):
      recordSet.append({'serie': series.get('key'), 'Date': val[0], 'Value': val[1]})
  return recordSet

def call(aresObj):
  """ This will return fake data to feed the different test components in this framework """
  return {"status": "Updated", "data": getRecordSet(), "content": ""}

# def call(aresObj):
#   """
#   [ PLEASE DETAIL YOU SCRIPT HERE ]
#   """
#   recordSet = getRecordSet(aresObj)
#   recordSetJson = open(os.path.join(aresObj.http['DIRECTORY'], 'data', aresObj.http['file_name']), "w")
#   json.dump(recordSet, recordSetJson)
#   recordSetJson.close()
#
#   # And return the recordSet
#   return json.dumps(recordSet)

