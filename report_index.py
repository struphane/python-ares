""" Report Comment


"""

import os

def report(aresObj, localPath=None):
  """

  """
  id = aresObj.input("Report Name", '')
  reportsPath = r"E:\GitHub\Ares\html"

  # Get the list of all the reports
  foldersReports = []
  for folder in os.listdir(reportsPath):
    if os.path.isdir(r"%s\%s" % (reportsPath, folder)):
      foldersReports.append(folder)
  # Add this list to the auto completion of the input item
  aresObj.item(id).autocomplete(foldersReports)
  aresObj.button("")
  # Create a new report

  return aresObj.html(localPath, title='Select an existing report')