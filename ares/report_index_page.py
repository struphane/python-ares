"""


"""

import os
import time

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
  comp = aresObj.download()
  comp.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': '%s.py' % aresObj.http['SCRIPTS_NAME']})

  fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], aresObj.reportName, '%s.py' % aresObj.http['SCRIPTS_NAME'])))
  fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], aresObj.reportName, '%s.py' % aresObj.http['SCRIPTS_NAME']))))

  displayedScript = {}
  ajxCall =  aresObj.http['SCRIPTS_AJAX'].get('%s.py' % aresObj.http['SCRIPTS_NAME'], [])
  for call in ajxCall:
    displayedScript[call] = True
  scripts = [['Script Name', 'Size', 'Modification Date', 'Parent', 'Ajax', 'download', 'delete'],
             [scriptComp, fileSize, fileDate,  '', ''.join(ajxCall), comp, '']]
  scriptUpdate = fileDate
  displayedScript['%s.py' % aresObj.http['SCRIPTS_NAME']] = True
  for mainScript, child in aresObj.http['SCRIPTS_CHILD']:
    for i, script in enumerate([mainScript, child]):
      if script not in displayedScript:
        remov = aresObj.remove()
        print("##########")
        print(aresObj.http['SCRIPTS_PATH'])
        remov.post('click', "../delete/%s" % aresObj.http['SCRIPTS_NAME'], {'SCRIPT': script}, 'display(data);')
        downComp = aresObj.download()
        downComp.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': script})
        fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], aresObj.http['SCRIPTS'][script], script)))
        fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], aresObj.http['SCRIPTS'][script], script))))
        ajxCall =  aresObj.http['SCRIPTS_AJAX'].get(script, [])
        divComp = aresObj.div(script)
        divComp.toolTip('%s' % os.path.join(aresObj.http['SCRIPTS'].get(script, ''), script))
        for call in ajxCall:
          displayedScript[call] = True
        if i == 1:
          scripts.append([divComp, fileSize, fileDate, mainScript, "".join(ajxCall), downComp, remov])
        else:
          scripts.append([script, fileSize, fileDate, '', "".join(ajxCall), downComp, remov])
        displayedScript[script] = True
        scriptUpdate = fileDate if fileDate > scriptUpdate else scriptUpdate

  for script, scriptPath in aresObj.http['SCRIPTS'].items():
    if script not in displayedScript and script != '__pycache__' and not script.endswith('pyc') and not script.endswith('zip') and not script.endswith('.svn'):
      removComp = aresObj.remove()
      removComp.post('click', "../delete/%s" % aresObj.http['SCRIPTS_NAME'], {'SCRIPT': script}, "display(data); window.location.href='../page/%s' ;" % aresObj.http['SCRIPTS_NAME'])
      downComp = aresObj.download()
      downComp.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': script})
      fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script)))
      fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], scriptPath, script))))
      divComp = aresObj.div(script)
      divComp.toolTip(os.path.join(scriptPath, script))
      scripts.append([divComp, fileSize, fileDate, '', '', downComp, removComp])
      scriptUpdate = fileDate if fileDate > scriptUpdate else scriptUpdate

  aresObj.div('Last update of your environment %s' % scriptUpdate, cssCls='alert alert-success')
  #dropComp = aresObj.dropfile('Drop you files here')
  #dropComp.reportName = aresObj.http['SCRIPTS_NAME']
  graphObj = aresObj.bar([ {"key": "Cumulative Return","values": [["2017-08-17", 15] ] }])
  graphObj.height = 200
  aresObj.table(scripts, cssCls="table table-hover table-bordered")

  zipComp = aresObj.downloadAll()
  zipComp.js('click', "window.location.href='../download/%s/package'" % aresObj.http['SCRIPTS_NAME'])
  return aresObj