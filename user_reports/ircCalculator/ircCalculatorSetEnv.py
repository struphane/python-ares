''' [SCRIPT COMMENT] '''

AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']
CHILD_PAGES = {'results': 'ircCalculatorResults.py'} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

def report(aresObj):

  aresObj.title("IRC Results for %s" % aresObj.http['GET']['NODE'])
  uploadComp = aresObj.upload()
  uploadComp.js('change', '')
  uploadComp.post('click', '../upload/%s' % aresObj.http['REPORT_NAME'], {}, '', '%s/%s' % (aresObj.http['GET']['DATE'], aresObj.http['GET']['NODE']))
  button = aresObj.button("Refresh files with Live", cssCls='btn btn-info')

  aresObj.newline()
  aresObj.newline()
  fileInfo = [['FileName', 'Last Modification Date', 'Size', '', '']]
  for file in aresObj.getFiles([aresObj.http['GET']['DATE'], aresObj.http['GET']['NODE']]):
    info = aresObj.getFileInfo(file, [aresObj.http['GET']['DATE'], aresObj.http['GET']['NODE']])
    iconComp = aresObj.icon('trash')
    iconComp.post('click', "../delete_file/%s" % aresObj.http['REPORT_NAME'], {'SOURCE_PATH': '%s/%s' % (aresObj.http['GET']['DATE'], aresObj.http['GET']['NODE']),
                                                                               'FILE_NAME': file}, 'location.reload();')

    downComp = aresObj.icon('download')
    downComp.js('click', "window.location.href='../download/%(report_name)s/%(script)s'" % {'report_name': aresObj.http['REPORT_NAME'], 'script': file})

    fileInfo.append([file, info['LAST_MOD_DT'], info['SIZE'], downComp, iconComp])
  aresObj.table('Configuration Files', fileInfo)

  ahref = aresObj.anchor("Go to Computation", cssCls='btn btn-success')
  ahref.addLink('results?NODE=%s&DATE=%s' % (aresObj.http['GET']['NODE'], aresObj.http['GET']['DATE']))

  aresObj.title3('Environment Statistics')
  aresObj.pieChart('', [["One", 29],["4fdffgfd", 196]])
  aresObj.pieChart('', [["One", 1119],["Four", 5],["youpi", 5]])

  return aresObj