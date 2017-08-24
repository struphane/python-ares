''' [SCRIPT COMMENT] '''

DISPLAY = 'Generic Calculator'
SHORTCUTS = [('Configuration', 'Calculator.py'),
             ('Environments', 'CalculatorSetEnv.py'),
             ('Calculator', 'CalculatorResults.py')]

AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']
CHILD_PAGES = {'results': 'CalculatorSetEnv.py'} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

import collections
import os

def report(aresObj):
  aresObj.title('IRC Calculator')
  dateObj = aresObj.date('COB Date')
  nodeObj = aresObj.input('Node')
  nameObj = aresObj.input('Name')
  button = aresObj.button("Create Environment")
  button.post('click', '/reports/folder/create',
              "{'REPORT_NAME': '%s', 'FOLDERS': %s + '/' + %s}" % (aresObj.http['FILE'], dateObj.val, nodeObj.val),
              'display(data);setTimeout(function() {location.reload();}, 1000);    ')
  aresObj.container('Create Test Environment', [dateObj, nodeObj, nameObj, aresObj, button])

  dataTabe, testPerDay = [['Folder', 'Creation Date', '']], collections.defaultdict(int)
  for folder in aresObj.getFolders():
    if len(folder) == 2:
      ahref = aresObj.anchor(os.path.join(*folder))
      ahref.addLink('results?NODE=%s&DATE=%s' % (folder[1], folder[0]))
      info = aresObj.getFileInfo(folder[1], [folder[0]])
      iconComp = aresObj.icon('trash').deleteLink(aresObj.http['REPORT_NAME'], None, [folder[0], folder[1]])
      dataTabe.append([ahref, info['LAST_MOD_DT'], iconComp])
      testPerDay[folder[0]] += 1
  aresObj.bar('Tests per day', [ {"key": "Cumulative Return","values": [[k, v] for k, v in testPerDay.items()] }])
  aresObj.table('Available Environments', dataTabe)
  return aresObj