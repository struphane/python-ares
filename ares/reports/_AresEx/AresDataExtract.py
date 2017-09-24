


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
  repo = aresObj.table(aresObj.getOutputFrom("BasicExtract"),
                        [{'key': 'folderPath', 'colName': 'Folder'},
                         {'key': 'file', 'colName': 'File Name'},
                         {'key': 'LAST_MOD_DT', 'colName': 'Last Modification'},
                         {'key': 'SIZE', 'colName': 'File Size'},
                         ],
                        headerBox="Environments")

  button.click('''
                  display(status) ;
                  %s ;
               ''' % repo.jsUpdate(), {'youpi': 'RRR', 'node': nodeObj, 'name': nameObj, 'cob': dateObj})



