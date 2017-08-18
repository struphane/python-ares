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
  aresObj.title("This is my first report !!!")
  uploadComp = aresObj.upload()
  # We need to use ../ to call the main upload service from the user_report folder
  uploadComp.post('click', '../upload/%s' % aresObj.http['REPORT_NAME'], {}, "display(data) ;", 'data/209')
  content = [['File Name', 'Size', 'Last Update']]
  for file in aresObj.getFiles(['data', '209']):
    fileData = aresObj.getFileInfo(['data', '209'], file)
    content.append([file, fileData['SIZE'], fileData['LAST_MOD_DT']])
  aresObj.table(content)

  return aresObj