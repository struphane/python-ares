"""


"""

import os
import time
import collections
import six

from ares.Lib import Ares

def report(aresObj, localPath=None):
  """
  Run the report

  """
  aresObj.title('%s - ReportEnvironment' % aresObj.http['SCRIPTS_NAME'])
  aresObj.newline()
  aresObj.title3('Report Description')
  aresObj.paragraph('''
                    The below section display the documentation defined in your main script at the top of it.
                    Please do not hesitate to update this section as it might be useful to understand the purpose of you
                    what if environment.
                    ''')
  aresObj.code(aresObj.http['SCRIPTS_DSC'])
  scriptComp = aresObj.anchor('%s.py' % aresObj.http['SCRIPTS_NAME'], **{'report_name': aresObj.http['SCRIPTS_NAME'], 'cssCls': ''})
  aresObj.title3('Python Scripts')
  aresObj.paragraph('''
                      Python scripts cannot be updated from this from end. Please download the package to get your environment.
                      The package will give you the last version of the scripts and also the tool in order to upload new python scripts.
                      Any script can be updated in your environment / any folder can be added.
                      Please go here to get more details about the process
                    ''')
  downComp = aresObj.anchor_download('', **{'report_name': aresObj.http['SCRIPTS_NAME'], 'script': '%s.py' % aresObj.http['SCRIPTS_NAME']})
  fileSize = Ares.convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], aresObj.http['REPORT_NAME'], '%s.py' % aresObj.http['SCRIPTS_NAME'])))
  fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], aresObj.http['REPORT_NAME'], '%s.py' % aresObj.http['SCRIPTS_NAME']))))
  displayedScript = {}
  ajxCall =  aresObj.http['SCRIPTS_AJAX'].get('%s.py' % aresObj.http['SCRIPTS_NAME'], [])
  for call in ajxCall:
    displayedScript[call] = True
  header = [{'key': 'script_name', 'colName': 'Script Name', 'type': 'object'},
            {'key': 'size', 'colName': 'Size'},
            {'key': 'lst_mod_dt', 'colName': 'Modification Date'},
            {'key': 'ajax', 'colName': 'Ajax'},
            {'key': 'download', 'colName': 'Download', 'type': 'object'},
            {'key': 'delete', 'colName': 'Delete', 'type': 'object'}]

  recordSet = []
  recordSet.append({'script': '%s.py' % aresObj.http['SCRIPTS_NAME'], 'script_name': scriptComp, 'size': fileSize,
                    'lst_mod_dt': fileDate, 'ajax': ''.join(ajxCall), 'download': downComp, 'delete': '', 'parent': ''})
  scriptUpdate = fileDate
  displayedScript['%s.py' % aresObj.http['SCRIPTS_NAME']] = True
  for mainScript, child in aresObj.http['SCRIPTS_CHILD']:
    for i, script in enumerate([mainScript, child]):
      if script not in displayedScript:
        remov = aresObj.icon('trash')
        scriptPath = aresObj.http['SCRIPTS'][script]
        scriptLink = scriptPath.replace(aresObj.http['SCRIPTS_NAME'], "")
        remov.post('click', "../delete/%s" % aresObj.http['SCRIPTS_NAME'], {'SCRIPT': script}, 'display(data);')
        downComp = aresObj.anchor_download('', **{'report_name': aresObj.http['SCRIPTS_NAME'], 'script': "%s&%s" % (scriptLink, script)})
        fileSize = Ares.convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script)))
        fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script))))
        ajxCall =  aresObj.http['SCRIPTS_AJAX'].get(script, [])
        divComp = aresObj.div(script)
        divComp.toolTip('%s' % os.path.join(aresObj.http['SCRIPTS'].get(script, ''), script))
        for call in ajxCall:
          displayedScript[call] = True
        if i == 1:
          row = {'script': script, 'script_name': divComp, 'size': fileSize, 'lst_mod_dt': fileDate, 'ajax': ''.join(ajxCall), 'download': downComp, 'delete': remov}
        else:
          row = {'script': script, 'script_name': script, 'size': fileSize, 'lst_mod_dt': fileDate, 'ajax': ''.join(ajxCall), 'download': downComp, 'delete': remov}
        recordSet.append(row)
        displayedScript[script] = True
        scriptUpdate = fileDate if fileDate > scriptUpdate else scriptUpdate

  for script, scriptPath in aresObj.http['SCRIPTS'].items():
    if script not in displayedScript and script != '__pycache__' and not script.endswith('pyc') and not script.endswith('zip') and not script.endswith('.svn'):
      removComp = aresObj.icon('trash')
      scriptLink = scriptPath.replace(aresObj.http['SCRIPTS_NAME'], "")
      removComp.post('click', "../delete/%s" % aresObj.http['SCRIPTS_NAME'], {'SCRIPT': script}, "display(data); window.location.href='../page/%s' ;" % aresObj.http['SCRIPTS_NAME'])
      downComp = aresObj.anchor_download('', **{'report_name': aresObj.http['SCRIPTS_NAME'], 'script': "%s&%s" % (scriptLink, script)})
      fileSize = Ares.convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script)))
      fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script))))
      divComp = aresObj.div(script)
      divComp.toolTip(os.path.join(scriptPath, script))
      recordSet.append({'script': script, 'script_name': divComp, 'size': fileSize, 'lst_mod_dt': fileDate, 'ajax': '', 'download': downComp, 'delete': removComp})
      scriptUpdate = fileDate if fileDate > scriptUpdate else scriptUpdate

  aresLogFile = os.path.join(aresObj.http['DIRECTORY'], 'log_ares.dat')
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
  selectReport = aresObj.select(["Report", "Python Service", "Javascript"], selected="Report")
  createReport = aresObj.anchor_add_scripts('Add', **{'script': inputModal, 'report_name': aresObj.http['SCRIPTS_NAME'], 'script_type': selectReport})
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

  tableComp = aresObj.table(recordSet, header, 'Scripts Summary', cssCls="table table-hover table-bordered")
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
  zipComp.js('click', "window.location.href='../download/%s/package'" % aresObj.http['SCRIPTS_NAME'])