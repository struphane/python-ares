""" Internal Report to display the list of available reports

This Environment will be based on the same structure that the user reports.
The only difference if the fact that they will start with an underscore.

This is to simplify a lot the report.py entries (to make sure that all the entries are generic
but also to guarantee the fact that the system reports will be based on shared components.

The target would be to try to avoid generic features that users will ask for going forward
"""

import os
import time
import collections
import six

from ares.Lib import Ares

NAME = 'Report Environment'

def report(aresObj):
  """
  Run the report

  """
  aresObj.title('%s - ReportEnvironment' % aresObj.http['USER_SCRIPT'])
  aresObj.newline()
  aresObj.title3('Report Description')
  aresObj.paragraph('''
                    The below section display the documentation defined in your main script at the top of it.
                    Please do not hesitate to update this section as it might be useful to understand the purpose of you
                    what if environment.
                    ''')
  directory = os.path.join(aresObj.http['DIRECTORY'], aresObj.http['USER_SCRIPT'])
  #aresObj.code(aresObj.http['SCRIPTS_DSC'])
  aresObj.title3('Python Scripts')
  aresObj.paragraph('''
                      Python scripts cannot be updated from this from end. Please download the package to get your environment.
                      The package will give you the last version of the scripts and also the tool in order to upload new python scripts.
                      Any script can be updated in your environment / any folder can be added.
                      Please go here to get more details about the process
                    ''')
  header = [{'key': 'script_name', 'colName': 'Script Name', 'type': 'object'},
            {'key': 'size', 'colName': 'Size'},
            {'key': 'lst_mod_dt', 'colName': 'Modification Date'},
            {'key': 'download', 'colName': 'Download', 'type': 'object'},
            {'key': 'delete', 'colName': 'Delete', 'type': 'object'}]

  recordSet, scriptUpdate = [], None
  for script in os.listdir(directory):
    if not script.endswith(".py"):
      continue

    downComp = aresObj.anchor_download('', **{'report_name': aresObj.http['USER_SCRIPT'], 'script': script})
    fileSize = Ares.convert_bytes(os.path.getsize(os.path.join(directory, script)))
    fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(directory, script))))
    if script == "%s.py" % aresObj.http['USER_SCRIPT']:
      hyperLink = aresObj.anchor('%s.py' % aresObj.http['USER_SCRIPT'], **{'report_name': aresObj.http['USER_SCRIPT'], 'cssCls': ''})
      row = {'script': script, 'script_name': hyperLink, 'size': fileSize, 'lst_mod_dt': fileDate, 'download': downComp, 'delete': ''}
    else:
      remov = aresObj.icon('trash')
      remov.post('click', "../delete/%s" % aresObj.http['USER_SCRIPT'], {'SCRIPT': script}, 'display(data);')
      divComp = aresObj.div(script)
      divComp.toolTip(script)
      row = {'script': script, 'script_name': divComp, 'size': fileSize, 'lst_mod_dt': fileDate, 'download': downComp, 'delete': remov}
    recordSet.append(row)
    scriptUpdate = fileDate if scriptUpdate is None or fileDate > scriptUpdate else scriptUpdate

  ajaxRecordSet = []
  for script in os.listdir(os.path.join(directory, 'ajax')):
    if not script.endswith(".py") or script == '__init__.py':
      continue

    downComp = aresObj.anchor_download('', **{'report_name': aresObj.http['USER_SCRIPT'], 'script': "ajax&%s" % script})
    fileSize = Ares.convert_bytes(os.path.getsize(os.path.join(directory, 'ajax', script)))
    fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(directory, 'ajax', script))))
    ajaxRecordSet.append({'script': script, 'script_name': script, 'size': fileSize, 'lst_mod_dt': fileDate, 'download': downComp, 'delete': remov})

  aresLogFile = os.path.join(directory, 'log_ares.dat')
  folderEvents = collections.defaultdict(int)
  if os.path.exists(aresLogFile):
    log = open(aresLogFile, "r")
    for line in log:
      row = line.strip().split("#")
      folderEvents[row[1]] += 1
    log.close()

  aresObj.div('Last update of your environment %s' % scriptUpdate, cssCls='alert alert-success')

  modal = aresObj.modal('Add a script')
  modal.modal_header = 'Create new script'
  inputModal = aresObj.input("Script Name", '')
  selectReport = aresObj.select(["Report", "Python Service", "Javascript", "Configuration"], selected="Report")
  createReport = aresObj.button("Add", "")
  #createReport.('Add', **{'script': inputModal, 'report_name': aresObj.http['SCRIPTS_NAME'], 'script_type': selectReport})
  aresObj.addTo(modal, inputModal)
  aresObj.addTo(modal, selectReport)
  aresObj.addTo(modal, createReport)
  aresObj.newline()
  aresObj.newline()

  activity = collections.defaultdict(int)
  inFile = aresObj.readFile('log_ares.dat')
  if inFile is not None:
    six.next(inFile)
    for line in inFile:
      splitLine = line.strip().split("#")
      activity[splitLine[1]] += 1
    inFile.close()
  content = []
  for k in sorted(activity.keys()):
    content.append([k, activity[k]])

  aresObj.table(recordSet, header, 'Report Summary', cssCls="table table-hover table-bordered")
  aresObj.table(ajaxRecordSet, header, 'Python Service Summary', cssCls="table table-hover table-bordered")

  eventRecordSet = []
  for dt, eventCount in folderEvents.items():
    eventRecordSet.append({'date': dt, 'count': eventCount})

  aresObj.bar(eventRecordSet,
              [{'key': 'date', 'colName': 'Date'},
               {'key': 'count', 'colName': 'Events', 'selected': True, 'type': 'number'}]
              , 'Activity History'
              )

  graphObj = aresObj.bar(recordSet,
                          [{'key': 'script', 'colName': 'Script Name', 'type': 'object'},
                           {'key': 'size', 'colName': 'Size', 'selected': True, 'type': 'number'},
                           {'key': 'lst_mod_dt', 'colName': 'Modification Date', 'selected': True}], 'Activity Dates')

  pieObj = aresObj.pie(recordSet,
                       [{'key': 'script', 'colName': 'Script Name', 'type': 'object', 'selected': True},
                        {'key': 'size', 'colName': 'Size', 'selected': True, 'type': 'number'},
                        {'key': 'lst_mod_dt', 'colName': 'Modification Date'}], 'Files Size')

  aresObj.row([graphObj, pieObj])
  zipComp = aresObj.downloadAll('Download Zip archive of this environment')
  zipComp.js('click', "window.location.href='../download/%s/package'" % aresObj.http['USER_SCRIPT'])