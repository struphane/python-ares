""" Service dedicated to parse files according to a standard Configurations
@author: Olivier Nogues

Those configuration are mandatories in the framework as they will allow you to display
in a comprehensive manner the data in the framework. Those configurations are important
for outputs but also static files.

You can retrieve data from this module by interating on it.
Also there is a function in Ares to allow you to iterate on files which are configured in your
environment.

Please do not use this module directly in your production code.

"""

import re
import csv

regex = re.compile('[^a-zA-Z0-9_]')

class FileParser(object):
  """
  """
  hdrLines = 0

  def __init__(self, inFile):
    """ Create a file object """
    self.__inputFile = inFile
    for _ in range(self.hdrLines):
      self.__inputFile.next()
    self.header, self.colCnvFnc, keyMapCol = [], {}, {}
    for i, col in enumerate(self.cols):
      self.header.append(regex.sub('', col['colName']))
      keyMapCol[col['colName']] = i
      if 'convertFnc' in col:
        self.colCnvFnc[i] = col['convertFnc']
    vCols = getattr(self, 'vCols', [])
    self.vHeader, self.vColCnvFnc = [], {}
    for i, vCol in enumerate(vCols):
      self.vHeader.append((i, regex.sub('', vCol['colName'])))
      self.vColCnvFnc[i] = ([regex.sub('', col)  for col in vCol['mapCols']], vCol['convertFnc'])

  def __iter__(self):
    """ Iterator to return a line """
    for line in self.__inputFile:
      reader  = csv.reader([line], skipinitialspace=True, delimiter=self.delimiter)
      for row in reader:
        rec = dict(zip(self.header, row))
        for i, transFnc in self.colCnvFnc.items():
          rec[self.header[i]] = transFnc(row[i])
        for i, name in self.vHeader:
          rec[name] = self.vColCnvFnc[i][1](*[rec[col] for col in self.vColCnvFnc[i][0]])
        yield rec

  @classmethod
  def getHeader(cls):
    """ Return the header definition """
    fileHeader = []
    for col in cls.cols:
      fileHeader.append({'colName': col['colName'], 'key': regex.sub('', col['colName'])})
    return fileHeader
