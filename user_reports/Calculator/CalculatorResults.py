''' [SCRIPT COMMENT] '''

AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']
CHILD_PAGES = {'results': 'CalculatorResults.py'} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

import collections

def report(aresObj):

  aresObj.title("Calculator Environment")
  if 'NODE' not in aresObj.http:
    dataTabe, testPerDay = [['Folder', 'Creation Date', '']], collections.defaultdict(int)
    for folder in aresObj.getFolders():
      env = folder.split("\\")
      if len(env) == 3:
        ahref = aresObj.anchor(folder)
        ahref.addLink('results?NODE=%s&DATE=%s' % (env[2], env[1]), dots='../..')
        info = aresObj.getFileInfo(env[2], [env[1]])
        iconComp = aresObj.icon('trash').deleteLink(aresObj.http['REPORT_NAME'], None, [env[1], env[2]])
        dataTabe.append([ahref, info['LAST_MOD_DT'], iconComp])
        testPerDay[env[1]] += 1
    aresObj.table('Available Environments', dataTabe)

    return aresObj

  aresObj.title("IRC Results for %s" % aresObj.http['NODE'])
  aresObj.pieChart('', [["One", 29],["Four", 196]])
  aresObj.pieChart('', [["One", 1119],["Four", 5],["youpi", 5]])
  return aresObj