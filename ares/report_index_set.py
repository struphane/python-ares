"""


"""

import os

def call(aresObj):
  """ """
  path = os.path.join(aresObj.http['USER_PATH'], aresObj.http['POST']['report'])
  if not os.path.exists(path):
      os.makedirs(path)
      reportFile = open(r"%s\%s.py" % (path, aresObj.http['POST']['report']), "w")
      reportFile.write("''' [SCRIPT COMMENT] '''\n\n")
      reportFile.write("AJAX_CALL = ['MyRepotTestAjax.py'] # Ajax call definition\n")
      reportFile.write("CHILD_PAGES = {'test': 'MyRepotTestChild.py',} # Child pages call definition\n\n")
      reportFile.write("def report(aresObj, localPath=None):\n\n\n\n")
      reportFile.write("  return aresObj")
      reportFile.close()
      return '%s - Report created' % aresObj.http['POST']['report']

  else:
    return '%s - Already exist' % aresObj.http['POST']['report']