"""


"""

import zipfile
import os
import time


def call(aresObj):
  """ """
  path = os.path.join(aresObj.http['DIRECTORY'], aresObj.http['report_name'])
  if not os.path.exists(path):
      os.makedirs(path)
      fileFullPath = os.path.join(path, "%s.py" % aresObj.http['report_name'])
      reportFile = open(fileFullPath, "w")
      reportFile.write("''' [SCRIPT COMMENT] \n\n")
      reportFile.write(" >>>> Important variables \n")
      reportFile.write("In the python layer \n")
      reportFile.write("   aresObj.http['FILE'] is the current file \n")
      reportFile.write("   aresObj.http['REPORT_NAME'] is the current report environment name \n\n")
      reportFile.write("In the javascript layer \n")
      reportFile.write("   display(data) to return the result in a notification modal popup \n")
      reportFile.write("   preloader() to show a loading page \n\n")
      reportFile.write("AJAX_CALL = {} # Ajax call definition \n")
      reportFile.write("CHILD_PAGES = {} # Child pages call definition e.g {'test': 'MyRepotTestChild.py',} \n\n")
      reportFile.write("def report(aresObj):\n\n\n\n")
      reportFile.write("  return aresObj")
      reportFile.close()
      # Add entry to a system log files
      reportFile = open(os.path.join(path, "log_ares.dat"), "w")
      reportFile.write("EVENT#DAY#TIME#COMMENT\n")
      showtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")
      reportFile.write("FOLDER CREATION#%s#%s#%s\n" % (showtime[0], showtime[1], aresObj.http['report_name']))
      reportFile.close()
      with zipfile.ZipFile("%s.zip" % fileFullPath, 'w') as zf:
        zf.write(fileFullPath, "%s_%s" % (time.strftime("%Y%m%d-%H%M%S"), "%s.py" % aresObj.http['report_name']))
      return '%s - Report created' % aresObj.http['report_name']

  else:
    return '%s - Already exist' % aresObj.http['report_name']