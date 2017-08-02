"""


"""

import os

def report(aresObj, localPath=None):
  """

  """
  dropId = aresObj.dropFile()
  aresObj.item(dropId).reportName = aresObj.http['SCRIPTS_NAME']
  aresObj.title(2, 'List des scripts')
  scripts = [('%s.py' % aresObj.http['SCRIPTS_NAME'], 'Main Script', '')]
  for childScripts in aresObj.http['SCRIPTS_CHILD']:
    scripts.append(('%s.py' % childScripts, 'Child of %s' % aresObj.http['SCRIPTS_NAME'], 'Remove'))

  aresObj.table(['Script Name', 'Type', 'Action'], scripts)
  aresObj.title(2, 'Report Description')
  aresObj.paragraph(aresObj.http['SCRIPTS_DSC'])
  return aresObj.html(localPath, title='%s - ReportEnvironment' % aresObj.http['SCRIPTS_NAME'])