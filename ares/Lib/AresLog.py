""" Dedicated module to store the Ares Log information

I believe it is a good practise to have a dedicated module in order to centralise all the log even actions and the
structure of the log_ares.dat file

At the beginning I put this in each module but I believe that the format might change and it would be better to have
only 1 place to produce, update and parse the file. It will make enhancements easier

This module will also take care of the storage of the previous version of the report.
It will store the results in the a dedicated Zip archive

"""

import os
import time

class FileCfgnLog(object):
  """ The file configuration for the main Ares Log file """
  fileName = "log_ares.dat"
  delimiter = "#"
  cols = [{"key": 'EVENT', 'ColName': 'Event Type'},
          {"key": 'DAY', 'ColName': 'Day'},
          {"key": 'TIME', 'ColName': 'TimeStamp'},
          {"key": 'TYPE', 'ColName': 'Type'},
          {"key": 'SCRIPT', 'ColName': 'Script'},
          {"key": 'COMMENT', 'ColName': 'Comment'}]

  def __init__(self):
    """ Instantiate the object and create the line format """
    self.line = "%s\n" % self.delimiter.join([ "%%(%s)s" % col['key'] for col in self.cols])

class AresLog(object):
  """

  """

  def __init__(self, rootPath, reportName, configData):
    """ Instantiate the object and store the report name """
    self.reportName = reportName
    self.aresRoot = rootPath
    self.configData = configData
    self.cfgn = FileCfgnLog()

  def addScript(self, scriptType, scriptName):
    """ Add a new script to the log File """
    date, timeStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")
    data = {"EVENT": 'CREATE_SCRIPT',  'DAY': date, 'TIME': timeStamp, 'TYPE': scriptType, 'SCRIPT': scriptName,'COMMENT': scriptName}
    logFile = open(os.path.join(self.aresRoot, self.configData.ARES_USERS_LOCATION, self.reportName, self.cfgn.fileName), "a")
    logFile.write(self.cfgn.line % data)
    logFile.close()

  def createFolder(self):
    """ Add the folder creation to the log File """
    date, timeStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()).split(" ")
    data = {"EVENT": 'FOLDER_CREATION',  'DAY': date, 'TIME': timeStamp, 'TYPE': 'Report', 'SCRIPT': self.reportName, 'COMMENT': ''}
    header = dict([(col["key"], col['ColName'])for col in self.cfgn.cols])
    logFile = open(os.path.join(self.aresRoot, self.configData.ARES_USERS_LOCATION, self.reportName, self.cfgn.fileName), "a")
    logFile.write(self.cfgn.line % header)
    logFile.write(self.cfgn.line % data)
    logFile.close()