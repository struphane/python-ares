''' [SCRIPT COMMENT] '''

AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']
CHILD_PAGES = {'results': 'ircCalculatorResults.py'} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

def report(aresObj):
  aresObj.title('IRC Calculator')
  aresObj.title3('Environment set up')
  dateObj = aresObj.date('COB Date')
  nodeObj = aresObj.input('Node')
  upload = aresObj.upload('Select File')
  upload.js('change', 'alert(%s);' %  upload.jsVal())
  aresObj.input('Name')
  button = aresObj.button("Create")
  button.post('click', '/reports/folder/create',
              "{'REPORT_NAME': '%s', 'FOLDERS': %s + '/' + %s}" % (aresObj.http['FILE'], dateObj.jsVal(), nodeObj.jsVal()),
              'display(data);setTimeout(function() {location.reload();}, 1000);    ')
  aresObj.newline()
  aresObj.newline()
  aresObj.title3('Available Environments')

  dataTabe = [['Folder']]
  for folder in aresObj.getFolders():
    env = folder.split("\\")
    if len(env) == 3:
      ahref = aresObj.anchor(folder)
      ahref.addLink('results?NODE=%s&DATE=%s' % (env[2], env[1]))
      dataTabe.append([ahref])
  aresObj.table(dataTabe)
  return aresObj