


import ExAjaxDataExtract

NAME = 'Reports Data Extract'

def report(aresObj):
  """
  """
  aresObj.title('Report Data Extraction')

  dateObj = aresObj.date('COB Date')
  nodeObj = aresObj.input('Node')
  nameObj = aresObj.input('Name')
  button = aresObj.refresh(" Extract Data", [], 'ExAjaxDataExtract')
  aresObj.setOutput('BasicExtract', "youpi2.txt")
  repo = aresObj.table(aresObj.getOutputFrom("BasicExtract"),
                        [{'key': 'folderPath', 'colName': 'Folder'},
                         {'key': 'file', 'colName': 'File Name'},
                         ],
                        headerBox="Environments")

  button.click('''
                  display(status) ;
                  %s ;
               ''' % repo.jsUpdate())



