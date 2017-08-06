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
  aId = aresObj.anchor('%s.py' % aresObj.http['SCRIPTS_NAME'], 'report', CHILD_PAGES, localPath)
  aresObj.title(2, 'List des scripts')
  dId = aresObj.download()

  fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], '%s.py' % aresObj.http['SCRIPTS_NAME'])))
  fileDate = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], '%s.py' % aresObj.http['SCRIPTS_NAME']))))

  scripts = [(aresObj.item(aId), fileSize, fileDate,  'Main Script', aresObj.item(dId), '')]
  for childScripts in aresObj.http['SCRIPTS']:
    if childScripts == "%s.py" % aresObj.http['SCRIPTS_NAME'] or childScripts == '__pycache__':
      continue

    bId = aresObj.remove()
    dId = aresObj.download()
    fileSize = convert_bytes(os.path.getsize(os.path.join(aresObj.http['SCRIPTS_PATH'], childScripts)))
    fileDate = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(aresObj.http['SCRIPTS_PATH'], childScripts))))

    aresObj.item(bId).jsAjax('click', 'location.href = "/reports/page/%s";' % aresObj.http['SCRIPTS_NAME'], aresObj.http['SCRIPTS_NAME'], localPath, {'SCRIPT': "'%s'" % childScripts})
    scripts.append((childScripts, fileSize, fileDate, 'Child of %s' % aresObj.http['SCRIPTS_NAME'], aresObj.item(dId), aresObj.item(bId)))

  spId = aresObj.button(" %s.zip" % aresObj.http['SCRIPTS_NAME'], 'btn-success glyphicon glyphicon-download-alt')
  tpId = aresObj.nestedtable(['Script Name', 'Size', 'Modification Date', 'Type', 'download', 'delete'], scripts)

  dropId = aresObj.dropFile()
  aresObj.item(dropId).reportName = aresObj.http['SCRIPTS_NAME']
  aresObj.container([aresObj.item(tpId), aresObj.item(spId)])

  aresObj.item(spId).js('click',
                        'window.location.href="/script_download/%s/MyRepotTestChild.py"; return false;' % aresObj.http['SCRIPTS_NAME'])
  return aresObj