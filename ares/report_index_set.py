"""


"""

import zipfile
import os
import time

def call(aresObj):
  """ """
  path = os.path.join(aresObj.http['USER_PATH'], aresObj.http['POST']['REPORT'])
  print(path)
  if not os.path.exists(path):
      os.makedirs(path)
      fileFullPath = r"%s\%s.py" % (path, aresObj.http['POST']['REPORT'])
      reportFile = open(fileFullPath, "w")
      reportFile.write("''' [SCRIPT COMMENT] \n\n")
      reportFile.write(" >>>> Important variables \n")
      reportFile.write("In the python layer \n")
      reportFile.write("   aresObj.http['FILE'] is the current file \n")
      reportFile.write("   aresObj.http['REPORT_NAME'] is the current report environment name \n\n")
      reportFile.write("In the javascript layer \n")
      reportFile.write("   display(data) to return the result in a notification modal popup \n")
      reportFile.write("   preloader() to show a loading page \n\n")

      reportFile.write("AJAX_CALL = {} # Ajax call definition e.g ['MyRepotTestAjax.py']\n")
      reportFile.write("CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',} \n\n")
      reportFile.write("def report(aresObj):\n\n\n\n")
      reportFile.write("  return aresObj")
      reportFile.close()

      with zipfile.ZipFile("%s.zip" % fileFullPath, 'w') as zf:
        zf.write(fileFullPath, "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), "%s.py" % aresObj.http['POST']['REPORT']))

      return '%s - Report created' % aresObj.http['POST']['REPORT']

  else:
    return '%s - Already exist' % aresObj.http['POST']['REPORT']