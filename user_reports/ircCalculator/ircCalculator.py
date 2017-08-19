''' [SCRIPT COMMENT] '''

AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']
CHILD_PAGES = {'results': 'ircCalculatorResults.py'} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',}

def report(aresObj):
  aresObj.title('IRC Calculator')
  dateObj = aresObj.date('COB Date')
  nodeObj = aresObj.input('Node')
  nameObj = aresObj.input('Name')
  button = aresObj.button("Create Environment")
  button.post('click', '/reports/folder/create',
              "{'REPORT_NAME': '%s', 'FOLDERS': %s + '/' + %s}" % (aresObj.http['FILE'], dateObj.jsVal(), nodeObj.jsVal()),
              'display(data);setTimeout(function() {location.reload();}, 1000);    ')

  aresObj.container('Create Test Environment', [dateObj, nodeObj, nameObj, aresObj, button])

  dataTabe = [['Folder']]
  for folder in aresObj.getFolders():
    env = folder.split("\\")
    if len(env) == 3:
      ahref = aresObj.anchor(folder)
      ahref.addLink('results?NODE=%s&DATE=%s' % (env[2], env[1]))
      dataTabe.append([ahref])
  aresObj.table('Available Environments', dataTabe)
  return aresObj