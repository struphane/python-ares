"""

http://127.0.0.1:5000/reports/run/JsWikiScripts

"""


def report(aresObj):
  """

  """
  path = r"E:\GitHub\Ares\ares"
  scriptName = aresObj.http['script'].replace(".py", "")
  wikiObj = aresObj.wiki(aresObj, scriptName, open(r"%s\%s.py" % (path, scriptName)).__doc__.split("\n"))

  aresObj.anchor('youpi', **{'report_name': 'JsWikiScripts', 'script_name': 'JsWikiScriptsTest',
                             'var': 'youpi', 'cssCls': 'Yes'
                             })
  return aresObj
