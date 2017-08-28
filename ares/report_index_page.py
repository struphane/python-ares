"""


"""

import os
import time
import collections
import six

AJAX_CALL = {
  'download': 'MyRepotTestAjax.py'
  }

CHILD_PAGES = {
	'report': 'MyRepotTestChild2.py',
  'test3': 'MyRepotTestChild3.py',
  }

def convert_bytes(num):
  """
  this function will convert bytes to MB.... GB... etc
  """
  for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
      if num < 1024.0:
          return "%3.1f %s" % (num, x)
      num /= 1024.0

def report(aresObj, localPath=None):
  """ Run the report """
  aresObj.title('%s - ReportEnvironment' % aresObj.http['SCRIPTS_NAME'])
  aresObj.newline()
  aresObj.title3('Report Description')
  aresObj.paragraph('''
                    The below section display the documentation defined in your main script at the top of it.
                    Please do not hesitate to update this section as it might be useful to understand the purpose of you
                    what if environment.
                    ''')
  aresObj.code(aresObj.http['SCRIPTS_DSC'])

  CHILD_PAGES['report'] = "../../run/%s" % aresObj.http['SCRIPTS_NAME']
  scriptComp = aresObj.anchor('%s.py' % aresObj.http['SCRIPTS_NAME'])
  scriptComp.preload('click')
  scriptComp.addLink('report', dots='.')
  aresObj.title3('Python Scripts')
  aresObj.paragraph('''
                      Python scripts cannot be updated from this from end. Please download the package to get your environment.
                      The package will give you the last version of the scripts and also the tool in order to upload new python scripts.
                      Any script can be updated in your environment / any folder can be added.
                      Please go here to get more details about the process
                    ''')
  comp = aresObj.icon('download')
  comp.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': '%s.py' % aresObj.http['SCRIPTS_NAME']})

  fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], aresObj.reportName, '%s.py' % aresObj.http['SCRIPTS_NAME'])))
  fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], aresObj.reportName, '%s.py' % aresObj.http['SCRIPTS_NAME']))))

  displayedScript = {}
  ajxCall =  aresObj.http['SCRIPTS_AJAX'].get('%s.py' % aresObj.http['SCRIPTS_NAME'], [])
  for call in ajxCall:
    displayedScript[call] = True
  hearder = ['Script Name', 'Size', 'Modification Date', 'Parent', 'Ajax', 'download', 'delete']
  recordSet = []
  recordSet.append(dict(zip(hearder, [scriptComp, fileSize, fileDate,  '', ''.join(ajxCall), comp, ''])))
  scriptUpdate = fileDate
  displayedScript['%s.py' % aresObj.http['SCRIPTS_NAME']] = True
  for mainScript, child in aresObj.http['SCRIPTS_CHILD']:
    for i, script in enumerate([mainScript, child]):
      if script not in displayedScript:
        remov = aresObj.icon('trash')
        scriptPath = aresObj.http['SCRIPTS'][script]
        scriptLink = scriptPath.replace(aresObj.http['SCRIPTS_NAME'], "")
        remov.post('click', "../delete/%s" % aresObj.http['SCRIPTS_NAME'], {'SCRIPT': script}, 'display(data);')
        downComp = aresObj.icon('download')
        downComp.js('click', "window.location.href='../download/%(report_name)s/%(script)s' ;" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': "%s&%s" % (scriptLink, script)})
        fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script)))
        fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script))))
        ajxCall =  aresObj.http['SCRIPTS_AJAX'].get(script, [])
        divComp = aresObj.div(script)
        divComp.toolTip('%s' % os.path.join(aresObj.http['SCRIPTS'].get(script, ''), script))
        for call in ajxCall:
          displayedScript[call] = True
        if i == 1:
          row = [divComp, fileSize, fileDate, mainScript, "".join(ajxCall), downComp, remov]
        else:
          row = [script, fileSize, fileDate, '', "".join(ajxCall), downComp, remov]
        recordSet.append(dict(zip(hearder, row)))
        displayedScript[script] = True
        scriptUpdate = fileDate if fileDate > scriptUpdate else scriptUpdate

  for script, scriptPath in aresObj.http['SCRIPTS'].items():
    if script not in displayedScript and script != '__pycache__' and not script.endswith('pyc') and not script.endswith('zip') and not script.endswith('.svn'):
      removComp = aresObj.icon('trash')
      scriptLink = scriptPath.replace(aresObj.http['SCRIPTS_NAME'], "")
      removComp.post('click', "../delete/%s" % aresObj.http['SCRIPTS_NAME'], {'SCRIPT': script}, "display(data); window.location.href='../page/%s' ;" % aresObj.http['SCRIPTS_NAME'])
      downComp = aresObj.icon('download')
      downComp.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': "%s&%s" % (scriptLink, script)})
      fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script)))
      fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script))))
      divComp = aresObj.div(script)
      divComp.toolTip(os.path.join(scriptPath, script))
      recordSet.append(dict(zip(hearder, [divComp, fileSize, fileDate, '', '', downComp, removComp])))
      scriptUpdate = fileDate if fileDate > scriptUpdate else scriptUpdate

  aresObj.div('Last update of your environment %s' % scriptUpdate, cssCls='alert alert-success')
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
  tableComp = aresObj.table('Scripts Summary', recordSet,
                            dict(zip(['Script Name', 'Size', 'Modification Date', 'Parent', 'Ajax', 'download', 'delete'],
                                     ['Script Name', 'Size', 'Modification Date', 'Parent', 'Ajax', 'download',
                                      'delete'])),
                            cssCls="table table-hover table-bordered")
  graphObj = aresObj.bar('Deployments count', recordSet,
                         dict(zip(['Script Name', 'Size', 'Modification Date', 'Parent', 'Ajax', 'download', 'delete'],
                                  ['Script Name', 'Size', 'Modification Date', 'Parent', 'Ajax', 'download',
                                   'delete'])),
                         (['Script Name'], ['Size']))

  graphObj.linkTo(tableComp)
  graphObj.height = 200

  zipComp = aresObj.downloadAll('Download Zip archive of this environment')
  zipComp.js('click', "window.location.href='../download/%s/package'" % aresObj.http['SCRIPTS_NAME'])
  return aresObj