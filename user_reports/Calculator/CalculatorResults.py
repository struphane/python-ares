''' [SCRIPT COMMENT] '''

AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']
CHILD_PAGES = {'results': 'CalculatorResults.py'} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

import collections
import os

def report(aresObj):

  aresObj.title("Calculator Environment")
  if 'NODE' not in aresObj.http:
    dataTabe, testPerDay = [['Folder', 'Creation Date', '']], collections.defaultdict(int)
    for folder in aresObj.getFolders():
      if len(folder) == 2:
        ahref = aresObj.anchor(os.path.join(*folder))
        ahref.addLink('results?NODE=%s&DATE=%s' % (folder[1], folder[0]), dots='../..')
        info = aresObj.getFileInfo(folder[1], [folder[0]])
        iconComp = aresObj.icon('trash').deleteLink(aresObj.http['REPORT_NAME'], None, [folder[0], folder[1]])
        dataTabe.append([ahref, info['LAST_MOD_DT'], iconComp])
        testPerDay[folder[0]] += 1
    aresObj.table('Available Environments', dataTabe)
    return aresObj

  aresObj.title("IRC Results for %s" % aresObj.http['NODE'])
  aresObj.pieChart('', [["One", 29],["Four", 196]])
  aresObj.pieChart('', [["One", 1119],["Four", 5],["youpi", 5]])
  return aresObj