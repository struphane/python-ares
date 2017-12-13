""" [SCRIPT COMMENT]

>>>> Important variables / functions

In the python layer
    aresObj.http['FILE'] is the current file
    aresObj.http['REPORT_NAME'] is the current report environment name
    aresObj.http['DIRECTORY'] is the report location

     def readFile(self, file, subfolders=None):
     def createFile(self, file, subfolders=None, checkFileExist=True):
     def getFolders(self):
     def getFiles(self, subfolders):


In the javascript layer
    display(data) to return the result in a notification modal popup
    preloader() to show a loading page

"""


NAME = 'Report' # The Report Name in the left menu
# The Shortcuts should be defined as below
# [(Cateogry Name, [List of the script in the root directory])]
# It is only possible to create new links for scripts in the root
SHORTCUTS = [] # All the possible link to other pages
FILE_CONFIGS = [] # All the static and output files configurationa
# The format in the above list should be as: {'filename': 'data.txt', 'folder': 'outputs', 'parser': InFilePricesConfig.InFilePices},

HTTP_PARAMS = [] # If you want to use the param method to set parameter before running hte report

import random

#def params(aresObj):
#  """ Optional param method to be run before the report method to set parameter """


def report(aresObj):
  '''
  Write your function below
  '''
  aresObj.title("My report Title")