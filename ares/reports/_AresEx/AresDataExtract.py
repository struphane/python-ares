


import ExAjaxDataExtract

NAME = 'Reports Data Extract'
DOWNLOAD = 'SCRIPT'

def report(aresObj):
  """
  """
  aresObj.title('Report Data Extraction')

  dateObj = aresObj.date('COB Date')
  nodeObj = aresObj.input('Node')
  button = aresObj.refresh(" Extract Data", [], 'ExAjaxDataExtract')
  repo = aresObj.table(aresObj.listDataFrom("BasicExtract"),
                        [{'key': 'folderPath', 'colName': 'Folder'},
                         {'key': 'file', 'colName': 'File Name'},
                         {'key': 'LAST_MOD_DT', 'colName': 'Last Modification'},
                         {'key': 'SIZE', 'colName': 'File Size'},
                         ],
                        headerBox="Environments")

  repo.filters(['File Name', 'Last Modification'])
  button.click('''
                  display(status) ;
                  %s ;
               ''' % repo.jsUpdate(), {'youpi': 'RRR', 'node': nodeObj, 'cob': dateObj})



