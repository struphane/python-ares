"""

"""

import os
import sys
import pyclbr

NAME = 'HTML Components'

def report(aresObj):
  """ Display all the HTML components """
  modulesPath = tmpplPath = os.path.join(aresObj.http['DIRECTORY'], "..", "ares", "Lib")
  sys.path.append(modulesPath)
  aresObj.title("HTML Components")
  classNames = []
  for aresMod in os.listdir(modulesPath):
    if aresMod.endswith(".py") and aresMod.startswith("AresHtml"):
      module_info = pyclbr.readmodule(aresMod.replace(".py", ""))
      for item in module_info.values():
        classNames.append({'Class': aresObj.main(item.name, cssCls='', **{'report_name': '_AresDoc',
                                                                          'script_name': 'AresDocHtmlItem',
                                                                          'html_class': item.name,
                                                                          'html_alias': 'anchor'
                                                                          }),
                           'Ares Module': aresMod})
  aresObj.table(classNames, [{'colName': 'Class', 'type': 'object'},
                             {'colName': 'Ares Module'}], 'Ares Module Documentation')

