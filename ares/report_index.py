""" Report Comment


"""

import os

def report(aresObj, localPath=None):
  """

  """

  aresObj.title(1, 'Reports Environment (Beta)')
  id = aresObj.input("Report Name", '')
  reportsPath = aresObj.http.get('USER_PATH')
  if localPath is not None:
    reportsPath = r"%s\html"
  # Get the list of all the reports
  foldersReports = []
  for folder in os.listdir(reportsPath):
    if os.path.isdir(os.path.join(reportsPath, folder)):
      foldersReports.append(folder)
  # Add this list to the auto completion of the input item
  aresObj.item(id).autocomplete(foldersReports)
  bId = aresObj.button("Open Report Section", 'btn-success')
  aresObj.item(bId).js('click', 'window.location.href="/reports/page/" + %s; return false;' % aresObj.item(id).jsVal())

  # Create a new report
  modalId = aresObj.modal('click on the link to create a new report section')
  modalAres = aresObj.item(modalId).aresObj
  iReportName = modalAres.input("Report Name", '')
  bModal = modalAres.button("Create the Report", 'btn-primary')
  modalAres.item(bModal).jsAjax('click', 'alert(data);location.href = "../reports/index";',
                                'report_index_set.py', localPath, {'report': modalAres.item(iReportName).jsVal(),
                                                                   'serverPath': '"%s"' % localPath}, url='reports/create')
 #create
  return aresObj