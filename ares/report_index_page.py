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
  aresObj.title(1, '%s - ReportEnvironment' % aresObj.http['SCRIPTS_NAME'])
  aresObj.title(2, 'Report Description')
  aresObj.code(aresObj.http['SCRIPTS_DSC'])

  CHILD_PAGES['report'] = "../run/%s" % aresObj.http['SCRIPTS_NAME']
  aId = aresObj.anchor('%s.py' % aresObj.http['SCRIPTS_NAME'], aresObj.http['FILE'], 'report', CHILD_PAGES, localPath)
  aresObj.title(2, 'List des scripts')
  dId = aresObj.download()
  aresObj.item(dId).js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': '%s.py' % aresObj.http['SCRIPTS_NAME']})

  fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], '%s.py' % aresObj.http['SCRIPTS_NAME'])))
  fileDate = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], '%s.py' % aresObj.http['SCRIPTS_NAME']))))

  displayedScript = {}
  ajxCall =  aresObj.http['SCRIPTS_AJAX'].get('%s.py' % aresObj.http['SCRIPTS_NAME'], [])
  for call in ajxCall:
    displayedScript[call] = True
  scripts = [(aresObj.item(aId), fileSize, fileDate,  '', aresObj.newLine.join(ajxCall), aresObj.item(dId), '')]
  displayedScript['%s.py' % aresObj.http['SCRIPTS_NAME']] = True
  for mainScript, child in aresObj.http['SCRIPTS_CHILD']:
    for i, script in enumerate([mainScript, child]):
      if script not in displayedScript:
        bId = aresObj.remove()
        aresObj.item(bId).jsAjax('click', 'location.href = "/reports/page/%s";' % aresObj.http['SCRIPTS_NAME'], aresObj.http['SCRIPTS_NAME'], localPath, data={'SCRIPT': script}, url=None)
        dId = aresObj.download()
        aresObj.item(dId).js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': script})
        fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], script)))
        fileDate = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], script))))
        aresObj.item(bId).jsAjax('click', 'location.href = "/reports/page/%s";' % aresObj.http['SCRIPTS_NAME'], aresObj.http['SCRIPTS_NAME'], localPath, {'SCRIPT': "'%s'" % script})
        ajxCall =  aresObj.http['SCRIPTS_AJAX'].get(script, [])
        for call in ajxCall:
          displayedScript[call] = True
        if i == 1:
          scripts.append((script, fileSize, fileDate, mainScript, aresObj.newLine.join(ajxCall), aresObj.item(dId), aresObj.item(bId)))
        else:
          scripts.append((script, fileSize, fileDate, '', aresObj.newLine.join(ajxCall), aresObj.item(dId), aresObj.item(bId)))
        displayedScript[script] = True

  for script in aresObj.http['SCRIPTS']:
    if script not in displayedScript and script != '__pycache__' and not script.endswith('pyc'):
      bId = aresObj.remove()
      aresObj.item(bId).jsAjax('click', 'location.href = "/reports/page/%s";' % aresObj.http['SCRIPTS_NAME'], aresObj.http['SCRIPTS_NAME'], localPath, data={'SCRIPT': script}, url=None)
      dId = aresObj.download()
      aresObj.item(dId).js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['SCRIPTS_NAME'], 'script': script})
      fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], script)))
      fileDate = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], script))))
      tid = aresObj.div(script)
      aresObj.item(tid).toolTip('Script not correctly linked')
      scripts.append((aresObj.item(tid), fileSize, fileDate, '', '', aresObj.item(dId), aresObj.item(bId)))

  dropId = aresObj.dropFile()
  aresObj.item(dropId).reportName = aresObj.http['SCRIPTS_NAME']
  aresObj.nestedtable(['Script Name', 'Size', 'Modification Date', 'Parent', 'Ajax', 'download', 'delete'], scripts)

  spId = aresObj.downloadAll(" %s.zip" % aresObj.http['SCRIPTS_NAME'])
  aresObj.item(spId).js('click', "window.location.href='../download/%s/package'" % aresObj.http['SCRIPTS_NAME'])

  return aresObj