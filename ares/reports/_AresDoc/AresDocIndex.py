""" Report Comment


"""

import collections
import os

NAME = 'Reports Documentation'
SHORTCUTS = [('Documentation', [
      ('Local Runs', 'AresDocLocalEnv'),
      ('HTML Components', 'AresDocHtml'),
      ('Graph Components', 'AresDocGraph'),
    ]
   )]

def report(aresObj):
  """

  """
  aresObj.title("Report Documentation")
  aresObj.title2("How to create a report")
