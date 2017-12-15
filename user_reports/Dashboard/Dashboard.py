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


NAME = 'Dashbord Example' # The Report Name in the left menu
# The Shortcuts should be defined as below
# [(Cateogry Name, [List of the script in the root directory])]
# It is only possible to create new links for scripts in the root
SHORTCUTS = [('', [('Portfolio', 'ViewPtf'),('Group', 'ViewGrp'),('Counterparty', 'ViewCpty')])] # All the possible link to other pages
FILE_CONFIGS = [] # All the static and output files configurationa
# The format in the above list should be as: {'filename': 'data.txt', 'folder': 'outputs', 'parser': InFilePricesConfig.InFilePices},

HTTP_PARAMS = [] # If you want to use the param method to set parameter before running hte report


#def params(aresObj):
#  """ Optional param method to be run before the report method to set parameter """


def report(aresObj):
  '''
  Write your function below
  '''
  aresObj.title("Consolidated View")
  # Example of DropDown selection
  #   - parameter 1: the title to be displayed in the object
  #   - parameter 2: the content of the dropdown (the items should be tuple (Name, hyperlink)

