"""

http://127.0.0.1:5000/reports/run/JsWikiScripts

"""


def report(aresObj):
  """

  """
  scriptName = aresObj.http['script'].replace(".py", "")
  report = open(r"D:\GitHub\python-ares\ares\%s.py" % scriptName)
  aresObj.wiki(aresObj, scriptName, report)
  report.close()

  aresObj.script('youpi', **{'report_name': 'JsWikiScripts', 'script_name': 'JsWikiScriptsTest',
                             'var': 'youpi', 'cssCls': 'Yes'
                             })
  return aresObj

