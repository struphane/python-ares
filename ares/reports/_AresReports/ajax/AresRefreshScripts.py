"""


"""

import os
import time
import json

from ares.Lib import Ares

def getRecordSet(aresObj, directory, restrictedExt=".py"):
  """ Return the list of script for a given path """
  recordSet = []
  if not os.path.exists(directory):
    return recordSet

  for script in os.listdir(directory):
    if not script.endswith(restrictedExt):
      continue

    downComp = aresObj.anchor_download('', **{'report_name': aresObj.http['USER_SCRIPT'], 'script': script})
    fileSize = Ares.convert_bytes(os.path.getsize(os.path.join(directory, script)))
    fileDate = time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime(os.path.getmtime(os.path.join(directory, script))))
    if script == "%s%s" % (aresObj.http['USER_SCRIPT'], restrictedExt):
      hyperLink = aresObj.anchor('%s%s' % (aresObj.http['USER_SCRIPT'], restrictedExt), **{'report_name': aresObj.http['USER_SCRIPT'], 'cssCls': ''})
      row = {'script': script, 'script_name': hyperLink, 'size': fileSize, 'lst_mod_dt': fileDate, 'download': downComp, 'delete': ''}
    else:
      remov = aresObj.icon('trash')
      remov.post('click', "../delete/%s" % aresObj.http['USER_SCRIPT'], {'SCRIPT': script}, 'display(data);')
      divComp = aresObj.div(script)
      divComp.toolTip(script)
      row = {'script': script, 'script_name': divComp, 'size': fileSize, 'lst_mod_dt': fileDate, 'download': downComp, 'delete': remov}
    recordSet.append(row)
  return recordSet

def call(aresObj):
  """ Ajax Call to refresh the tables """
  return {"status": "Updated", "data": [], "content": ""}