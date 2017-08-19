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


  aresObj.container('Create Environment', [aresInput, aresButton])

  # Create a new report
  modal = aresObj.modal('click on the link to create a new report section')
  createReport = aresObj.button("Create the Report", 'btn btn-primary')
  inputModal = aresObj.input("Report Name", '')
  aresObj.addTo(modal, inputModal)
  aresObj.addTo(modal, createReport)
  tableComp = aresObj.table('Existing Reports', [['Test', 'fdsf'], ['Test', 'fdsf']])
  createReport.post('click', "./create/env" , "{'REPORT': %s}" % inputModal.jsVal(), 'display(data);')

  print(aresObj.getFolders())
  pieComp = aresObj.pieChart('Folders', [['UN', 1], ['DEUX', 2]])
  aresObj.grid([pieComp, tableComp])
  return aresObj