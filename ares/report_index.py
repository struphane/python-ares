""" Report Comment


"""

import os

def report(aresObj):
  """

  """

  aresObj.title('Reports Environment (Beta)')
  aresInput = aresObj.input("Report Name", '')
  reportsPath = aresObj.http.get('USER_PATH')
  # Get the list of all the reports
  foldersReports = []
  for folder in os.listdir(reportsPath):
    if os.path.isdir(os.path.join(reportsPath, folder)):
      foldersReports.append(folder)
  # Add this list to the auto completion of the input item
  aresInput.autocomplete(foldersReports)
  aresButton = aresObj.button("Open Report Section", 'btn btn-success')
  aresButton.js('click', 'window.location.href="/reports/page/" + %s; return false;' % aresInput.val)
  modal = aresObj.modal('click on the link to create a new report section')
  grid = aresObj.row([aresButton, modal])
  grid.gridCss = None
  aresObj.container('Create Environment', [aresInput, grid])

  content = []
  for folder, folderInfo in aresObj.getFoldersInfo().items():
    iconComp = aresObj.icon('trash')
    iconComp.post('click', "./delete_folder/%s" % folder, {}, 'location.reload();')
    content.append({'folderName': folder, 'Date': folderInfo['LAST_MOD_DT'], 'Size': folderInfo['SIZE'],
                    'FolderFiles': len(aresObj.getFiles([folder])), 'delete': iconComp})

  # Create a new report
  tableComp = aresObj.table('Existing Reports', content, {'folderName': 'Folder Name', 'FolderFiles': 'Count Files',
                                                          'Date': 'Last Modification', 'Size': 'Size in Ko', 'delete': ''})
  barComp = aresObj.bar('Scripts per folder', content, {'folderName': 'Folder Name', 'FolderFiles': 'Count Files'},
                        (['Folder Name'], ['Count Files']))
  barComp.linkTo(tableComp)
  createReport = aresObj.button("Create the Report", 'btn btn-primary')
  inputModal = aresObj.input("Report Name", '')
  aresObj.addTo(modal, inputModal)
  aresObj.addTo(modal, createReport)
  createReport.post('click', "./create/env" , "{'REPORT': %s}" % inputModal.val, 'display(data);')
  pieComp = aresObj.pieChart('Folders', content, {'folderName': 'Folder Name', 'FolderFiles': 'Count Files'},
                            (['Folder Name'], ['Count Files']))
  pieComp.linkTo(tableComp)
  #tableComp.jsLinkTo([barComp, pieComp])
  aresObj.row([pieComp, tableComp])
  return aresObj