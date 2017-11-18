""" Report Comment


"""

import collections
import os

NAME = 'Reports Definition'
DOWNLOAD = None

def report(aresObj):
  """

  """
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
  content = []
  for folder, folderInfo in aresObj.getFoldersInfo().items():
    if not os.path.exists(os.path.join(aresObj.http['DIRECTORY'], folder, "%s.py" % folder)):
      continue

    name = folder
    with open(os.path.join(aresObj.http['DIRECTORY'], folder, "%s.py" % folder)) as script:
      for line in script:
        if line.startswith("NAME"):
          name = line.split("=")[1].strip().split("#")[0].replace("'", "").replace('"', "")

    content.append({'report_name': name, 'Date': folderInfo['LAST_MOD_DT'], 'Size': float(folderInfo['SIZE'].split(" ")[0]),
                    'FolderName': folder, 'Day': folderInfo['LAST_MOD_DT'].split(" ")[0], #'folderLink': aresObj.internalLink(name, folder, attrs={'REPORT_NAME': folder}, cssCls=[]),
                    'FolderFiles': len(aresObj.getFiles([folder])), 'activity': folderEvents[folder]['count'],
                    'show_params': '1',
                    'creationDate': folderEvents[folder]['data'].get('FOLDER CREATION', '')})

  # Create a new report # 'Existing Reports',
  tableComp = aresObj.table(content, [{'key': 'FolderName', 'colName': 'Folder Name'},
                                      {'key': 'show_params', 'colName': 'Show Params', 'visible': 'false'},
                                      {'key': 'report_name', 'colName': 'Folder Name', 'url': {'cols': ['report_name', 'FolderName', 'show_params']}},
                                      {'key': 'FolderFiles', 'colName': 'Count Files'},
                                      {'key': 'creationDate', 'colName': 'Creation'},
                                      {'key': 'Date', 'colName': 'Last Modification'},
                                      {'key': 'Size', 'colName': 'Size in Ko'}], 'Existing Reports')

  #tableComp.filters(['Folder Name'])
  bar = aresObj.bar(content, [{'key': 'report_name', 'colName': 'Folder Name'},
                              {'key': 'Day', 'colName': 'Last Modification'},
                              {'key': 'FolderFiles', 'colName': 'Count Files', 'type': 'number'},
                              {'key': 'Date', 'colName': 'Last Modification'},
                              {'key': 'Size', 'colName': 'Size in Ko', 'type': 'number'},
                              {'key': 'activity', 'colName': 'Activity', 'type': 'number'},
                              {'key': 'delete', 'colName': ''}], 'Scripts per folder')

  #
  bar.setKeys(['Day'])
  bar.setVals(['Size'])

  donut = aresObj.donut(content, [{'key': 'report_name', 'colName': 'Folder Name', 'selected': True},
                                  {'key': 'FolderFiles', 'colName': 'Count Files', 'type': 'number', 'selected': True},
                                  {'key': 'Date', 'colName': 'Last Modification'},
                                  {'key': 'Size', 'colName': 'Size in Ko', 'type': 'number'},
                                  {'key': 'activity', 'colName': 'Activity', 'type': 'number'},
                                  {'key': 'delete', 'colName': ''}], 'Folder')

  donut.setKeys(['report_name'])
  donut.setVals(['activity'])

  aresObj.row([bar, donut])
