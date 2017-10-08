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
  '''
  Write your function below
  '''

  # Example of DropDown selection
  #   - parameter 1: the title to be displayed in the object
  #   - parameter 2: the content of the dropdown (the items should be tuple (Name, hyperlink)
  dropdown = aresObj.dropdown('Test', [('link 1', None),
                                       ('Other', [('link 2', None),
                                                 ('link 3', [('link 4', None)] )])
                                                 ])
  # To disable some links
  dropdown.disable('link 1', None)
  # Because the hyperlink are not defined a click has to be defined to define the action
  dropdown.click(None)

  # Example of a Radio select HTML object
  #   - parameter 1: the key in the recordSet to be used to define the range of values
  #   - parameter 2: the recordset (a list of dictionaries)
  #   - parameter 3: the header definition of the recordset
  radio = aresObj.radio('CCY', [{'CCY': 'EUR'}, {'CCY': 'HUF'}, {'CCY': 'USD'}],
                        [{'key': 'PTF', 'colName': 'Portfolio'},
                         {'key': 'CCY', 'colName': 'Currency'},
                         {'key': 'VAL2', 'colName': 'Value 2'},
                         {'key': 'VAL3', 'colName': 'Value 3'}])

  radio.select('EUR')
  radio.click(None)



# The three below variables are not used anymore but they will need to be defined
# as some base classes are checking them
# A revamping will be done to remove this
REPORT_NAME = ''
AJAX_CALL = {} # Ajax call definition
CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}
