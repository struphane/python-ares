""" Simple wrapper to set up the configuration on the local environment

This will retrieve the scripts but also it will get the server path

"""

import shutil
import requests
import zipfile
import contextlib
import os
import io

SERVER_PATH = 'http://127.0.0.1:5000'

if __name__ == '__main__':
  response = requests.post("%s/reports/download/ares" % SERVER_PATH)
  with contextlib.closing(response), zipfile.ZipFile(io.BytesIO(response.content)) as archive:
    for member in archive.infolist():
      splitName = os.path.split(member.filename)
      currPath = []
      if splitName[0] == '':
        inFile = open(os.path.join(splitName[-1]), "wb")
        inFile.write(archive.read(member))
        inFile.close()
      else:
        for folder in splitName[:-1]:
          currPath.append(folder)
          filePath = os.path.join(*currPath)
          if not os.path.exists(filePath):
            os.makedirs(filePath)
          if splitName[-1] == '':
            continue

          inFile = open(os.path.join(filePath, splitName[-1]), "wb")
          inFile.write(archive.read(member))
          inFile.close()

  #
  for path in (['ares'], ['ares', 'Lib'], ['ares', 'Lib', 'html'], ['ares', 'Lib', 'graph']):
    strPath = os.path.join(*path)
    open(os.path.join(strPath, '__init__.py'), 'w').close()

  dummyReportName = 'NewReport'
  # Then creation of the dummy report environment
  if os.path.exists(dummyReportName):
    shutil.rmtree(dummyReportName)

  os.makedirs(dummyReportName)

  # Create the folders
  os.makedirs(os.path.join(dummyReportName, 'js')) # for the javascript fragments
  os.makedirs(os.path.join(dummyReportName, 'json')) # for the static configurations
  os.makedirs(os.path.join(dummyReportName, 'ajax')) # for the python dynamic data extraction
  os.makedirs(os.path.join(dummyReportName, 'statics')) # for the MRX Static views (1 view per MRX screen)
  os.makedirs(os.path.join(dummyReportName, 'outputs')) # To push output files
  os.makedirs(os.path.join(dummyReportName, 'styles')) # for the special CSS and JS files to be used on the server
  os.makedirs(os.path.join(dummyReportName, 'saved')) # To push the already ready HTML reports

  shutil.copy2(os.path.join('ares', 'tmpl', 'tmpl_report.py'), os.path.join(dummyReportName, "%s.py" % dummyReportName))
