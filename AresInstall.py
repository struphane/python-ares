""" Simple wrapper to set up the configuration on the local environment

This will retrieve the scripts but also it will get the server path

"""

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
          inFile = open(os.path.join(filePath, splitName[-1]), "wb")
          inFile.write(archive.read(member))
          inFile.close()
