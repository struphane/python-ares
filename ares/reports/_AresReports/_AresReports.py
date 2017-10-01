""" Report Comment


"""

import collections
import os

NAME = 'Reports Definition'
DOWNLOAD = None

def report(aresObj):
  """

  """
  aresInput = aresObj.input("Report Name", '')
  reportsPath = aresObj.http.get('DIRECTORY')
  # Get the list of all the reports
  foldersReports, folderEvents = [], {}
  for folder in os.listdir(reportsPath):
    folderEvents[folder] = collections.defaultdict(int)
    folderEvents[folder]['data'] = {}
    if os.path.isdir(os.path.join(reportsPath, folder)):
      foldersReports.append(folder)
      aresLogFile = os.path.join(reportsPath, folder, 'log_ares.dat')
      events = collections.defaultdict(dict)
      # Retrieve all the reports events
      if os.path.exists(aresLogFile):
        log = open(aresLogFile)
        for line in log:
          rec = line.strip().split("#")
          folderEvents[folder][rec[0]] += 1
          folderEvents[folder]['data'][rec[0]] = rec[1]
          folderEvents[folder]['count'] += 1
        log.close()
  # Add this list to the auto completion of the input item
  aresInput.autocomplete(foldersReports)
  aresButton = aresObj.main('Open Report Section', **{'report_name': aresInput, 'cssCls': 'btn btn-success'})
  modal = aresObj.modal('click on the link to create a new report section')
  modal.modal_header = "Set New Environment"
  grid = aresObj.row([aresButton, modal])
  grid.gridCss = None
  aresObj.container('Create Environment', [aresInput, grid])
  content = []
  for folder, folderInfo in aresObj.getFoldersInfo().items():
    if not os.path.exists(os.path.join(aresObj.http['DIRECTORY'], folder, "%s.py" % folder)):
      continue

    name = folder
    with open(os.path.join(aresObj.http['DIRECTORY'], folder, "%s.py" % folder)) as script:
      for line in script:
        if line.startswith("NAME"):
          name = line.split("=")[1].strip().split("#")[0].replace("'", "").replace('"', "")

    iconComp = aresObj.icon('trash')
    iconComp.post('click', "./delete_folder/%s" % folder, {}, 'location.reload();')
    content.append({'folderName': name, 'Date': folderInfo['LAST_MOD_DT'], 'Size': folderInfo['SIZE'],
                    'folderLink': aresObj.anchor(name, **{'report_name': folder, 'cssCls': ''}),
                    # TODO add this page in the bottom right section
                    #'folderLink': aresObj.main(folder, **{'report_name': '_AresReports', 'script_name': 'AresIndexPage', 'user_script': folder}),
                    'FolderFiles': len(aresObj.getFiles([folder])), 'delete': iconComp,
                    'activity': folderEvents[folder]['count'],
                    'creationDate': folderEvents[folder]['data'].get('FOLDER CREATION', '')
                    }
                   )

  # Create a new report # 'Existing Reports',
  tableComp = aresObj.table(content, [{'key': 'folderLink', 'colName': 'Folder Name', 'type': 'object'},
                                      {'key': 'FolderFiles', 'colName': 'Count Files'},
                                      {'key': 'creationDate', 'colName': 'Creation'},
                                      {'key': 'Date', 'colName': 'Last Modification'},
                                      {'key': 'Size', 'colName': 'Size in Ko'},
                                      {'key': 'delete', 'colName': '', 'type': 'object'}], 'Existing Reports')
  tableComp.filters(['Folder Name'])
  barComp = aresObj.bar(content, [{'key': 'folderName', 'colName': 'Folder Name', 'selected': True},
                                  {'key': 'FolderFiles', 'colName': 'Count Files', 'type': 'number', 'selected': True},
                                  {'key': 'Date', 'colName': 'Last Modification'},
                                  {'key': 'Size', 'colName': 'Size in Ko', 'type': 'number'},
                                  {'key': 'activity', 'colName': 'Activity', 'type': 'number'},
                                  {'key': 'delete', 'colName': ''}], 'Scripts per folder')
  inputModal = aresObj.input("Report Name", '')
  #createReport = aresObj.button('Create the Report')
  #createReport.post('click', 'ares.ajaxCreate', **{'report_name': inputModal, 'js': "%s.modal('toggle') ; display(data) ;" % modal.jqId})
  aresObj.addTo(modal, inputModal)
  #aresObj.addTo(modal, createReport)
  pieComp = aresObj.donut(content, [{'key': 'folderName', 'colName': 'Folder Name', 'selected': True},
                                  {'key': 'FolderFiles', 'colName': 'Count Files', 'type': 'number', 'selected': True},
                                  {'key': 'Date', 'colName': 'Last Modification'},
                                  {'key': 'Size', 'colName': 'Size in Ko', 'type': 'number'},
                                  {'key': 'activity', 'colName': 'Activity', 'type': 'number'},
                                  {'key': 'delete', 'colName': ''}], 'Folder')
  aresObj.row([barComp, pieComp])
  aresObj.meter(0.60)