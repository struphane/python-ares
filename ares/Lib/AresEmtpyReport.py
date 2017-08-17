""" [SCRIPT COMMENT]

>>>> Important variables / functions

In the python layer
    aresObj.http['FILE'] is the current file
    aresObj.http['REPORT_NAME'] is the current report environment name

     def readFile(self, file, subfolders=None):
     def createFile(self, file, subfolders=None, checkFileExist=True):
     def getFolders(self):
     def getFiles(self, subfolders):


In the javascript layer
    display(data) to return the result in a notification modal popup
    preloader() to show a loading page

"""

AJAX_CALL = {} # Ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

def report(aresObj):
  # Write your report here

  return aresObj