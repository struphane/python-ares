"""

http://127.0.0.1:5000/reports/run/JsWikiScripts

"""

import os
import sys

NAME = "Download Button Test"


def report(aresObj):
  """
  Entry point for the SPE script monitoring

  This page will be the entry point and it will return the comments for a given script.
  Those comments will then be potentially updated by users in order to improve the quality of the processes

  In this page only relevant information related to the documentation will be displayed to users.
  Scripts not migrated to the new framework, without the correct BDI standards, will not be available.

  """
  aresObj.title("Download Button")
  print(aresObj.http)
  aresObj.download('test.txt')


  return aresObj
