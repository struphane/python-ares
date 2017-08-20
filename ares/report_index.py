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
  aresButton.js('click', 'window.location.href="/reports/page/" + %s; return false;' % aresInput.jsVal())
  modal = aresObj.modal('click on the link to create a new report section')

  aresObj.container('Create Environment', [aresInput, aresButton, modal])

  contentFolder, contentSize = [['Environment', 'Date', 'Size', '']], []
  for folder, folderInfo in aresObj.getFoldersInfo().items():
    iconComp = aresObj.icon('trash')
    iconComp.post('click', "./delete_folder/%s" % folder, {}, 'location.reload();')
    contentFolder.append([folder, folderInfo['LAST_MOD_DT'], folderInfo['SIZE'], iconComp])
    contentSize.append([folder, len(aresObj.getFiles([folder]))])
  # Create a new report

  aresObj.bar('Scripts per folder', [ {"key": "Cumulative Return","values": contentSize }])
  createReport = aresObj.button("Create the Report", 'btn btn-primary')
  inputModal = aresObj.input("Report Name", '')
  aresObj.addTo(modal, inputModal)
  aresObj.addTo(modal, createReport)
  createReport.post('click', "./create/env" , "{'REPORT': %s}" % inputModal.jsVal(), 'display(data);')
  tableComp = aresObj.table('Existing Reports', contentFolder)
  pieComp = aresObj.pieChart('Folders', [['UN', 1], ['DEUX', 2]])
  aresObj.grid([pieComp, tableComp])
  return aresObj