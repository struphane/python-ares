"""

http://127.0.0.1:5000/reports/run/JsWikiScripts

"""


def report(aresObj):
  """

  """
  wikiObj = aresObj.wiki(aresObj, 'scriptName', ['Youpi', 'test'])
  aresObj.script('youpi', **{'report_name': 'JsWikiScripts', 'script_name': 'JsWikiScriptsTest'})
  return aresObj
