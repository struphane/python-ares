""" Simple wrapper to set up the configuration on the local environment

This will retrieve the scripts but also it will get the server path

"""

import shutil
import requests
import zipfile
import contextlib
import os
import io
import AresCreateLocalEnv

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
    
  # Then creation of the dummy report environment
  AresCreateLocalEnv.createEnv('NewReport', True)
