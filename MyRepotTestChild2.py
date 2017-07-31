""" Report Module

"""

CHILD_PAGES = {} # No Child for this page

def report(aresObj, localPath=None):
  """ Empty report with only a title """
  aresObj.title(1, 'I am a child 2')
  return aresObj.html(localPath, title='Third Page')
	