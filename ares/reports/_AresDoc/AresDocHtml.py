"""

"""

import os
import sys
import pyclbr
import inspect

NAME = 'HTML Components'

def report(aresObj):
  """ Display all the HTML components """
  modulesPath = tmpplPath = os.path.join(aresObj.http['DIRECTORY'], "..", "ares", "Lib")
  sys.path.append(modulesPath)
  aresObj.title("HTML Components")
  classNames = []
  for aresMod in os.listdir(modulesPath):
    if aresMod.endswith(".py") and aresMod.startswith("AresHtml") and not aresMod.startswith("AresHtmlGraph") and aresMod != 'AresHtml.py':
      mod = __import__(aresMod.replace(".py", ""))
      for name, cls in inspect.getmembers(mod):
        if inspect.isclass(cls) and hasattr(cls, 'alias'):
          classNames.append({'Class': aresObj.main(name, cssCls='',
                                                   **{'report_name': '_AresDoc',
                                                       'script_name': 'AresDocHtmlItem',
                                                        'html_module': aresMod,
                                                        'html_class': name,
                                                        'html_alias': cls.alias}),
                             'Ares Module': aresMod,
                             'Documentation': aresObj.external_link('Website', cls.reference),
                             })
  aresObj.table(classNames, [{'colName': 'Class', 'type': 'object'},
                             {'colName': 'Ares Module'},
                             {'colName': 'Documentation', 'type': 'object'}
                             ], 'Ares Module Documentation')

