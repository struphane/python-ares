"""

"""

import importlib

NAME = 'HTML Item'
DOWNLOAD = None

def report(aresObj):
  """

  """
  aresObj.title("HTML Definition for the %s component" % aresObj.http['HTML_CLASS'])
  mod = importlib.import_module("ares.Lib.%s" % aresObj.http['HTML_MODULE'].replace(".py", ""))
  htmlObj = getattr(mod, aresObj.http['HTML_CLASS']).aresExample(aresObj)

