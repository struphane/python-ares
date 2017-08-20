''' [SCRIPT COMMENT] '''

AJAX_CALL = {} # Ajax call
CHILD_PAGES = {'results': 'CalculatorResults.py'} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

import collections

def report(aresObj):

  aresObj.title("Calculator Environment")
  if 'NODE' not in aresObj.http:
    dataTabe, testPerDay = [['Folder', 'Creation Date', '']], collections.defaultdict(int)
    for folder in aresObj.getFolders():
      print(folder)
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
  uploadComp = aresObj.upload().click(aresObj.http['REPORT_NAME'], folders=[aresObj.http['DATE'], aresObj.http['NODE']])
  uploadComp.js('change', '')
  button = aresObj.button("Refresh files with Live", cssCls='btn btn-info')
  button.post('click', '../ajax/%s/testAjax2.py' % aresObj.http['REPORT_NAME'], {'LOCATION': 'LocalLibs'}, 'alert(data)')

  aresObj.newline()
  aresObj.newline()
  fileInfo = [['FileName', 'Last Modification Date', 'Size', '', '']]
  for file in aresObj.getFiles([aresObj.http['DATE'], aresObj.http['NODE']]):
    info = aresObj.getFileInfo(file, [aresObj.http['DATE'], aresObj.http['NODE']])
    iconComp = aresObj.icon('trash').deleteLink(aresObj.http['REPORT_NAME'], file, [aresObj.http['DATE'], aresObj.http['NODE']])

    downComp = aresObj.icon('download')
    downComp.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['REPORT_NAME'], 'script': file})

    fileInfo.append([file, info['LAST_MOD_DT'], info['SIZE'], downComp, iconComp])
  aresObj.table('Configuration Files', fileInfo)

  ahref = aresObj.anchor("Go to Computation", cssCls='btn btn-success')
  ahref.addLink('results?NODE=%s&DATE=%s' % (aresObj.http['NODE'], aresObj.http['DATE']))

  aresObj.title3('Environment Statistics')
  aresObj.pieChart('', [["One", 29],["4fdffgfd", 196]])
  aresObj.pieChart('', [["One", 1119],["Four", 5],["youpi", 5]])

  return aresObj