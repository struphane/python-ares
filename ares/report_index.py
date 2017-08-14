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
  aresObj.addNotification('Success', 'GOOD', 'something wrong happened')
  aresObj.addNotification('Info', 'HEY', 'something wrong happened')
  aresObj.addNotification('Warning', 'ATTENTION', 'something wrong happened')
  # aresObj.addNotification('Danger', 'NO VALUE', 'something wrong happened')
  # Create a new report
  modal = aresObj.modal('click on the link to create a new report section')
  aresObj.addTo(modal, aresObj.input("Report Name", ''))
  aresObj.addTo(modal, aresObj.button("Create the Report", 'btn btn-primary'))
  #modalAres.item(bModal).jsAjax('click', 'alert(data);location.href = "../reports/index";',
  #                              'report_index_set.py', localPath, {'report': modalAres.item(iReportName).jsVal(),
  #                                                                 'serverPath': '"%s"' % localPath}, url='reports/create')
  return aresObj