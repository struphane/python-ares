""" Report Comment


"""

import os

def report(aresObj, localPath=None):
  """

  """

  aresObj.title(1, 'Reports Environment (Beta)')
  id = aresObj.input("Report Name", '')
  reportsPath = r"%s\user_reports" % aresObj.http.get('ROOT_PATH')
  if localPath is not None:
    reportsPath = r".\html"
  # Get the list of all the reports
  foldersReports = []
  for folder in os.listdir(reportsPath):
    if os.path.isdir(r"%s\%s" % (reportsPath, folder)):
      foldersReports.append(folder)
  # Add this list to the auto completion of the input item
  aresObj.item(id).autocomplete(foldersReports)
  bId = aresObj.button("Open Report Section", 'btn-success')
  aresObj.item(bId).js('click', 'window.location.href="/reports/page/" + %s; return false;' % aresObj.item(id).jsVal())
  aresObj.addNotification('Success', 'GOOD', 'something wrong happened')
  aresObj.addNotification('Info', 'HEY', 'something wrong happened')
  aresObj.addNotification('Warning', 'ATTNENTION', 'something wrong happened')
  # aresObj.addNotification('Danger', 'NO VALUE', 'something wrong happened')
  # Create a new report
  modalId = aresObj.modal('click on the link to create a new report section')
  modalAres = aresObj.item(modalId).aresObj
  iReportName = modalAres.input("Report Name", '')
  bModal = modalAres.button("Create the Report", 'btn-primary')
  modalAres.item(bModal).jsAjax('click', 'alert(data) ; ',
                                'report_index_set.py', localPath, {'report': modalAres.item(iReportName).jsVal(),
                                                                   'serverPath': '"%s"' % localPath})

  return aresObj