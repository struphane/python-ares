"""


"""

import os

AJAX_CALL = {
  'download': 'MyRepotTestAjax.py'
  }

CHILD_PAGES = {
	'report': 'MyRepotTestChild.py',
  'test3': 'MyRepotTestChild3.py',
  }

def report(aresObj, localPath=None):
  """

  """
  dropId = aresObj.dropFile()
  aresObj.item(dropId).reportName = aresObj.http['SCRIPTS_NAME']
  CHILD_PAGES['report'] = "../reports/%s" % aresObj.http['SCRIPTS_NAME']
  aresObj.anchor(" > Go to Report", 'report', CHILD_PAGES, localPath)

  aresObj.title(2, 'List des scripts')
  scripts = [('%s.py' % aresObj.http['SCRIPTS_NAME'], 'Main Script', '')]
  for childScripts in aresObj.http['SCRIPTS_CHILD']:
    scripts.append(('%s.py' % childScripts, 'Child of %s' % aresObj.http['SCRIPTS_NAME'], 'Remove'))

  aresObj.table(['Script Name', 'Type', 'Action'], scripts)
  aresObj.title(2, 'Report Description')
  aresObj.paragraph(aresObj.http['SCRIPTS_DSC'])

  spId = aresObj.button("Download report", 'btn-success')
  aresObj.item(spId).js('click',
                        'window.location.href="/script_download/%s/MyRepotTestChild.py"; return false;' % aresObj.http['SCRIPTS_NAME'])

  return aresObj.html(localPath, title='%s - ReportEnvironment' % aresObj.http['SCRIPTS_NAME'])