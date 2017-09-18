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

def report(aresObj):
  # Write your report here

  return aresObj




# The three below variables are not used anymore but they will need to be defined
# as some base classes are checking them
# A revamping will be done to remove this
REPORT_NAME = ''
AJAX_CALL = {} # Ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}
