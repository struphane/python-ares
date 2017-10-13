"""

"""

import os
import sys
import pyclbr
import inspect

NAME = 'HTML Components'
DOWNLOAD = None

def report(aresObj):
  """ Display all the HTML components """
  modulesPath = tmpplPath = os.path.join(aresObj.http['DIRECTORY'], "..", "ares", "Lib", 'html')
  sys.path.append(modulesPath)

  aresObj.title("A suite of HTML components available")
  classNames = []
  for aresMod in os.listdir(modulesPath):
    if aresMod.endswith(".py") and aresMod.startswith("AresHtml") and not aresMod.startswith("AresHtmlGraph") and aresMod != 'AresHtml.py':
      mod = __import__(aresMod.replace(".py", ""))
      for name, cls in inspect.getmembers(mod):
        if inspect.isclass(cls) and hasattr(cls, 'alias'):
          classNames.append({'Class': aresObj.href(name, 'AresDocHtmlItem',
                                                   {'html_module': aresMod, 'html_class': name, 'html_alias': cls.alias}, cssCls=''),
                             'Ares Module': aresMod,
                             #'Documentation': aresObj.external_link('Website', cls.reference),
                             })
  aresObj.table(classNames, [{'colName': 'Class', 'type': 'object'},
                             {'colName': 'Ares Module'},
                             #{'colName': 'Documentation', 'type': 'object'}
                             ], 'Ares Module Documentation')

